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
  6 install  the release repository (release.py) installs with `quarto use template` and `quarto add` into an empty folder,
             as a user would: every template and chart theme, the same extension at the released version, nothing that
             .quartoignore excludes; every template renders there. --install-from trongtrd/vcci-quarto@vX tests GitHub
  8 charts   the sample charts (tests/charts) are drawn with the matplotlib, ggplot2 and Stata themes; every SVG uses only
             VCCI colours, no transparency, text in the brand fonts, the Vietnamese title, decimal commas, no vertical grid,
             Drum Gold for one value at most, series in brand order; the charts fixture then puts them through layers 2-5
             (R or Stata skipped when not installed, or with --no-stata)
A fixture declares what to check in its front matter under `test:` (formats, pages, must-contain). The user templates
(quarto-vcci/templates/) carry no test key; their checks are in TEMPLATE_SPECS below.
Self-test (tests/selftest/): deliberately broken documents with `expect-fail: [check, ...]`; the run fails unless each
named check fails on them, which proves the checks catch the errors they are meant to catch.
Text is read from the word boxes of each page, so text pushed off a page counts as missing.
Results: quarto-vcci/tests/out/<fixture>/ (outputs, page images) and quarto-vcci/tests/out/summary.md.
"""
import glob, html, json, os, re, shutil, subprocess, sys, tempfile, unicodedata, zipfile
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
FONT_OK = re.compile(r'^(Lora|LoraItalic|BeVietnamPro|JetBrainsMono|FontAwesome|NewCMMath)')   # JetBrains Mono: code
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
    'charts': {'formats': ['vcci-report-typst', 'vcci-report-docx'], 'pages': [3, 5], 'needs-r': True,
               'must-contain': ['Năm 2025 đạt điểm cao nhất trong sáu năm', 'Doanh nghiệp nhỏ đánh giá tích cực hơn',
                                'scale_fill_vcci_div()'],
               'must-contain-pdf': ['67,4', 'Hà Nội', 'Đà Nẵng', 'Nguồn: VCCI, Khảo sát PCI']},
}

# ---------------------------------------------------------------- layer 8: chart themes
CHARTS = os.path.join(QV, 'charts')                 # generated by build.py from src/charts
CHART_SRC = os.path.join(HERE, 'charts')            # sample charts in Python, R and Stata, one data set
CHART_OUT = os.path.join(OUT, 'chart-svg')
# what each sample chart must show; gold: shapes filled Drum Gold (one highlighted value at most)
CHART_SPECS = {
    'bar': {'title': 'Năm 2025 đạt điểm cao nhất trong sáu năm', 'gold': 1, 'comma': '67,4', 'zero': True},
    'line': {'title': 'Hà Nội vượt TP.HCM và Đà Nẵng từ năm 2024', 'comma': '67,5'},
    'stack': {'title': 'Doanh nghiệp nhỏ đánh giá tích cực hơn'},
    'scatter': {'title': 'Chi phí không chính thức tăng theo quy mô'},
    'series6': {'title': 'Sáu ngành theo thứ tự màu chuỗi', 'series': 6},
    'heat': {'title': 'Đông Nam Bộ dẫn đầu, Tây Nguyên cải thiện nhanh', 'comma': '64,1'},
}

def brand_colours():
    """Every colour a VCCI chart may use: brand colours, tonal scales, chart palettes; never status colours."""
    t = json.load(open(os.path.join(ROOT, 'brand-assets', 'brand-tokens.json'), encoding='utf-8'))
    col, dv = t['colour'], t['dataviz']
    ok = {v['hex'].upper() for v in col.values() if isinstance(v, dict) and 'hex' in v}
    ok |= {h.upper() for name, steps in col['scales'].items() if name != 'note' for h in steps.values()}
    ok |= {h.upper() for _, h in dv['categorical']} | {h.upper() for k in ('sequential_7', 'sequential_5', 'diverging_7') for h in dv[k]}
    ok |= {dv['highlight'][k].upper() for k in ('focus', 'context', 'muted')} | {'#FFFFFF'}
    return ok, [h.upper() for _, h in dv['categorical']], dv['highlight']['focus'].upper(), t['typography'], col['Stone']['hex'].upper()

def css_colour(v):
    v = v.strip().strip('"\'')
    if v.startswith('#') and len(v) == 4: v = '#' + ''.join(c * 2 for c in v[1:])
    m = re.match(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', v)
    if m: v = '#%02X%02X%02X' % tuple(int(x) for x in m.groups())
    return {'white': '#FFFFFF', 'black': '#000000'}.get(v.lower(), v.upper())

def svg_elements(path):
    """(tag, props, text) for every element: props merges attributes and inline CSS."""
    import xml.etree.ElementTree as ET
    out = []
    for el in ET.parse(path).iter():
        tag = el.tag.split('}')[-1]
        props = {k.split('}')[-1]: v for k, v in el.attrib.items()}
        for decl in props.pop('style', '').split(';'):
            if ':' in decl:
                k, v = decl.split(':', 1); props[k.strip()] = v.strip()
        out.append((tag, props, ''.join(el.itertext()) if tag == 'text' else ''))
    return out

def points(tag, p):
    """First and last point of a line-like element, or None."""
    if tag == 'line':
        return (float(p.get('x1', 0)), float(p.get('y1', 0))), (float(p.get('x2', 0)), float(p.get('y2', 0)))
    nums = re.findall(r'-?\d+(?:\.\d+)?(?:e-?\d+)?', p.get('points', '') or p.get('d', ''))
    if tag in ('polyline', 'path') and len(nums) >= 4 and not re.search(r'[CcQqAaZz]', p.get('d', '')):
        return (float(nums[0]), float(nums[1])), (float(nums[-2]), float(nums[-1]))
    return None

def svg_checks(label, path, spec):
    ok_colours, series, gold, ty, stone = brand_colours()
    els = svg_elements(path)
    used, bad = set(), set()
    for tag, p, _ in els:
        for k in ('fill', 'stroke', 'color', 'stop-color'):
            v = p.get(k)
            if not v or v.lower() in ('none', 'currentcolor', 'transparent', 'inherit') or v.startswith('url('): continue
            c = css_colour(v); used.add(c)
            if c not in ok_colours: bad.add(c)
    record('charts', label, 'only VCCI colours (no defaults, no status colours)', not bad, ', '.join(sorted(bad)[:6]))
    # transparency mixes colours outside the palette; a fully transparent stroke (Stata's hidden frames) is fine
    alpha = sorted({p[k] for _, p, _ in els for k in ('opacity', 'fill-opacity', 'stroke-opacity')
                    if k in p and 0 < float(p[k]) < 1})
    record('charts', label, 'no transparency', not alpha, ', '.join(alpha[:4]))
    texts = [(p, t) for tag, p, t in els if tag == 'text' and t.strip()]
    fams = {p.get('font-family', '').split(',')[0].strip().strip('"\'') for p, _ in texts}
    brand = {ty['display']['family'], ty['text']['family']}
    record('charts', label, 'text kept as text, in the brand fonts', bool(texts) and fams <= brand,
           'no text elements' if not texts else ', '.join(sorted(fams - brand)))
    words = ' '.join(t for _, t in texts)
    record('charts', label, 'Vietnamese title present', norm(spec['title']) in norm(words), spec['title'])
    if 'comma' in spec:
        numbers = re.findall(r'(?<![\w.])\d+[.,]\d+(?![\w.])', words)
        point = [n for n in numbers if '.' in n and not re.fullmatch(r'\d{1,3}\.\d{3}', n)]
        record('charts', label, 'decimal comma', spec['comma'] in words and not point, ', '.join(point[:4]) or f'no "{spec["comma"]}"')
    # a shape counts once, however many times it is drawn (Stata draws a bar's fill, then its zero-width outline)
    zero_stroke = lambda p: re.match(r'0*\.?0*$', (p.get('stroke-width') or '1').replace('px', '').strip())
    golds = len({tuple(p.get(k) for k in ('x', 'y', 'width', 'height', 'd', 'points')) for tag, p, _ in els if tag != 'text'
                 and ((p.get('fill') and css_colour(p['fill']) == gold)
                      or (p.get('stroke') and css_colour(p['stroke']) == gold and not zero_stroke(p)))})
    record('charts', label, f'Drum Gold only marks one value ({spec.get("gold", 0)} expected)', golds == spec.get('gold', 0), f'{golds} gold shapes')
    vertical = []
    for tag, p, _ in els:
        if p.get('stroke') and css_colour(p['stroke']) == stone and (pt := points(tag, p)):
            (x0, y0), (x1, y1) = pt
            if abs(x1 - x0) < abs(y1 - y0): vertical.append(f'x={x0:.0f}')
    record('charts', label, 'no vertical grid lines', not vertical, ', '.join(vertical[:4]))
    if spec.get('zero'):
        record('charts', label, 'value axis starts at zero', any(t.strip() == '0' for _, t in texts))
    if spec.get('series'):
        # the data lines are the widest strokes; their colours, in drawing order, follow the series order
        width = lambda p: float(re.match(r'[\d.]+', p.get('stroke-width', '0') or '0').group(0) or 0)
        lines = [(width(p), css_colour(p['stroke'])) for tag, p, _ in els if p.get('stroke') and tag in ('path', 'polyline', 'line')
                 and p['stroke'].lower() != 'none']
        top = max(w for w, _ in lines) if lines else 0
        order = list(dict.fromkeys(c for w, c in lines if w >= 0.9 * top))
        record('charts', label, 'series colours in brand order', order == series[:spec['series']],
               ' > '.join(order))

def find_rscript():
    found = shutil.which('Rscript')
    if found: return found
    cands = sorted(glob.glob(r'C:\Program Files\R\R-*\bin\x64\Rscript.exe'))
    return cands[-1] if cands else None

def find_stata():
    if os.environ.get('VCCI_STATA'): return os.environ['VCCI_STATA']
    for name in ('stata-mp', 'stata-se', 'stata'):
        if shutil.which(name): return shutil.which(name)
    cands = [c for c in sorted(glob.glob(r'C:\Program Files\Stata*\Stata*-64.exe')) if '_old' not in c]
    return cands[-1] if cands else None

def chart_layer():
    """Layer 8: draw the sample charts with each tool, then check every SVG against the brand rules."""
    os.makedirs(CHART_OUT, exist_ok=True)
    for old in glob.glob(os.path.join(CHART_OUT, '*.svg')) + glob.glob(os.path.join(CHART_OUT, '*.log')): os.remove(old)
    data = os.path.join(CHART_SRC, 'data')
    tools = {'py': [sys.executable, os.path.join(CHART_SRC, 'charts.py'), CHART_OUT, CHARTS]}
    r = find_rscript()
    if r: tools['r'] = [r, os.path.join(CHART_SRC, 'charts.R'), CHART_OUT, CHARTS]
    else: print('  [SKIP] R: Rscript not found')
    st = find_stata()
    if '--no-stata' in sys.argv: print('  [SKIP] Stata: --no-stata')
    elif st: tools['stata'] = [st, '/e' if sys.platform == 'win32' else '-b', 'do', os.path.join(CHART_SRC, 'charts.do'), CHART_OUT, CHARTS, data]
    else: print('  [SKIP] Stata: not found (set VCCI_STATA to the Stata executable)')
    for tool_name, cmd in tools.items():
        res = run(cmd, cwd=CHART_OUT)
        log = res.stdout + res.stderr
        if tool_name == 'stata' and os.path.exists(os.path.join(CHART_OUT, 'charts.log')):
            log = open(os.path.join(CHART_OUT, 'charts.log'), encoding='utf-8', errors='replace').read()
        open(os.path.join(CHART_OUT, f'{tool_name}.log' if tool_name != 'stata' else 'stata-run.log'), 'w', encoding='utf-8').write(log)
        expected = [c for c in CHART_SPECS if not (tool_name == 'stata' and c == 'heat')]
        missing = [c for c in expected if not os.path.exists(os.path.join(CHART_OUT, f'{tool_name}-{c}.svg'))]
        errors = [l for l in log.splitlines() if re.match(r'^r\(\d+\);|^Error|Traceback|^\(note: +named style', l)]
        record('charts', tool_name, 'sample charts draw without errors', not missing and not errors,
               ', '.join(missing) + ' | '.join(errors[:3]))
        for c in expected:
            p = os.path.join(CHART_OUT, f'{tool_name}-{c}.svg')
            if os.path.exists(p): svg_checks(f'{tool_name}-{c}', p, CHART_SPECS[c])
    readme_examples(tools)

def readme_examples(tools, readme=None, label='README'):
    """Every code example in charts/README.md runs as written, in a folder set up as the README says
    (the theme files next to the code, the extension installed), and writes its chart in VCCI colours."""
    md = open(readme or os.path.join(CHARTS, 'README.md'), encoding='utf-8').read()
    ok_colours = brand_colours()[0]
    for lang, code in re.findall(r'```(python|r|stata)\n(.*?)```', md, re.S):
        name = {'python': 'py', 'r': 'r', 'stata': 'stata'}[lang]
        if name not in tools: continue
        out = re.search(r'(?:savefig|ggsave|graph export)\(?\s*"([^"]+)"', code).group(1)
        with tempfile.TemporaryDirectory() as tmp:
            for f in os.listdir(CHARTS): shutil.copy(os.path.join(CHARTS, f), tmp)
            shutil.copytree(os.path.join(QV, '_extensions'), os.path.join(tmp, '_extensions'))
            src = os.path.join(tmp, {'py': 'example.py', 'r': 'example.R', 'stata': 'example.do'}[name])
            open(src, 'w', encoding='utf-8').write(code)
            cmd = [sys.executable, src] if name == 'py' else tools['r'][:1] + [src] if name == 'r' else tools['stata'][:2] + ['do', src]
            res = run(cmd, cwd=tmp)
            log = res.stdout + res.stderr
            if name == 'stata' and os.path.exists(os.path.join(tmp, 'example.log')):
                log = open(os.path.join(tmp, 'example.log'), encoding='utf-8', errors='replace').read()
            errors = [l for l in log.splitlines() if re.match(r'^r\(\d+\);|^Error|Traceback', l)]
            p = os.path.join(tmp, out)
            made = os.path.exists(p)
            bad = set()
            if made:
                for _, props, _ in svg_elements(p):
                    for k in ('fill', 'stroke'):
                        v = props.get(k)
                        if v and v.lower() not in ('none', 'currentcolor') and not v.startswith('url(') and css_colour(v) not in ok_colours:
                            bad.add(css_colour(v))
            record('charts', f'{label} {lang}', f'example runs and writes {out} in VCCI colours',
                   made and not errors and not bad, ' | '.join(errors[:2]) or ', '.join(sorted(bad)) or ('' if made else 'no output'))

def chart_selftest():
    """Broken charts (tests/selftest/charts) must be caught by the checks named in expect.yml."""
    base = os.path.join(HERE, 'selftest', 'charts')
    expect = yaml.safe_load(open(os.path.join(base, 'expect.yml'), encoding='utf-8'))
    for f, e in expect.items():
        start = len(results)
        QUIET[0] = True
        try:
            svg_checks(f, os.path.join(base, f), CHART_SPECS[e['spec']])
        finally:
            QUIET[0] = False
        got = results[start:]
        del results[start:]
        for check in e['expect-fail']:
            caught = [c for _, _, c, ok, _ in got if check in c and not ok]
            record(f'selftest/charts', f, f'check "{check}" catches the deliberate error', bool(caught), '' if caught else 'not detected')
    # README examples: one that fails to run, one that draws in matplotlib's default colours
    start = len(results)
    QUIET[0] = True
    try:
        readme_examples({'py': [sys.executable]}, os.path.join(base, 'broken-readme.md'), 'broken README')
    finally:
        QUIET[0] = False
    got = results[start:]
    del results[start:]
    record('selftest/charts', 'broken-readme.md', 'check "example runs ... in VCCI colours" catches both broken examples',
           len(got) == 2 and not any(ok for *_, ok, _ in got), f'{sum(1 for *_, ok, _ in got if not ok)} of {len(got)} caught')

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
    # must-contain-pdf: text only the PDF shows as text (inside SVG charts; Word turns them into pictures)
    want = spec.get('must-contain', []) + spec.get('must-contain-pdf', [])
    missing = [s for s in want if norm(s).replace(' ', '') not in visible.replace(' ', '')]
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
    doc = pymupdf.open(pdf)
    # Word renames a font it takes from the document's embedded copies ("___WRD_EMBED_SUB_52"): identify it by its outlines
    real = {f[3]: embedded_font_name(doc, f[0]) for p in doc for f in p.get_fonts() if '___WRD_EMBED_SUB' in f[3]}
    for page in doc:
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    font = next((v for k, v in real.items() if k.endswith(span['font'].split('+')[-1])), span['font'])
                    font = font.split('+')[-1].replace(' ', '')
                    if not re.match(r'^(Lora|BeVietnam|JetBrainsMono|CambriaMath)', font) and span['text'].strip(' •·◦▪	-'):
                        bad.add(f'{font}: "{span["text"][:20]}"')
    record(fx, fmt, 'Word PDF sets all text in brand fonts', not bad, ', '.join(sorted(bad)[:5]))
    txt = os.path.join(outdir, 'word-text.txt')
    run([tool('pdftotext'), '-enc', 'UTF-8', pdf, txt])
    text = norm(open(txt, encoding='utf-8').read())
    missing = [s for s in spec.get('must-contain', []) if norm(s) not in text]
    record(fx, fmt, 'Word PDF shows the required text', not missing, ' | '.join(missing))
    run([PDFTOPPM, '-png', '-r', '50', pdf, os.path.join(outdir, 'word-page')])

BRAND_FONTS = []   # (name, TTFont) of every font in brand-assets/03_Fonts, loaded once

def embedded_font_name(doc, xref):
    """The brand font whose glyph outlines a font program in the PDF carries, or the program's own name."""
    import io
    from fontTools.ttLib import TTFont
    def outlines(font):   # every non-empty glyph as its point list (subsets renumber glyphs and may drop cmap)
        glyf = font['glyf']
        return {tuple(glyf[g].getCoordinates(glyf)[0].array.tolist()) for g in font.getGlyphOrder()
                if glyf[g].numberOfContours != 0} - {()}
    name, _, _, buf = doc.extract_font(xref)
    try:
        sub = outlines(TTFont(io.BytesIO(buf)))
    except Exception:
        return name
    if not BRAND_FONTS:
        BRAND_FONTS.extend((os.path.splitext(os.path.basename(f))[0], outlines(TTFont(f)))
                           for f in sorted(glob.glob(os.path.join(ROOT, 'brand-assets', '03_Fonts', '*', '*.ttf'))))
    for brand, ref in BRAND_FONTS:
        if sub and sub <= ref:
            return brand
    return name

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
                                                                           'Be Vietnam Pro Medium', 'Be Vietnam Pro SemiBold', 'JetBrains Mono'})
    record(fx, fmt, 'no direct fonts outside the brand', not fonts, ', '.join(fonts))
    record(fx, fmt, 'fonts embedded', any(n.startswith('word/fonts/') for n in z.namelist()))
    parts = [doc] + [z.read(n).decode('utf-8') for n in ('word/footnotes.xml', 'word/endnotes.xml') if n in z.namelist()]
    plain = norm(html.unescape(''.join(t for p in parts for t in re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))))   # "&lt;-" is "<-"
    record(fx, fmt, 'no broken characters (U+FFFD)', '\ufffd' not in plain)   # e.g. a byte-wise string.upper in Lua
    missing = [s for s in spec.get('must-contain', []) if norm(s).replace(' ', '') not in plain.replace(' ', '')]
    record(fx, fmt, 'required Vietnamese text present', not missing, ' | '.join(missing))

def test_fixture(path, spec=None):
    fx = os.path.splitext(os.path.basename(path))[0]
    src = open(path, encoding='utf-8').read()
    if spec is None: spec = yaml.safe_load(src.split('---')[1]).get('test', {})
    if not QUIET[0]: print(f'\n{fx}', flush=True)
    if spec.get('needs-r') and not find_rscript():
        print(f'  [SKIP] {fx}: R not installed')
        return
    need = [f'{t}-{c}.svg' for t in spec.get('charts', []) for c in CHART_SPECS if not (t == 'stata' and c == 'heat')]
    missing = [n for n in need if not os.path.exists(os.path.join(CHART_OUT, n))]
    if missing:
        print(f'  [SKIP] {fx}: sample charts not drawn ({", ".join(missing[:3])}...)')
        return
    outdir = os.path.join(OUT, fx)
    os.makedirs(outdir, exist_ok=True)
    for fmt in spec.get('formats', []):
        with tempfile.TemporaryDirectory() as tmp:
            # a clean folder, as a user gets it: the extension, the document and its assets,
            # and the chart themes, which users copy next to their document
            shutil.copytree(os.path.join(QV, '_extensions'), os.path.join(tmp, '_extensions'))
            for item in os.listdir(os.path.dirname(path)):
                p = os.path.join(os.path.dirname(path), item)
                (shutil.copytree if os.path.isdir(p) else shutil.copy)(p, os.path.join(tmp, item))
            for f in os.listdir(CHARTS): shutil.copy(os.path.join(CHARTS, f), tmp)
            if need:
                os.makedirs(os.path.join(tmp, 'charts'))
                for n in need: shutil.copy(os.path.join(CHART_OUT, n), os.path.join(tmp, 'charts'))
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

# ---------------------------------------------------------------- layer 6: installation from the release repository
sys.path.insert(0, QV)
import build, release

# what `quarto use template` must leave in a folder named vcci-test: the report template takes the folder's name
USER_FILES = {'vcci-test.qmd': 'report', 'wp.qmd': 'wp', 'memo.qmd': 'memo', 'charts.qmd': 'charts', 'references.bib': None}
NOT_COPIED = ['README.md', 'LICENSE.md', 'CHANGELOG.md', 'CITATION.cff', 'examples', 'template.qmd']   # .quartoignore

def installed_formats(folder):
    """{format: path} of the installed extensions: _extensions/<name> (local source) or _extensions/<owner>/<name> (GitHub)."""
    found = {}
    for p in glob.glob(os.path.join(folder, '_extensions', '*', '_extension.yml')) + glob.glob(os.path.join(folder, '_extensions', '*', '*', '_extension.yml')):
        found[os.path.basename(os.path.dirname(p))] = os.path.dirname(p)
    return found

def install_test(source, label='install', render=True):
    """Layer 6: install from the release repository (a local export, or trongtrd/vcci-quarto@vX on GitHub) as a user would:
    `quarto use template` into an empty folder must give the templates, the chart themes and an extension identical to
    this build, at the released version, and nothing listed in .quartoignore; every template renders there.
    `quarto add` must install the same extension."""
    ver = release.version()
    with tempfile.TemporaryDirectory() as tmp:
        d = os.path.join(tmp, 'vcci-test')
        os.makedirs(d)
        r = run(['quarto', 'use', 'template', source, '--no-prompt'], cwd=d)
        record(label, None, 'quarto use template succeeds', r.returncode == 0, ANSI.sub('', r.stderr)[-200:])
        missing = [f for f in USER_FILES if not os.path.isfile(os.path.join(d, f))]
        missing += [f'charts/{f}' for f in os.listdir(CHARTS) if not os.path.isfile(os.path.join(d, 'charts', f))]
        record(label, None, 'quarto use template creates every template and chart theme', not missing, ', '.join(missing))
        extra = [f for f in NOT_COPIED if os.path.exists(os.path.join(d, f))]
        record(label, None, '.quartoignore keeps README, LICENSE, CHANGELOG, CITATION and examples out of the user folder', not extra, ', '.join(extra))
        ext = installed_formats(d)
        record(label, None, 'the installed extension is identical to this build (every font, style and filter)',
               sorted(ext) == build.FORMATS and all(build.same_tree(p, os.path.join(build.OUT, f)) for f, p in ext.items()),
               f'installed: {", ".join(os.path.relpath(p, d) for p in ext.values()) or "none"}')
        vers = {f: re.search(r'^version:\s*(\S+)', open(os.path.join(p, '_extension.yml'), encoding='utf-8').read(), re.M).group(1)
                for f, p in ext.items()}
        record(label, None, f'every installed format is version {ver}', len(vers) == len(build.FORMATS) and set(vers.values()) == {ver}, str(vers))
        a = os.path.join(tmp, 'add')
        os.makedirs(a)
        r = run(['quarto', 'add', source, '--no-prompt'], cwd=a)
        added = installed_formats(a)
        record(label, None, 'quarto add installs the same extension', r.returncode == 0 and sorted(added) == build.FORMATS
               and all(build.same_tree(p, os.path.join(build.OUT, f)) for f, p in added.items()), ANSI.sub('', r.stderr)[-200:])
        if not render: return
        for f, name in USER_FILES.items():
            if not name: continue
            spec = TEMPLATE_SPECS[name]
            if spec.get('needs-r') and not find_rscript(): continue
            for fmt in spec['formats']:
                env = dict(os.environ, TYPST_IGNORE_SYSTEM_FONTS='true')
                r = run(['quarto', 'render', f, '--to', fmt], cwd=d, env=env)
                out = os.path.join(d, f[:-4] + ('.pdf' if fmt.endswith('typst') else '.docx'))
                warns = [l.strip() for l in ANSI.sub('', r.stdout + r.stderr).splitlines() if WARN.search(l)]
                record(label, fmt, f'{f} renders after installation, without warnings',
                       r.returncode == 0 and os.path.exists(out) and not warns, ' | '.join(warns[:2]) or ANSI.sub('', r.stderr)[-200:])

def local_install_test():
    """Layer 6 on a fresh local export of the release repository (before anything is pushed)."""
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, 'quarto-vcci')
        release.export(out)
        install_test(out)

def install_selftest():
    """Broken release exports must be caught: a missing font, and examples/ left out of .quartoignore."""
    def broken(name, expect, damage):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, 'quarto-vcci')
            release.export(out)
            damage(out)
            start = len(results)
            QUIET[0] = True
            try:
                install_test(out, render=False)
            finally:
                QUIET[0] = False
            got = results[start:]
            del results[start:]
            caught = [c for _, _, c, ok, _ in got if expect in c and not ok]
            record('selftest/install', name, f'check "{expect}" catches the deliberate error', bool(caught), '' if caught else 'not detected')
    broken('missing-font', 'identical to this build',
           lambda out: os.remove(os.path.join(out, '_extensions', 'vcci-wp', 'fonts', 'Lora-Medium.ttf')))
    # the layout Quarto cannot read: _extensions/vcci/<name> installs nothing with `quarto use template`
    def nested(out):
        os.makedirs(os.path.join(out, '_extensions', 'vcci'))
        for f in build.FORMATS: shutil.move(os.path.join(out, '_extensions', f), os.path.join(out, '_extensions', 'vcci', f))
    broken('nested-extensions', 'identical to this build', nested)
    def unignore(out):
        p = os.path.join(out, '.quartoignore')
        open(p, 'w', encoding='utf-8').write(open(p, encoding='utf-8').read().replace('examples/\n', ''))
    broken('examples-copied', '.quartoignore keeps', unignore)

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

def font_identity_selftest():
    """Word renames embedded fonts; identifying them by outlines must name JetBrains Mono and must not
    mistake another monospace font (DejaVu Sans Mono, built into Typst) for a brand font."""
    import pymupdf
    fonts = os.path.join(QV, '_extensions', 'vcci', 'vcci-report', 'fonts')
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 't.typ')
        open(src, 'w', encoding='utf-8').write('#text(font: "JetBrains Mono")[pci_2025 Đà Nẵng]\n\n'
                                                '#text(font: "DejaVu Sans Mono")[pci_2025 Da Nang]\n')
        run(['quarto', 'typst', 'compile', '--ignore-system-fonts', '--font-path', fonts, src, os.path.join(tmp, 't.pdf')])
        doc = pymupdf.open(os.path.join(tmp, 't.pdf'))
        try:
            found = {f[3].split('+')[-1]: embedded_font_name(doc, f[0]) for f in doc[0].get_fonts()}
        finally:
            doc.close()
    jb = [v for k, v in found.items() if k.startswith('JetBrains')]
    dv = [v for k, v in found.items() if k.startswith('DejaVu')]
    record('selftest/fonts', None, 'renamed-font check identifies JetBrains Mono by its outlines', jb == ['JetBrainsMono-Regular'], str(found))
    record('selftest/fonts', None, 'renamed-font check does not take DejaVu Sans Mono for a brand font',
           bool(dv) and not any(v.split('-')[0] in ('Lora', 'BeVietnamPro', 'JetBrainsMono') for v in dv), str(found))

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
    if '--install-from' in sys.argv:   # layer 6 only, e.g. --install-from trongtrd/vcci-quarto@v1.0.0
        source = sys.argv[sys.argv.index('--install-from') + 1]
        print(f'installation from {source}')
        install_test(source)
        failed = [r for r in results if not r[3]]
        print(f'\n{len(results) - len(failed)} passed, {len(failed)} failed')
        sys.exit(1 if failed else 0)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    fixtures = [os.path.join(HERE, 'fixtures', f if f.endswith('.qmd') else f + '.qmd') for f in args] \
        or sorted(glob.glob(os.path.join(HERE, 'fixtures', '*.qmd')))
    print('static checks')
    layer1()
    if not args or any('charts:' in open(f, encoding='utf-8').read().split('---')[1] for f in fixtures):
        print('\nchart themes (sample charts in Python, R and Stata)')
        chart_layer()
    for f in fixtures: test_fixture(f)
    if not args:
        for name, spec in TEMPLATE_SPECS.items():
            test_fixture(os.path.join(QV, 'templates', name + '.qmd'), spec)
    if not args:
        print('\ninstallation (local export of the release repository)')
        local_install_test()
        print('\nself-test (broken documents must be caught)')
        for f in sorted(glob.glob(os.path.join(HERE, 'selftest', '*.qmd'))): selftest(f)
        visual_selftest()
        chart_selftest()
        font_identity_selftest()
        install_selftest()
    failed = [r for r in results if not r[3]]
    lines = ['# quarto-vcci test summary', '', f'{len(results) - len(failed)} passed, {len(failed)} failed', '',
             '| Fixture | Format | Check | Result | Detail |', '|---|---|---|---|---|']
    lines += [f'| {fx} | {fmt or "-"} | {c} | {"PASS" if ok else "**FAIL**"} | {d.replace("|", "/")} |' for fx, fmt, c, ok, d in results]
    open(os.path.join(OUT, 'summary.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'\n{len(results) - len(failed)} passed, {len(failed)} failed -> {os.path.join(OUT, "summary.md")}')
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
