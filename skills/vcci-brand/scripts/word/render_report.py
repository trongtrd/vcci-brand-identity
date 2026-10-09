"""Render a VCCI-formatted report (.docx) from structured Markdown, using brand-assets/06_Templates/Word/VCCI_Report.dotx.

The template's cover, table of contents, running header/footer and back cover are kept; its sample body is
replaced by the Markdown content, mapped onto the template's own styles. Markdown syntax: see
skills/vcci-brand/references/word-markdown.md.

    python render_report.py report.md -o report.docx

Needs Python 3.9+, lxml and Pillow. Does not need Microsoft Word (run finalize.py afterwards to refresh the
table of contents and export a PDF when Word is available).
"""
import argparse, copy, os, re, sys
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (NS, W, R, REL_IMAGE, REL_LINK, TEMPLATE_CT, DOC_CT, frag, template_path,
                    read_package, write_package, xml_bytes)

TEXT_WIDTH = 9412          # twips between the report body margins
EMU_PER_TWIP = 635
BULLET_NUM, NUMBERED_ABSTRACT = '2', '2'   # template numbering: numId 2 = bullets, abstractNum 2 = 1. 2. 3.
NUMERIC = re.compile(r'^[\[(]?[+\-−–]?\s?[\d.,]+\s?(%|‰|pp|đ|USD|VND)?[\])]?$')

# ---------------------------------------------------------------- Markdown parsing

def parse_front_matter(text):
    meta = {}
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ':' in line and not line.lstrip().startswith('#'):
                    k, v = line.split(':', 1)
                    meta[k.strip().lower()] = v.strip().strip('"').strip("'")
            text = text[end + 4:]
    return meta, text


def parse_attrs(s):
    """'{.light .total label="Phụ lục A" width=60%}' -> ({'light','total'}, {'label': 'Phụ lục A', 'width': '60%'})"""
    classes, kv = set(), {}
    for m in re.finditer(r'\.([\w-]+)|([\w-]+)=("([^"]*)"|\S+)', s):
        if m.group(1): classes.add(m.group(1))
        else: kv[m.group(2)] = m.group(4) if m.group(4) is not None else m.group(3)
    return classes, kv


def split_attrs(line):
    m = re.search(r'\s*\{([^{}]*)\}\s*$', line)
    if m and (('.' in m.group(1)) or '=' in m.group(1)):
        return line[:m.start()], *parse_attrs(m.group(1))
    return line, set(), {}


def parse_blocks(text):
    lines = text.replace('\r\n', '\n').split('\n')
    blocks, footnotes, i = [], {}, 0
    caption = None

    def is_special(l):
        s = l.strip()
        return (not s or s.startswith(('#', '>', '|', ':::', '![', '\\pagebreak', '<!--')) or re.match(r'^(\s*)([-*+]|\d+[.)])\s+', l)
                or re.match(r'^(Bảng|Table|Hình|Figure)\s*:', s) or re.match(r'^\[\^[^\]]+\]:', s))

    while i < len(lines):
        line = lines[i]; s = line.strip()
        if not s: i += 1; continue
        if s.startswith('<!--') and s != '<!-- pagebreak -->':   # comments (e.g. left by extract_docx.py) are skipped
            while i < len(lines) and '-->' not in lines[i]: i += 1
            i += 1; continue
        m = re.match(r'^\[\^([^\]]+)\]:\s*(.*)$', s)
        if m:
            footnotes[m.group(1)] = m.group(2); i += 1; continue
        if s == '\\pagebreak' or s == '<!-- pagebreak -->':
            blocks.append({'t': 'pagebreak'}); i += 1; continue
        m = re.match(r'^(#{1,3})\s+(.*)$', s)
        if m:
            txt, cls, kv = split_attrs(m.group(2))
            blocks.append({'t': 'h', 'level': len(m.group(1)), 'text': txt.strip(), 'cls': cls, 'kv': kv}); i += 1; continue
        m = re.match(r'^:::\s*(\w+)\s*$', s)
        if m:
            kind, body = m.group(1).lower(), []
            i += 1
            while i < len(lines) and lines[i].strip() != ':::':
                body.append(lines[i]); i += 1
            i += 1
            paras = [' '.join(p.split('\n')).strip() for p in '\n'.join(body).split('\n\n') if p.strip()]
            if kind == 'figures':
                items = [(l.split('|', 1) + [''])[:2] for l in body if l.strip()]
                blocks.append({'t': 'figures', 'items': [(a.strip(), b.strip()) for a, b in items]})
            else:
                blocks.append({'t': kind, 'paras': paras})
            continue
        if s.startswith('>'):
            body = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                body.append(lines[i].strip()[1:].strip()); i += 1
            attrib = None
            j = i
            while j < len(lines) and not lines[j].strip(): j += 1
            if j < len(lines) and re.match(r'^(—|--)\s+', lines[j].strip()):
                attrib = re.sub(r'^(—|--)\s+', '', lines[j].strip()); i = j + 1
            blocks.append({'t': 'quote', 'text': ' '.join(body), 'attrib': attrib}); continue
        m = re.match(r'^(Bảng|Table|Hình|Figure)\s*:\s*(.*)$', s)
        if m:
            caption = (m.group(1) in ('Hình', 'Figure'),) + split_attrs(m.group(2)); i += 1; continue
        if s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                r = lines[i].strip().strip('|')
                cells = [c.strip() for c in re.split(r'(?<!\\)\|', r)]
                if not all(re.match(r'^:?-{2,}:?$', c) for c in cells if c):
                    rows.append([c.replace('\\|', '|') for c in cells])
                i += 1
            is_fig, cap, cls, kv = caption if caption else (False, '', set(), {})
            blocks.append({'t': 'table', 'rows': rows, 'caption': cap.strip(), 'as_figure': is_fig, 'cls': cls, 'kv': kv})
            caption = None; continue
        m = re.match(r'^!\[([^\]]*)\]\(([^)\s]+)\)(\{[^}]*\})?\s*$', s)
        if m:
            cls, kv = parse_attrs(m.group(3) or '')
            blocks.append({'t': 'image', 'caption': m.group(1).strip(), 'path': m.group(2), 'cls': cls, 'kv': kv}); i += 1; continue
        if re.match(r'^(\s*)([-*+]|\d+[.)])\s+', line):
            items = []
            while i < len(lines) and lines[i].strip():
                m = re.match(r'^(\s*)([-*+]|\d+[.)])\s+(.*)$', lines[i])
                if m:
                    level = min(len(m.group(1).replace('\t', '    ')) // 2, 2)
                    items.append({'level': level, 'ordered': m.group(2)[0].isdigit(), 'text': m.group(3).strip()})
                elif items:
                    items[-1]['text'] += ' ' + lines[i].strip()
                i += 1
            blocks.append({'t': 'list', 'items': items}); continue
        para = [s]; i += 1
        while i < len(lines) and not is_special(lines[i]):
            para.append(lines[i].strip()); i += 1
        blocks.append({'t': 'p', 'text': ' '.join(para)})
    return blocks, footnotes

# ---------------------------------------------------------------- document builder

class Builder:
    def __init__(self, files, base_dir, footnotes):
        self.files, self.base_dir, self.fn_text = files, base_dir, footnotes
        self.rels = etree.fromstring(files['word/_rels/document.xml.rels'])
        self.fn_tree = etree.fromstring(files['word/footnotes.xml'])
        self.ct = etree.fromstring(files['[Content_Types].xml'])
        self.num_tree = etree.fromstring(files['word/numbering.xml'])
        self.fn_ids, self.next_fn = {}, 1
        self.doc_pr = 100
        self.n_table = self.n_figure = self.n_chapter = 0
        self.media = 0
        self.warnings = []

    # relationships / parts
    def add_rel(self, rtype, target, external=False):
        ids = {e.get('Id') for e in self.rels}
        k = 1
        while f'rIdVcci{k}' in ids: k += 1
        rid = f'rIdVcci{k}'
        el = etree.SubElement(self.rels, '{%s}Relationship' % NS['rel'], Id=rid, Type=rtype, Target=target)
        if external: el.set('TargetMode', 'External')
        return rid

    def add_image(self, path):
        from PIL import Image
        full = path if os.path.isabs(path) else os.path.join(self.base_dir, path)
        if not os.path.exists(full):
            self.warnings.append(f'Image not found: {path}'); return None
        ext = os.path.splitext(full)[1].lower().lstrip('.')
        if ext == 'jpeg': ext = 'jpg'
        if ext not in ('png', 'jpg', 'gif', 'bmp'):
            self.warnings.append(f'Unsupported image type: {path}'); return None
        self.media += 1
        name = f'media/vcci_img{self.media}.{ext}'
        self.files['word/' + name] = open(full, 'rb').read()
        if not any(e.get('Extension', '').lower() == ext for e in self.ct):
            mime = {'jpg': 'image/jpeg'}.get(ext, 'image/' + ext)
            self.ct.insert(0, etree.Element('{http://schemas.openxmlformats.org/package/2006/content-types}Default',
                                            Extension=ext, ContentType=mime))
        with Image.open(full) as im:
            w, h = im.size; dpi = im.info.get('dpi', (96, 96))[0] or 96
        return self.add_rel(REL_IMAGE, name), w / dpi * 914400, h / dpi * 914400

    def new_numbered_list(self):
        ids = [int(n.get(W + 'numId')) for n in self.num_tree.findall(W + 'num')]
        nid = str(max(ids) + 1)
        self.num_tree.append(frag(f'<w:num w:numId="{nid}"><w:abstractNumId w:val="{NUMBERED_ABSTRACT}"/>'
                                  f'<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>')[0])
        return nid

    def footnote(self, key):
        if key in self.fn_ids: return self.fn_ids[key]
        if key not in self.fn_text:
            self.warnings.append(f'Footnote [^{key}] has no definition'); return None
        fid = str(self.next_fn); self.next_fn += 1; self.fn_ids[key] = fid
        p = frag(f'<w:footnote w:id="{fid}"><w:p><w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>'
                 '<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>'
                 '<w:r><w:t xml:space="preserve"> </w:t></w:r></w:p></w:footnote>')[0]
        para = p.find(W + 'p')
        for r in self.runs(self.fn_text[key]): para.append(r)
        self.fn_tree.append(p)
        return fid

    # inline markup -> runs
    def runs(self, text, rpr=''):
        out = []
        pat = re.compile(r'(\*\*\*.+?\*\*\*|\*\*.+?\*\*|__.+?__|(?<!\w)\*(?!\s).+?(?<!\s)\*|(?<!\w)_(?!\s).+?(?<!\s)_(?!\w)|\[\^[^\]]+\]|\[[^\]]+\]\([^)\s]+\)|`[^`]+`)')
        pos = 0
        for m in pat.finditer(text):
            if m.start() > pos: out.append(self.run(text[pos:m.start()], rpr))
            tok = m.group(0)
            if tok.startswith('***'): out.extend(self.runs(tok[3:-3], rpr + '<w:b/><w:i/>'))
            elif tok.startswith(('**', '__')): out.extend(self.runs(tok[2:-2], rpr + '<w:b/>'))
            elif tok.startswith(('*', '_')): out.extend(self.runs(tok[1:-1], rpr + '<w:i/>'))
            elif tok.startswith('`'): out.append(self.run(tok[1:-1], rpr))
            elif tok.startswith('[^'):
                fid = self.footnote(tok[2:-1])
                if fid: out.append(frag(f'<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="{fid}"/></w:r>')[0])
            else:
                lm = re.match(r'\[([^\]]+)\]\(([^)\s]+)\)', tok)
                rid = self.add_rel(REL_LINK, lm.group(2), external=True)
                h = frag(f'<w:hyperlink r:id="{rid}" w:history="1"/>')[0]
                for r in self.runs(lm.group(1), rpr + '<w:rStyle w:val="Hyperlink"/>'): h.append(r)
                out.append(h)
            pos = m.end()
        if pos < len(text): out.append(self.run(text[pos:], rpr))
        return out

    def run(self, text, rpr=''):
        # rStyle must come first inside rPr
        rs = re.findall(r'<w:rStyle[^>]*/>', rpr); rest = re.sub(r'<w:rStyle[^>]*/>', '', rpr)
        r = frag(f'<w:r>{"<w:rPr>" + "".join(rs) + rest + "</w:rPr>" if rpr else ""}<w:t xml:space="preserve"></w:t></w:r>')[0]
        r.find(W + 't').text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)   # XML-illegal control characters
        return r

    def para(self, text='', style=None, ppr_extra='', rpr=''):
        ppr = (f'<w:pStyle w:val="{style}"/>' if style else '') + ppr_extra
        p = frag(f'<w:p>{"<w:pPr>" + ppr + "</w:pPr>" if ppr else ""}</w:p>')[0]
        for r in self.runs(text, rpr): p.append(r)
        return p

    def page_break(self):
        return frag('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')[0]

    def picture(self, rid, cx, cy, name):
        self.doc_pr += 1
        return frag(f'<w:r><w:rPr><w:noProof/></w:rPr><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
                    f'<wp:extent cx="{int(cx)}" cy="{int(cy)}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
                    f'<wp:docPr id="{self.doc_pr}" name="{name}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
                    '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>'
                    f'<pic:nvPicPr><pic:cNvPr id="0" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
                    f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
                    f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{int(cx)}" cy="{int(cy)}"/></a:xfrm>'
                    '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
                    '</wp:inline></w:drawing></w:r>')[0]

    # blocks
    def table(self, b):
        rows = [r for r in b['rows'] if r]
        if not rows: return []
        cls = b['cls']
        ncol = max(len(r) for r in rows)
        rows = [r + [''] * (ncol - len(r)) for r in rows]
        style = 'VCCITableLight' if 'light' in cls else 'VCCITable'
        header = 'noheader' not in cls
        body = rows[1:] if header else rows
        numeric = [bool(body) and all(NUMERIC.match(r[c]) or r[c] in ('', '<<') for r in body) and any(NUMERIC.match(r[c]) for r in body)
                   for c in range(ncol)]
        # column widths: proportional to the longest cell (clamped), numbers stay narrow
        lens = [max(4, min(40, max((len(r[c]) for r in rows if c + 1 >= ncol or r[c + 1].strip() != '<<'), default=4))) for c in range(ncol)]
        if b['kv'].get('widths'):   # {widths=3,1,1}
            given = [float(x) for x in b['kv']['widths'].split(',')][:ncol]
            lens = given + lens[len(given):]
        tot = sum(lens); widths = [int(TEXT_WIDTH * l / tot) for l in lens]; widths[-1] += TEXT_WIDTH - sum(widths)
        first_col = 'light' in cls or 'firstcol' in cls
        total = 'total' in cls
        banded = 'banded' in cls
        look = (0x20 if header else 0) | (0x40 if total else 0) | (0x80 if first_col else 0) | (0 if banded else 0x200) | 0x400
        t = frag(f'<w:tbl><w:tblPr><w:tblStyle w:val="{style}"/><w:tblW w:w="{TEXT_WIDTH}" w:type="dxa"/>'
                 f'<w:tblInd w:w="0" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
                 f'<w:tblLook w:val="{look:04X}" w:firstRow="{int(header)}" w:lastRow="{int(total)}" w:firstColumn="{int(first_col)}" '
                 f'w:lastColumn="0" w:noHBand="{int(not banded)}" w:noVBand="1"/></w:tblPr><w:tblGrid>'
                 + ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid></w:tbl>')[0]
        for ri, r in enumerate(rows):
            if header and ri == 0:   # header row is styled by the table style; drop manual bold
                r = [re.sub(r'^\*\*(.*)\*\*$', r'\1', c.strip()) for c in r]
            tr = frag('<w:tr>' + ('<w:trPr><w:tblHeader/></w:trPr>' if header and ri == 0 else '<w:trPr><w:cantSplit/></w:trPr>') + '</w:tr>')[0]
            c = 0
            while c < ncol:   # a cell containing only "<<" merges into the cell on its left
                span = 1
                while c + span < ncol and r[c + span].strip() == '<<': span += 1
                w = sum(widths[c:c + span])
                tc = frag(f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>'
                          + (f'<w:gridSpan w:val="{span}"/>' if span > 1 else '') + '</w:tcPr></w:tc>')[0]
                for part in re.split(r'<br\s*/?>', r[c]) or ['']:
                    tc.append(self.para(part.strip(), ppr_extra='<w:jc w:val="right"/>' if numeric[c] and span == 1 else ''))
                tr.append(tc); c += span
            t.append(tr)
        out = []
        if b['caption']:
            if b.get('as_figure'): self.n_figure += 1; label = f'Hình {self.n_figure}'
            else: self.n_table += 1; label = f'Bảng {self.n_table}'
            out.append(self.para(f'{label}.  {b["caption"]}', 'Caption', '<w:keepNext/><w:spacing w:before="200" w:after="80"/>'))
        out.append(t)
        out.append(frag('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')[0])
        return out

    def figures(self, b):
        items = b['items'][:4]
        if not items: return []
        n = len(items); widths = [TEXT_WIDTH // n] * n; widths[-1] += TEXT_WIDTH - sum(widths)
        t = frag(f'<w:tbl><w:tblPr><w:tblStyle w:val="VCCITableTint"/><w:tblW w:w="{TEXT_WIDTH}" w:type="dxa"/>'
                 '<w:tblInd w:w="0" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
                 '<w:tblLook w:val="0600" w:firstRow="0" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="1" w:noVBand="1"/>'
                 '</w:tblPr><w:tblGrid>' + ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid><w:tr/></w:tbl>')[0]
        tr = t.find(W + 'tr')
        for (val, label), w in zip(items, widths):
            tc = frag(f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/></w:tcPr></w:tc>')[0]
            tc.append(self.para(val, 'VCCIFigureNumber')); tc.append(self.para(label, 'VCCISmall'))
            tr.append(tc)
        if len(b['items']) > 4: self.warnings.append('::: figures shows at most 4 items; extra items dropped')
        return [t, frag('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')[0]]

    def image(self, b):
        got = self.add_image(b['path'])
        if not got: return []
        rid, cx, cy = got
        maxw = TEXT_WIDTH * EMU_PER_TWIP
        if 'width' in b['kv'] and b['kv']['width'].endswith('%'):
            target = maxw * float(b['kv']['width'][:-1]) / 100
        else:
            target = min(cx, maxw) if 'natural' in b['cls'] else maxw
        cy, cx = cy * target / cx, target
        p = frag('<w:p><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="80"/></w:pPr></w:p>')[0]
        p.append(self.picture(rid, cx, cy, os.path.basename(b['path'])))
        out = [p]
        if b['caption']:
            self.n_figure += 1
            out.append(self.para(f'Hình {self.n_figure}.  {b["caption"]}', 'Caption', '<w:spacing w:after="240"/>'))
        return out

    def build(self, blocks, protos, chapter_break=True):
        out, first_h1 = [], True
        for b in blocks:
            t = b['t']
            if t == 'h' and b['level'] == 1:
                if not first_h1 and chapter_break: out.append(self.page_break())
                first_h1 = False
                if 'nolabel' not in b['cls']:
                    if 'label' in b['kv']: label = b['kv']['label']
                    else: self.n_chapter += 1; label = f'Chương {self.n_chapter:02d}'
                    out.append(self.para(label, 'VCCILabel', '<w:keepNext/>'))
                out.append(self.para(b['text'], 'Heading1'))
                out.append(copy.deepcopy(protos['rule']))
            elif t == 'h':
                out.append(self.para(b['text'], f'Heading{b["level"]}'))
            elif t == 'p': out.append(self.para(b['text']))
            elif t == 'lead':
                out += [self.para(x, 'VCCILead') for x in b['paras']]
            elif t == 'callout':
                out += [self.para(x, 'VCCICallout') for x in b['paras']]
            elif t == 'small':
                out += [self.para(x, 'VCCISmall') for x in b['paras']]
            elif t == 'note':      # source / note line under a table or figure
                if out and out[-1].tag == W + 'p' and not ''.join(out[-1].itertext()).strip() and out[-1].find('.//' + W + 'drawing') is None:
                    out.pop()       # replace the spacer paragraph after a table
                out += [self.para(x, 'Caption', '<w:spacing w:before="60" w:after="240"/>') for x in b['paras']]
            elif t == 'references':
                out += [self.para(x, None, '<w:spacing w:after="120"/><w:ind w:left="425" w:hanging="425"/>',
                                  '<w:sz w:val="18"/><w:szCs w:val="18"/>') for x in b['paras']]
            elif t == 'quote':
                out.append(self.para(f'“{b["text"].strip(chr(34) + "“”")}”', 'Quote'))
                if b['attrib']:
                    out.append(self.para(f'— {b["attrib"]}', None, '<w:spacing w:after="280"/>',
                                         '<w:color w:val="5C6478"/><w:sz w:val="17"/><w:szCs w:val="17"/>'))
            elif t == 'list':
                num = None
                for it in b['items']:
                    if it['ordered']:
                        if it['level'] == 0 and num is None: num = self.new_numbered_list()
                        nid = num or self.new_numbered_list()
                    else: nid = BULLET_NUM
                    out.append(self.para(it['text'], 'ListParagraph',
                                         f'<w:numPr><w:ilvl w:val="{it["level"]}"/><w:numId w:val="{nid}"/></w:numPr>'))
            elif t == 'table': out += self.table(b)
            elif t == 'figures': out += self.figures(b)
            elif t == 'image': out += self.image(b)
            elif t == 'pagebreak': out.append(self.page_break())
            else:
                self.warnings.append(f'Unknown block ::: {t}; rendered as body text')
                out += [self.para(x) for x in b.get('paras', [])]
        return out

# ---------------------------------------------------------------- template surgery

def set_text(p, text):
    ts = list(p.iter(W + 't'))
    if not ts: return
    ts[0].text = text; ts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    for t in ts[1:]: t.text = ''


def hero_icon(spec):
    """'21', 'research-index' or 'VCCI_Hero_21_research-index' -> Gold-on-dark 512 px PNG of that hero icon."""
    folder = os.path.join(os.path.dirname(template_path('x')), '..', '..', '05_Icons', 'Hero', 'PNG', 'Gold-on-dark')
    key = spec.strip().lower()
    for f in sorted(os.listdir(folder)):
        m = re.match(r'VCCI_Hero_(\d\d)_(.+)_512px\.png$', f)
        if m and key in (m.group(1), m.group(1).lstrip('0'), m.group(2), f'vcci_hero_{m.group(1)}_{m.group(2)}'):
            return os.path.join(folder, f)
    return None


def set_cover_icon(files, doc, cover_elements, spec):
    """Swap the square hero icon on the front cover; icon: none removes it."""
    from PIL import Image
    import io
    rels = {e.get('Id'): e.get('Target') for e in etree.fromstring(files['word/_rels/document.xml.rels'])}
    for el in cover_elements:
        for blip in el.iter('{%s}blip' % NS['a']):
            name = 'word/' + rels.get(blip.get(R + 'embed'), '')
            if name not in files: continue
            w, h = Image.open(io.BytesIO(files[name])).size
            if w != h: continue                       # backgrounds and logo are not square
            if spec.strip().lower() in ('none', 'false', 'no'):
                drawing = next(a for a in blip.iterancestors() if a.tag == W + 'drawing')
                drawing.getparent().remove(drawing)
                return
            path = hero_icon(spec)
            if not path:
                raise SystemExit(f'Unknown icon "{spec}". Use a number 1-24 or a slug from brand-assets/05_Icons/Hero.')
            files[name] = open(path, 'rb').read()
            return


def render(md_path, out_path, template=None):
    text = open(md_path, encoding='utf-8-sig').read()
    meta, body = parse_front_matter(text)
    blocks, fns = parse_blocks(body)
    files = read_package(template or template_path('VCCI_Report.dotx'))
    doc = etree.fromstring(files['word/document.xml'])
    bd = doc.find(W + 'body')
    kids = list(bd)

    def style_of(el):
        s = el.find(f'{W}pPr/{W}pStyle')
        return s.get(W + 'val') if s is not None else None

    # locate template landmarks
    title_p = next(e for e in kids if style_of(e) == 'Title')
    sub_p = next(e for e in kids if style_of(e) == 'Subtitle')
    label_p = kids[kids.index(title_p) - 1]
    cover_tbl = next(e for e in kids if e.tag == W + 'tbl')
    sect_breaks = [e for e in kids if e.tag == W + 'p' and e.find(f'{W}pPr/{W}sectPr') is not None]
    toc_sdt = next(e for e in kids if e.tag == W + 'sdt')
    body_start = kids.index(toc_sdt) + 2          # skip the page break after the TOC
    body_end = kids.index(sect_breaks[1])         # section break before the back cover
    rule = next(e for e in kids[body_start:body_end] if e.find('.//' + W + 'drawing') is not None)
    protos = {'rule': copy.deepcopy(rule)}

    m = re.search(r'(19|20)\d\d', meta.get('date', ''))
    year = meta.get('year') or (m.group(0) if m else '')
    set_text(label_p, meta.get('label', 'Báo cáo  ·  Report' + (f'  ·  {year}' if year else '')))
    set_text(title_p, meta.get('title', 'Báo cáo'))
    if meta.get('subtitle'): set_text(sub_p, meta['subtitle'])
    else: bd.remove(sub_p)
    cps = [p for p in cover_tbl.iter(W + 'p') if ''.join(t.text or '' for t in p.iter(W + 't')).strip()]
    if cps: set_text(cps[0], meta.get('date', ''))
    if len(cps) > 1:
        parts = [meta.get('author'), meta.get('unit'), 'Liên đoàn Thương mại và Công nghiệp Việt Nam']
        set_text(cps[1], '  ·  '.join(x for x in parts if x))
    if meta.get('toc', 'true').lower() in ('false', 'no', '0'):
        for e in kids[kids.index(sect_breaks[0]) + 1:body_start]: bd.remove(e)

    if meta.get('icon'): set_cover_icon(files, doc, kids[:kids.index(sect_breaks[0])], meta['icon'])

    # back cover: contact line from front matter, or removed
    for p in list(bd.iter(W + 'p')):
        if ''.join(t.text or '' for t in p.iter(W + 't')).startswith('[Đầu mối liên hệ'):
            if meta.get('contact'): set_text(p, meta['contact'])
            else: p.getparent().remove(p)

    for e in kids[body_start:body_end]: bd.remove(e)
    b = Builder(files, os.path.dirname(os.path.abspath(md_path)), fns)
    new = b.build(blocks, protos, meta.get('chapter_break', 'true').lower() not in ('false', 'no', '0'))
    anchor = sect_breaks[1]
    for el in new: anchor.addprevious(el)

    # running header in the body section
    short = meta.get('header') or meta.get('title', '')
    for name in [n for n in files if re.match(r'word/header\d+\.xml$', n)]:
        h = etree.fromstring(files[name])
        ps = [p for p in h.iter(W + 'p') if '[Tên báo cáo' in ''.join(t.text or '' for t in p.iter(W + 't'))]
        for p in ps: set_text(p, f'{short}  ·  {year}' if year else short)
        if ps: files[name] = xml_bytes(h)

    # unique ids for any drawings we cloned
    for i, dp in enumerate(doc.iter('{%s}docPr' % NS['wp'])): dp.set('id', str(200 + i))

    files['word/document.xml'] = xml_bytes(doc)
    files['word/_rels/document.xml.rels'] = xml_bytes(b.rels)
    files['word/footnotes.xml'] = xml_bytes(b.fn_tree)
    files['word/numbering.xml'] = xml_bytes(b.num_tree)
    ct = xml_bytes(b.ct).decode('utf-8').replace(TEMPLATE_CT, DOC_CT)
    files['[Content_Types].xml'] = ct.encode('utf-8')
    st = files['word/settings.xml'].decode('utf-8')
    if '<w:updateFields' not in st:          # Word refreshes the TOC on open; finalize.py does it silently instead
        m = re.search(r'<w:(hdrShapeDefaults|footnotePr|endnotePr|compat|docVars|rsids)[ />]', st)
        st = st[:m.start()] + '<w:updateFields w:val="true"/>' + st[m.start():]
    files['word/settings.xml'] = st.encode('utf-8')
    core = files.get('docProps/core.xml')
    if core:
        c = core.decode('utf-8')
        c = re.sub(r'<dc:title>.*?</dc:title>|<dc:title/>', '', c)
        c = c.replace('</cp:coreProperties>', f'<dc:title>{escape(meta.get("title", ""))}</dc:title></cp:coreProperties>')
        files['docProps/core.xml'] = c.encode('utf-8')
    write_package(files, out_path)
    return b.warnings, {'chapters': b.n_chapter, 'tables': b.n_table, 'figures': b.n_figure, 'footnotes': len(b.fn_ids)}


def escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('markdown')
    ap.add_argument('-o', '--out', help='output .docx (default: next to the Markdown file)')
    ap.add_argument('--template', help='override the report template (.dotx)')
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.markdown)[0] + '_VCCI.docx'
    warnings, stats = render(a.markdown, out, a.template)
    for w in warnings: print('WARNING:', w)
    print(f'Wrote {out}  ({stats["chapters"]} chapters, {stats["tables"]} tables, {stats["figures"]} figures, {stats["footnotes"]} footnotes)')


if __name__ == '__main__':
    main()
