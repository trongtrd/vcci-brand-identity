"""Test the quarto-vcci extensions.  Run from the repository root:  python quarto-vcci/tests/run_tests.py [fixture ...]

Layers (docs/PLAN_QUARTO_VCCI.md, section 5); this file implements 1-4 (Word checks without Word):
  1 static   extensions are built from the current sources and brand tokens; _extension.yml files parse
  2 render   every fixture x format renders in a clean folder with system fonts ignored; any warning fails
  3 PDF      only brand fonts, all embedded; A4; page count in range; required Vietnamese text present;
             no word outside the page's safe area, no body word outside the side margins
  4 Word     only styles defined in the reference document; tables use the VCCI table style; no direct fonts; fonts embedded
A fixture declares what to check in its front matter under `test:` (formats, pages, must-contain).
Self-test (tests/selftest/): deliberately broken documents with `expect-fail: [check, ...]`; the run fails unless each
named check fails on them, which proves the checks catch the errors they are meant to catch.
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
FONT_OK = re.compile(r'^(Lora|LoraItalic|BeVietnamPro|FontAwesome)')   # FontAwesome: Quarto's callout icons
ANSI = re.compile(r'\x1b\[[0-9;]*m')   # Quarto colours its warnings
WARN = re.compile(r'^(WARN|WARNING|ERROR)\b|(^|\.\.\.)(warning|error): ')

results = []   # (fixture, format, check, ok, detail)
QUIET = [False]
def record(fx, fmt, check, ok, detail=''):
    results.append((fx, fmt, check, ok, detail))
    if not QUIET[0]: print(f'  [{"PASS" if ok else "FAIL"}] {fmt or "-"} · {check}{": " + detail if detail and not ok else ""}', flush=True)

def run(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')

def norm(s):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', s)).strip()

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
    txt = os.path.join(outdir, 'text.txt')
    run([tool('pdftotext'), '-enc', 'UTF-8', pdf, txt])
    text = norm(open(txt, encoding='utf-8').read())
    missing = [s for s in spec.get('must-contain', []) if norm(s) not in text]
    record(fx, fmt, 'required Vietnamese text present', not missing, ' | '.join(missing))
    # word boxes: nothing near the paper edge; body words inside the side margins
    bbox = os.path.join(outdir, 'bbox.html')
    run([tool('pdftotext'), '-enc', 'UTF-8', '-bbox', pdf, bbox])
    html = open(bbox, encoding='utf-8').read()
    edge, side = [], []
    for pno, (w, h, body) in enumerate(re.findall(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', html, re.S), 1):
        w, h = float(w), float(h)
        for x0, y0, x1, y1, word in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', body):
            x0, y0, x1, y1 = map(float, (x0, y0, x1, y1))
            if x0 < SAFE_EDGE_MM * MM or y0 < SAFE_EDGE_MM * MM or x1 > w - SAFE_EDGE_MM * MM or y1 > h - SAFE_EDGE_MM * MM:
                edge.append(f'p{pno} "{word}"')
            if x0 < SIDE_MARGIN_MM * MM - 1 or x1 > w - SIDE_MARGIN_MM * MM + 1:
                side.append(f'p{pno} "{word}" x={x0:.0f}-{x1:.0f}')
    record(fx, fmt, f'no text within {SAFE_EDGE_MM} mm of the paper edge', not edge, ', '.join(edge[:5]))
    record(fx, fmt, f'no text outside the {SIDE_MARGIN_MM} mm side margins', not side, ', '.join(side[:5]))
    run([PDFTOPPM, '-png', '-r', '50', pdf, os.path.join(outdir, 'page')])

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
    tbl = re.findall(r'w:tblStyle w:val="([^"]+)"', doc)
    record(fx, fmt, 'tables use the VCCI table style', all(t == 'Table' for t in tbl), ', '.join(sorted(set(tbl))))
    fonts = sorted(set(re.findall(r'w:rFonts [^>]*w:ascii="([^"]+)"', doc)) - {'Lora', 'Lora Medium', 'Lora SemiBold', 'Be Vietnam Pro',
                                                                           'Be Vietnam Pro Medium', 'Be Vietnam Pro SemiBold'})
    record(fx, fmt, 'no direct fonts outside the brand', not fonts, ', '.join(fonts))
    record(fx, fmt, 'fonts embedded', any(n.startswith('word/fonts/') for n in z.namelist()))
    parts = [doc] + [z.read(n).decode('utf-8') for n in ('word/footnotes.xml', 'word/endnotes.xml') if n in z.namelist()]
    plain = norm(''.join(t for p in parts for t in re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)))
    missing = [s for s in spec.get('must-contain', []) if norm(s).replace(' ', '') not in plain.replace(' ', '')]
    record(fx, fmt, 'required Vietnamese text present', not missing, ' | '.join(missing))

def test_fixture(path):
    fx = os.path.splitext(os.path.basename(path))[0]
    src = open(path, encoding='utf-8').read()
    spec = yaml.safe_load(src.split('---')[1]).get('test', {})
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
            else:
                name = fmt.rsplit('-', 1)[0]
                docx_checks(fx, fmt, os.path.join(fdir, f'{fx}.docx'), spec, os.path.join(QV, '_extensions', 'vcci', name))

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
    fixtures = [os.path.join(HERE, 'fixtures', f if f.endswith('.qmd') else f + '.qmd') for f in sys.argv[1:]] \
        or sorted(glob.glob(os.path.join(HERE, 'fixtures', '*.qmd')))
    print('static checks')
    layer1()
    for f in fixtures: test_fixture(f)
    if not sys.argv[1:]:
        print('\nself-test (broken documents must be caught)')
        for f in sorted(glob.glob(os.path.join(HERE, 'selftest', '*.qmd'))): selftest(f)
    failed = [r for r in results if not r[3]]
    lines = ['# quarto-vcci test summary', '', f'{len(results) - len(failed)} passed, {len(failed)} failed', '',
             '| Fixture | Format | Check | Result | Detail |', '|---|---|---|---|---|']
    lines += [f'| {fx} | {fmt or "-"} | {c} | {"PASS" if ok else "**FAIL**"} | {d.replace("|", "/")} |' for fx, fmt, c, ok, d in results]
    open(os.path.join(OUT, 'summary.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'\n{len(results) - len(failed)} passed, {len(failed)} failed -> {os.path.join(OUT, "summary.md")}')
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
