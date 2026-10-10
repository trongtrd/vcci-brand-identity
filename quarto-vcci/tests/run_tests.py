"""Test the quarto-vcci extensions.  Run from the repository root:  python quarto-vcci/tests/run_tests.py [fixture ...]

Layers (docs/PLAN_QUARTO_VCCI.md, section 5); this file implements 1-4 (Word checks without Word):
  1 static   extensions are built from the current sources and brand tokens; _extension.yml files parse
  2 render   every fixture x format renders in a clean folder with system fonts ignored; any warning fails
  3 PDF      only brand fonts, all embedded; A4; page count in range; required Vietnamese text present;
             no word outside the page's safe area, no body word outside the side margins
  4 Word     only styles defined in the reference document; tables use the VCCI table style; no direct fonts; fonts embedded;
             then Microsoft Word opens the file and exports a PDF, which must use only brand fonts and show the required text
             (skipped with --no-word, when Word is not installed, or when Word has documents open: never automate a user's Word)
  5 visual   every PDF page matches the approved image in tests/baseline/ (run with --update-baseline after an approved change)
  6 install  `quarto add` installs the extension into an empty folder, as a user would; every template renders there
A fixture declares what to check in its front matter under `test:` (formats, pages, must-contain). The user templates
(quarto-vcci/templates/) carry no test key; their checks are in TEMPLATE_SPECS below.
Self-test (tests/selftest/): deliberately broken documents with `expect-fail: [check, ...]`; the run fails unless each
named check fails on them, which proves the checks catch the errors they are meant to catch.
Text is read from the word boxes of each page, so text pushed off a page counts as missing.
Results: quarto-vcci/tests/out/<fixture>/ (outputs, page images) and quarto-vcci/tests/out/summary.md.
"""
import glob, os, re, shutil, subprocess, sys, tempfile, unicodedata, zipfile
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
QV = os.path.dirname(HERE)
ROOT = os.path.dirname(QV)
OUT = os.path.join(HERE, 'out')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from env import PDFTOPPM
POPPLER = os.path.dirname(PDFTOPPM) if os.path.isabs(PDFTOPPM) else ''
tool = lambda name: os.path.join(POPPLER, name) if POPPLER else name

MM = 72 / 25.4
SIDE_MARGIN_MM = 22          # body text must stay inside the side margins (vcci-base default)
SAFE_EDGE_MM = 8             # nothing (header, footer, cover text) within 8 mm of the paper edge
# FontAwesome: Quarto's callout icons. NewCMMath: Typst's maths font (the brand fonts have no OpenType MATH table)
FONT_OK = re.compile(r'^(Lora|LoraItalic|BeVietnamPro|FontAwesome|NewCMMath)')
ANSI = re.compile(r'\x1b\[[0-9;]*m')   # Quarto colours its warnings
WARN = re.compile(r'^(WARN|WARNING|ERROR)\b|(^|\.\.\.)(warning|error): ')

# templates users receive: checked without a `test:` key in the file
TEMPLATE_SPECS = {
    'report': {'formats': ['vcci-report-typst', 'vcci-report-docx'], 'pages': [6, 12],
               'must-contain': ['Đánh giá chi phí tuân thủ thủ tục đầu tư', 'Ba khuyến nghị ưu tiên', 'Lộ trình đề xuất']},
    'memo': {'formats': ['vcci-memo-typst', 'vcci-memo-docx'], 'pages': [1, 2],
             'must-contain': ['Tờ trình', 'Gửi', 'Chủ tịch VCCI', 'Về việc', 'Góp ý dự thảo Nghị định',
                              'Trưởng Ban Pháp chế', 'Tài liệu kèm theo', 'Bảng tổng hợp ý kiến doanh nghiệp']},
    'wp': {'formats': ['vcci-wp-typst', 'vcci-wp-docx'], 'pages': [2, 5],
           'must-contain': ['VCCI Working Paper số 2026/01', 'Từ khóa', 'Keywords', 'Mã JEL: D22, H11, K23, O17',
                            'Trích dẫn đề nghị', 'không nhất thiết phản ánh quan điểm', 'Bảng 2', 'Tài liệu tham khảo']},
}

results = []   # (fixture, format, check, ok, detail)
QUIET = [False]
def record(fx, fmt, check, ok, detail=''):
    results.append((fx, fmt, check, ok, detail))
    if not QUIET[0]: print(f'  [{"PASS" if ok else "FAIL"}] {fmt or "-"} · {check}{": " + detail if detail and not ok else ""}', flush=True)

def run(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')

def norm(s):
    # case-insensitive: labels are set in capitals by their style ("TÓM TẮT"), the words are the same
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', s)).strip().casefold()

# ---------------------------------------------------------------- layer 1
def layer1():
    r = run([sys.executable, os.path.join(QV, 'build.py'), '--check'])
    record('static', None, 'extensions match sources and brand tokens (build.py --check)', r.returncode == 0, r.stdout.strip())
    for y in glob.glob(os.path.join(QV, '_extensions', 'vcci', '*', '_extension.yml')):
        try:
            d = yaml.safe_load(open(y, encoding='utf-8'))
            ok = bool(d['contributes']['formats'].get('typst')) and bool(d['contributes']['formats'].get('docx'))
            record('static', None, f'{os.path.basename(os.path.dirname(y))}/_extension.yml has typst and docx formats', ok)
        except Exception as e:
            record('static', None, f'{y} parses', False, str(e))

# ---------------------------------------------------------------- layer 2-4 per fixture
def pdf_checks(fx, fmt, pdf, spec, outdir):
    fonts = run([tool('pdffonts'), pdf]).stdout.splitlines()[2:]
    names = [l.split()[0].split('+')[-1] for l in fonts if l.strip()]
    bad = [n for n in names if not FONT_OK.match(n)]
    not_emb = [l.split()[0] for l in fonts if l.strip() and ' no ' in l[50:70]]
    record(fx, fmt, 'only brand fonts', not bad, ', '.join(bad))
    record(fx, fmt, 'all fonts embedded', not not_emb, ', '.join(not_emb))
    info = run([tool('pdfinfo'), pdf]).stdout
    size = re.search(r'Page size:\s+([\d.]+) x ([\d.]+)', info)
    pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    record(fx, fmt, 'A4 paper', bool(size) and abs(float(size.group(1)) - 595.28) < 1 and abs(float(size.group(2)) - 841.89) < 1,
           size.group(0) if size else 'no size')
    lo, hi = spec.get('pages', [1, 999])
    record(fx, fmt, f'page count {lo}-{hi}', lo <= pages <= hi, f'{pages} pages')
    # word boxes of what is visible on the page (text pushed off the page has no box)
    bbox = os.path.join(outdir, 'bbox.html')
    run([tool('pdftotext'), '-enc', 'UTF-8', '-bbox', pdf, bbox])
    html = open(bbox, encoding='utf-8').read()
    unesc = lambda t: t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
    pages_words = []
    for w, h, body in re.findall(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', html, re.S):
        words = [(float(a), float(b), float(c), float(d), unesc(t)) for a, b, c, d, t in
                 re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', body)]
        pages_words.append((float(w), float(h), words))
    visible = norm(' '.join(t for _, _, words in pages_words for *_, t in words))
    # compared without spaces: pdftotext splits letter-spaced labels ("A B ST R ACT") into several words
    missing = [s for s in spec.get('must-contain', []) if norm(s).replace(' ', '') not in visible.replace(' ', '')]
    record(fx, fmt, 'no broken characters (U+FFFD)', '\ufffd' not in visible)
    record(fx, fmt, 'required Vietnamese text present and visible', not missing, ' | '.join(missing))
    edge, side, overlap = [], [], []
    for pno, (w, h, words) in enumerate(pages_words, 1):
        for x0, y0, x1, y1, word in words:
            if x0 < SAFE_EDGE_MM * MM or y0 < SAFE_EDGE_MM * MM or x1 > w - SAFE_EDGE_MM * MM or y1 > h - SAFE_EDGE_MM * MM:
                edge.append(f'p{pno} "{word}"')
            if x0 < SIDE_MARGIN_MM * MM - 1 or x1 > w - SIDE_MARGIN_MM * MM + 1:
                side.append(f'p{pno} "{word}" x={x0:.0f}-{x1:.0f}')
        # colliding words: two boxes sharing more than 30% of the smaller one. The status mark ("BẢN THẢO") is
        # deliberately behind the text and is set very large, so words taller than 30 pt are left out.
        body = [b for b in words if b[3] - b[1] < 30]
        for a in range(len(body)):
            ax0, ay0, ax1, ay1, at = body[a]
            for b in range(a + 1, len(body)):
                bx0, by0, bx1, by1, bt = body[b]
                ix, iy = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
                if ix > 0 and iy > 0:
                    small = min((ax1 - ax0) * (ay1 - ay0), (bx1 - bx0) * (by1 - by0))
                    if small > 0 and ix * iy > 0.3 * small:
                        overlap.append(f'p{pno} "{at}"/"{bt}"')
    record(fx, fmt, f'no text within {SAFE_EDGE_MM} mm of the paper edge', not edge, ', '.join(edge[:5]))
    record(fx, fmt, f'no text outside the {SIDE_MARGIN_MM} mm side margins', not side, ', '.join(side[:5]))
    record(fx, fmt, 'no overlapping text', not overlap, ', '.join(overlap[:5]))
    run([PDFTOPPM, '-png', '-r', '50', pdf, os.path.join(outdir, 'page')])

WORD_COM = os.path.join(ROOT, 'tools', 'word', 'word_com.ps1')

BASELINE = os.path.join(HERE, 'baseline')
# Typst renders identically every time, so an unchanged page differs by exactly 0. A page fails when any 32 x 32 px
# tile (about 16 mm at 50 dpi) differs by more than TILE_LIMIT grey levels on average: one changed word is enough.
TILE, TILE_LIMIT = 32, 4.0

def page_diff(a, b):
    """Largest mean grey-level difference over the page's tiles (0-255), and the difference image."""
    import numpy
    from PIL import Image, ImageChops
    ia, ib = Image.open(a).convert('L'), Image.open(b).convert('L')
    if ia.size != ib.size: return 255.0, None
    d = ImageChops.difference(ia, ib)
    arr = numpy.asarray(d, dtype=float)
    h, w = arr.shape
    worst = max(arr[y:y + TILE, x:x + TILE].mean() for y in range(0, h, TILE) for x in range(0, w, TILE))
    return worst, d

def visual_checks(fx, fmt, outdir):
    pages = sorted(glob.glob(os.path.join(outdir, 'page-*.png')), key=lambda f: int(f.rsplit('-', 1)[1][:-4]))
    base = os.path.join(BASELINE, fx, fmt)
    if '--update-baseline' in sys.argv:
        os.makedirs(base, exist_ok=True)
        for old in glob.glob(os.path.join(base, '*.png')): os.remove(old)
        for f in pages: shutil.copy(f, base)
        print(f'  [BASE] {fmt} · baseline updated ({len(pages)} pages)')
        return
    ref = sorted(glob.glob(os.path.join(base, 'page-*.png')), key=lambda f: int(f.rsplit('-', 1)[1][:-4]))
    if not ref:
        print(f'  [SKIP] {fmt} · no approved baseline yet')
        return
    record(fx, fmt, 'same page count as the approved version', len(ref) == len(pages), f'{len(pages)} pages, approved {len(ref)}')
    changed = []
    for r_, p_ in zip(ref, pages):
        score, d = page_diff(r_, p_)
        if score > TILE_LIMIT:
            changed.append(f'{os.path.basename(p_)} ({score:.1f})')
            if d is not None: d.point(lambda v: 255 - min(255, v * 4)).save(p_.replace('page-', 'diff-'))
    record(fx, fmt, 'pages look like the approved version', not changed, ', '.join(changed[:5]))

def word_state():
    """'ok', or why Word must not be used now."""
    if '--no-word' in sys.argv: return 'skipped (--no-word)'
    if sys.platform != 'win32': return 'skipped (needs Windows)'
    r = run(['powershell', '-NoProfile', '-Command', "Get-Process WINWORD -ErrorAction SilentlyContinue | "
             "ForEach-Object { $_.MainWindowTitle }"])
    if any(t.strip() for t in r.stdout.splitlines()): return 'skipped (Word has documents open)'
    r = run(['powershell', '-NoProfile', '-Command', "[bool](Get-Item 'Registry::HKEY_CLASSES_ROOT\\Word.Application' -ErrorAction SilentlyContinue)"])
    return 'ok' if 'True' in r.stdout else 'skipped (Word not installed)'

def word_checks(fx, fmt, docx, spec, outdir):
    state = word_state()
    if state != 'ok':
        print(f'  [SKIP] {fmt} · Word: {state}')
        return
    pdf = os.path.join(outdir, f'{fx}-word.pdf')
    if os.path.exists(pdf): os.remove(pdf)
    run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', WORD_COM, '-Mode', 'pdf', '-InFile', docx, '-OutFile', pdf])
    ok = os.path.exists(pdf)
    record(fx, fmt, 'Word opens the file and exports PDF', ok)
    if not ok: return
    size = re.search(r'Page size:\s+([\d.]+) x ([\d.]+)', run([tool('pdfinfo'), pdf]).stdout)
    record(fx, fmt, 'Word PDF is A4', bool(size) and abs(float(size.group(1)) - 595.3) < 1.5 and abs(float(size.group(2)) - 841.9) < 1.5,
           size.group(0) if size else 'no size')
    # Word sets list bullets in Symbol (and the space after them in Arial): allowed for those marks only, never for text.
    # Cambria Math: Word's equation font (the brand fonts have no OpenType MATH table)
    import pymupdf
    bad = set()
    for page in pymupdf.open(pdf):
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    font = span['font'].split('+')[-1].replace(' ', '')
                    if not re.match(r'^(Lora|BeVietnam|CambriaMath)', font) and span['text'].strip(' •·◦▪	-'):
                        bad.add(f'{font}: "{span["text"][:20]}"')
    record(fx, fmt, 'Word PDF sets all text in brand fonts', not bad, ', '.join(sorted(bad)[:5]))
    txt = os.path.join(outdir, 'word-text.txt')
    run([tool('pdftotext'), '-enc', 'UTF-8', pdf, txt])
    text = norm(open(txt, encoding='utf-8').read())
    missing = [s for s in spec.get('must-contain', []) if norm(s) not in text]
    record(fx, fmt, 'Word PDF shows the required text', not missing, ' | '.join(missing))
    run([PDFTOPPM, '-png', '-r', '50', pdf, os.path.join(outdir, 'word-page')])

def docx_checks(fx, fmt, docx, spec, ext_dir):
    z = zipfile.ZipFile(docx)
    doc = z.read('word/document.xml').decode('utf-8')
    defined = set(re.findall(r'w:styleId="([^"]+)"', z.read('word/styles.xml').decode('utf-8')))
    ref = zipfile.ZipFile(os.path.join(ext_dir, 'vcci-reference.docx'))
    ref_styles = set(re.findall(r'w:styleId="([^"]+)"', ref.read('word/styles.xml').decode('utf-8')))
    used = set(re.findall(r'w:(?:pStyle|rStyle) w:val="([^"]+)"', doc))
    # every style a paragraph or run refers to must be defined (Word silently falls back to Normal otherwise),
    # and every VCCI style used must come from the reference document
    undefined = sorted(used - defined)
    foreign_vcci = sorted(s for s in used if s.startswith('VCCI') and s not in ref_styles)
    record(fx, fmt, 'every paragraph/character style is defined', not undefined, ', '.join(undefined))
    record(fx, fmt, 'VCCI styles come from the reference document', not foreign_vcci, ', '.join(foreign_vcci))
    sizes = set(re.findall(r'<w:pgSz [^>]*/>', doc))
    a4 = all(re.search(r'w:w="11906"', x) and re.search(r'w:h="16838"', x) for x in sizes) and sizes
    record(fx, fmt, 'A4 paper (210 x 297 mm) in every section', bool(a4), ', '.join(sizes))
    tbl = re.findall(r'w:tblStyle w:val="([^"]+)"', doc)
    record(fx, fmt, 'tables use the VCCI table style', all(t == 'Table' for t in tbl), ', '.join(sorted(set(tbl))))
    fonts = sorted(set(re.findall(r'w:rFonts [^>]*w:ascii="([^"]+)"', doc)) - {'Lora', 'Lora Medium', 'Lora SemiBold', 'Be Vietnam Pro',
                                                                           'Be Vietnam Pro Medium', 'Be Vietnam Pro SemiBold'})
    record(fx, fmt, 'no direct fonts outside the brand', not fonts, ', '.join(fonts))
    record(fx, fmt, 'fonts embedded', any(n.startswith('word/fonts/') for n in z.namelist()))
    parts = [doc] + [z.read(n).decode('utf-8') for n in ('word/footnotes.xml', 'word/endnotes.xml') if n in z.namelist()]
    plain = norm(''.join(t for p in parts for t in re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)))
    record(fx, fmt, 'no broken characters (U+FFFD)', '\ufffd' not in plain)   # e.g. a byte-wise string.upper in Lua
    missing = [s for s in spec.get('must-contain', []) if norm(s).replace(' ', '') not in plain.replace(' ', '')]
    record(fx, fmt, 'required Vietnamese text present', not missing, ' | '.join(missing))

def test_fixture(path, spec=None):
    fx = os.path.splitext(os.path.basename(path))[0]
    src = open(path, encoding='utf-8').read()
    if spec is None: spec = yaml.safe_load(src.split('---')[1]).get('test', {})
    if not QUIET[0]: print(f'\n{fx}', flush=True)
    outdir = os.path.join(OUT, fx)
    os.makedirs(outdir, exist_ok=True)
    for fmt in spec.get('formats', []):
        with tempfile.TemporaryDirectory() as tmp:
            # a clean folder, as a user gets it: the extension, the document and its assets
            shutil.copytree(os.path.join(QV, '_extensions'), os.path.join(tmp, '_extensions'))
            for item in os.listdir(os.path.dirname(path)):
                p = os.path.join(os.path.dirname(path), item)
                (shutil.copytree if os.path.isdir(p) else shutil.copy)(p, os.path.join(tmp, item))
            env = dict(os.environ, TYPST_IGNORE_SYSTEM_FONTS='true')   # as on a computer without the brand fonts
            r = run(['quarto', 'render', os.path.basename(path), '--to', fmt], cwd=tmp, env=env)
            log = ANSI.sub('', r.stdout + r.stderr)
            open(os.path.join(outdir, f'{fmt}.log'), 'w', encoding='utf-8').write(log)
            ext = 'pdf' if fmt.endswith('typst') else 'docx'
            out = os.path.join(tmp, f'{fx}.{ext}')
            ok = r.returncode == 0 and os.path.exists(out)
            record(fx, fmt, 'renders', ok, log.strip().splitlines()[-1] if log.strip() else f'rc {r.returncode}')
            warns = [l.strip() for l in log.splitlines() if WARN.search(l)]
            record(fx, fmt, 'no warnings', not warns, ' | '.join(warns[:3]))
            if not ok: continue
            fdir = os.path.join(outdir, fmt); os.makedirs(fdir, exist_ok=True)
            for old in glob.glob(os.path.join(fdir, '*')): os.remove(old)
            shutil.copy(out, fdir)
            if ext == 'pdf':
                pdf_checks(fx, fmt, os.path.join(fdir, f'{fx}.pdf'), spec, fdir)
                if not QUIET[0]: visual_checks(fx, fmt, fdir)
            else:
                name = fmt.rsplit('-', 1)[0]
                docx_checks(fx, fmt, os.path.join(fdir, f'{fx}.docx'), spec, os.path.join(QV, '_extensions', 'vcci', name))
                word_checks(fx, fmt, os.path.join(fdir, f'{fx}.docx'), spec, fdir)

def install_test():
    """Layer 6: install with `quarto add` into an empty folder and render every user template there."""
    with tempfile.TemporaryDirectory() as tmp:
        r = run(['quarto', 'add', QV, '--no-prompt'], cwd=tmp)
        installed = sorted(os.listdir(os.path.join(tmp, '_extensions'))) if os.path.isdir(os.path.join(tmp, '_extensions')) else []
        record('install', None, 'quarto add installs the extension', r.returncode == 0 and bool(installed), ', '.join(installed) or ANSI.sub('', r.stderr)[-200:])
        for f in os.listdir(os.path.join(QV, 'templates')):   # the templates and their bibliography
            shutil.copy(os.path.join(QV, 'templates', f), tmp)
        for name, spec in TEMPLATE_SPECS.items():
            for fmt in spec['formats']:
                env = dict(os.environ, TYPST_IGNORE_SYSTEM_FONTS='true')
                r = run(['quarto', 'render', name + '.qmd', '--to', fmt], cwd=tmp, env=env)
                out = os.path.join(tmp, name + ('.pdf' if fmt.endswith('typst') else '.docx'))
                warns = [l.strip() for l in ANSI.sub('', r.stdout + r.stderr).splitlines() if WARN.search(l)]
                record('install', fmt, f'templates/{name}.qmd renders after installation, without warnings',
                       r.returncode == 0 and os.path.exists(out) and not warns, ' | '.join(warns[:2]))

def visual_selftest():
    """Layer 5 must notice a small change: move one approved page's content down by 3 mm."""
    from PIL import Image, ImageChops
    ref = sorted(glob.glob(os.path.join(BASELINE, 'report', 'vcci-report-typst', 'page-*.png')))
    if not ref:
        print('  [SKIP] visual self-test: no baseline')
        return
    with tempfile.TemporaryDirectory() as tmp:
        im = Image.open(ref[-2]).convert('RGB')
        shifted = ImageChops.offset(im, 0, 6)
        p = os.path.join(tmp, 'page-1.png'); shifted.save(p)
        score, _ = page_diff(ref[-2], p)
        record('selftest/visual', None, 'check "pages look like the approved version" catches content moved 3 mm',
               score > TILE_LIMIT, f'score {score:.2f}')
        # one changed word: a 40 x 8 px mark (about 20 x 4 mm) in the text area
        from PIL import ImageDraw
        im = Image.open(ref[-2]).convert('RGB'); ImageDraw.Draw(im).rectangle((120, 300, 160, 308), fill=(22, 26, 38))
        p = os.path.join(tmp, 'page-2.png'); im.save(p)
        score, _ = page_diff(ref[-2], p)
        record('selftest/visual', None, 'check "pages look like the approved version" catches one changed word',
               score > TILE_LIMIT, f'score {score:.2f}')

def selftest(path):
    fx = os.path.splitext(os.path.basename(path))[0]
    expect = yaml.safe_load(open(path, encoding='utf-8').read().split('---')[1])['test']['expect-fail']
    start = len(results)
    QUIET[0] = True
    try:
        test_fixture(path)
    finally:
        QUIET[0] = False
    got = results[start:]
    del results[start:]
    for e in expect:
        caught = [fmt for _, fmt, c, ok, _ in got if e in c and not ok]
        record(f'selftest/{fx}', None, f'check "{e}" catches the deliberate error', bool(caught), '' if caught else 'not detected')

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs(OUT, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    fixtures = [os.path.join(HERE, 'fixtures', f if f.endswith('.qmd') else f + '.qmd') for f in args] \
        or sorted(glob.glob(os.path.join(HERE, 'fixtures', '*.qmd')))
    print('static checks')
    layer1()
    for f in fixtures: test_fixture(f)
    if not args:
        for name, spec in TEMPLATE_SPECS.items():
            test_fixture(os.path.join(QV, 'templates', name + '.qmd'), spec)
    if not args:
        print('\ninstallation')
        install_test()
        print('\nself-test (broken documents must be caught)')
        for f in sorted(glob.glob(os.path.join(HERE, 'selftest', '*.qmd'))): selftest(f)
        visual_selftest()
    failed = [r for r in results if not r[3]]
    lines = ['# quarto-vcci test summary', '', f'{len(results) - len(failed)} passed, {len(failed)} failed', '',
             '| Fixture | Format | Check | Result | Detail |', '|---|---|---|---|---|']
    lines += [f'| {fx} | {fmt or "-"} | {c} | {"PASS" if ok else "**FAIL**"} | {d.replace("|", "/")} |' for fx, fmt, c, ok, d in results]
    open(os.path.join(OUT, 'summary.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'\n{len(results) - len(failed)} passed, {len(failed)} failed -> {os.path.join(OUT, "summary.md")}')
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
