"""Convert a raw Word document (.docx) into draft Markdown for render_report.py, plus its images.

Headings come from heading styles / outline levels; bold, italic, links, footnotes, bullet and numbered lists,
tables and pictures are kept. Direct formatting (fonts, colours, sizes) is dropped on purpose: the VCCI template
supplies it. The draft still needs an editorial pass (front matter, captions, lead/callout blocks).

    python extract_docx.py raw.docx -o work/report.md      # images go to work/media/
"""
import argparse, os, re, sys
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import NS, W, R, read_package


def load(files, name):
    return etree.fromstring(files[name]) if name in files else None


class Extractor:
    def __init__(self, path, media_dir, media_rel):
        self.files = read_package(path)
        self.doc = load(self.files, 'word/document.xml')
        self.rels = {e.get('Id'): e for e in load(self.files, 'word/_rels/document.xml.rels')}
        self.media_dir, self.media_rel = media_dir, media_rel
        self.heading_of = self._heading_styles()
        self.num_fmt = self._numbering()
        self.footnotes, self.fn_order = self._footnotes(), []
        self.saved = {}

    def _heading_styles(self):
        out = {}
        self.style_num = {}   # styleId -> numPr defined on the style (e.g. List Bullet, List Number)
        st = load(self.files, 'word/styles.xml')
        for s in st.iter(W + 'style'):
            np_ = s.find(f'{W}pPr/{W}numPr')
            if np_ is not None: self.style_num[s.get(W + 'styleId')] = np_
            sid = s.get(W + 'styleId'); name = (s.find(W + 'name').get(W + 'val') if s.find(W + 'name') is not None else '').lower()
            lvl = s.find(f'{W}pPr/{W}outlineLvl')
            m = re.match(r'heading (\d)', name)
            if m: out[sid] = int(m.group(1))
            elif lvl is not None and int(lvl.get(W + 'val')) < 9: out[sid] = int(lvl.get(W + 'val')) + 1
            elif name in ('title',): out[sid] = 0
        return out

    def _numbering(self):
        nb = load(self.files, 'word/numbering.xml')
        if nb is None: return {}
        absf = {}
        for a in nb.iter(W + 'abstractNum'):
            absf[a.get(W + 'abstractNumId')] = {l.get(W + 'ilvl'): (l.find(W + 'numFmt').get(W + 'val') if l.find(W + 'numFmt') is not None else 'bullet')
                                                for l in a.iter(W + 'lvl')}
        return {n.get(W + 'numId'): absf.get(n.find(W + 'abstractNumId').get(W + 'val'), {}) for n in nb.iter(W + 'num')}

    def _footnotes(self):
        fn = load(self.files, 'word/footnotes.xml')
        out = {}
        if fn is None: return out
        for f in fn.iter(W + 'footnote'):
            if f.get(W + 'type'): continue
            out[f.get(W + 'id')] = ' '.join(self.inline(p) for p in f.iter(W + 'p')).strip()
        return out

    def save_image(self, rid):
        if rid in self.saved: return self.saved[rid]
        rel = self.rels.get(rid)
        if rel is None or rel.get('TargetMode') == 'External': return None
        target = rel.get('Target')
        src = target.lstrip('/') if target.startswith('/') else 'word/' + target
        if src not in self.files: return None
        os.makedirs(self.media_dir, exist_ok=True)
        name = f'image{len(self.saved) + 1}{os.path.splitext(src)[1].lower()}'
        open(os.path.join(self.media_dir, name), 'wb').write(self.files[src])
        self.saved[rid] = f'{self.media_rel}/{name}'
        return self.saved[rid]

    def inline(self, p):
        """Paragraph -> Markdown inline text (bold/italic/links/footnotes)."""
        parts = []
        for el in p:
            tag = etree.QName(el).localname
            if tag == 'r': parts.append(self.run(el))
            elif tag == 'hyperlink':
                txt = ''.join(self.run(r) for r in el.iter(W + 'r'))
                rel = self.rels.get(el.get(R + 'id'))
                parts.append(f'[{txt}]({rel.get("Target")})' if rel is not None and txt.strip() else txt)
            elif tag in ('ins', 'smartTag', 'customXml', 'sdt'):
                for r in el.iter(W + 'r'): parts.append(self.run(r))
        text = ''.join(parts).replace('****', '')          # merge adjacent bold runs
        return re.sub(r'[ \t]{2,}', ' ', text).strip()

    def run(self, r):
        rpr = r.find(W + 'rPr')
        def on(tag):
            e = rpr.find(W + tag) if rpr is not None else None
            return e is not None and e.get(W + 'val') not in ('0', 'false')
        txt = ''
        for c in r:
            t = etree.QName(c).localname
            if t == 't': txt += c.text or ''
            elif t == 'tab': txt += ' '
            elif t == 'br' and c.get(W + 'type') != 'page': txt += '\n'   # line break; kept as <br> in table cells
            elif t == 'footnoteReference':
                fid = c.get(W + 'id'); self.fn_order.append(fid); txt += f'[^{fid}]'
            elif t in ('drawing', 'pict'):
                blip = c.find('.//{%s}blip' % NS['a'])
                if blip is not None:
                    path = self.save_image(blip.get(R + 'embed'))
                    if path: txt += f'\n\n![]({path})\n\n'
        if not txt.strip() or '![' in txt or '[^' in txt: return txt
        lead, core, trail = re.match(r'^(\s*)(.*?)(\s*)$', txt, re.S).groups()
        if on('b') and on('i'): core = f'***{core}***'
        elif on('b'): core = f'**{core}**'
        elif on('i'): core = f'*{core}*'
        return lead + core + trail

    def para(self, p):
        ppr = p.find(W + 'pPr')
        sid = ppr.find(W + 'pStyle').get(W + 'val') if ppr is not None and ppr.find(W + 'pStyle') is not None else None
        text = self.inline(p)
        if not text: return None
        lvl = self.heading_of.get(sid)
        ol = ppr.find(W + 'outlineLvl') if ppr is not None else None
        if lvl is None and ol is not None and int(ol.get(W + 'val')) < 9: lvl = int(ol.get(W + 'val')) + 1
        if lvl == 0: return f'<!-- title: {text} -->'
        if lvl:
            return '#' * min(lvl, 3) + ' ' + re.sub(r'^\*+|\*+$', '', text)
        num = ppr.find(W + 'numPr') if ppr is not None else None
        if num is None and sid in self.style_num: num = self.style_num[sid]
        if num is not None and num.find(W + 'numId') is not None and num.find(W + 'numId').get(W + 'val') != '0':
            ilvl = num.find(W + 'ilvl').get(W + 'val') if num.find(W + 'ilvl') is not None else '0'
            fmt = self.num_fmt.get(num.find(W + 'numId').get(W + 'val'), {}).get(ilvl, 'bullet')
            return '  ' * min(int(ilvl), 2) + ('1. ' if fmt not in ('bullet', 'none') else '- ') + text
        if sid and 'quote' in sid.lower(): return '> ' + text
        if sid and 'caption' in sid.lower(): return f'<!-- caption: {text} -->'
        return text

    def table(self, tbl):
        rows = []
        for tr in tbl.findall(W + 'tr'):
            row = []
            for tc in tr.findall(W + 'tc'):
                cell = '<br>'.join(t for t in (self.inline(p).replace('\n', '<br>') for p in tc.iter(W + 'p')) if t)
                span = tc.find(f'{W}tcPr/{W}gridSpan')
                row.append(cell.replace('|', '\\|'))
                if span is not None: row += ['<<'] * (int(span.get(W + 'val')) - 1)   # merged cells
            rows.append(row)
        if not rows: return ''
        n = max(len(r) for r in rows)
        rows = [r + [''] * (n - len(r)) for r in rows]
        lines = ['| ' + ' | '.join(rows[0]) + ' |', '|' + '---|' * n] + ['| ' + ' | '.join(r) + ' |' for r in rows[1:]]
        return 'Bảng: [tên bảng]\n' + '\n'.join(lines)

    def convert(self):
        out, prev_list = [], False
        for el in self.doc.find(W + 'body'):
            tag = etree.QName(el).localname
            if tag == 'p':
                s = self.para(el)
                if s is None: continue
                if not s.startswith('!['): s = re.sub(r' *\n *', ' ', s)
                is_list = bool(re.match(r'^\s*(-|1\.) ', s))
                if out and not (is_list and prev_list): out.append('')
                out.append(s); prev_list = is_list
            elif tag == 'tbl':
                out += ['', self.table(el)]; prev_list = False
            elif tag == 'sdt':
                for p in el.iter(W + 'p'):
                    s = self.para(p)
                    if s: out += ['', s]
        if self.fn_order:
            out.append('')
            for fid in dict.fromkeys(self.fn_order):
                out.append(f'[^{fid}]: {self.footnotes.get(fid, "")}')
        return re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip() + '\n'


FRONT = """---
title: [Tên báo cáo]
subtitle: [Tiêu đề phụ, hoặc xóa dòng này]
date: [Tháng 10 / 2026]
unit: [Đơn vị thực hiện, hoặc xóa dòng này]
header: [Tên rút gọn cho đầu trang]
---

"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('docx')
    ap.add_argument('-o', '--out', help='output .md (default: next to the .docx)')
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.docx)[0] + '.md'
    media = os.path.join(os.path.dirname(os.path.abspath(out)), 'media')
    ex = Extractor(a.docx, media, 'media')
    md = ex.convert()
    open(out, 'w', encoding='utf-8').write(FRONT + md)
    print(f'Wrote {out}  ({len(ex.saved)} images, {len(set(ex.fn_order))} footnotes)')


if __name__ == '__main__':
    main()
