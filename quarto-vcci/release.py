"""Export quarto-vcci as the release repository used by `quarto use template trongtrd/vcci-quarto`.

    python quarto-vcci/release.py --out "C:/GitHub Projects/vcci-quarto"

The release repository is generated, never edited by hand. Its layout:
  _extensions/<format>/            the built extensions (build.py --check must pass first); users get _extensions/trongtrd/<format>
  template.qmd                     templates/report.qmd (quarto use template renames it to <folder>.qmd)
  wp.qmd, memo.qmd, references.bib, charts.qmd
  charts/                          chart themes and their README
  examples/*.pdf, preview.png      rendered samples and the README picture made from them (the .docx samples go to the
                                   GitHub release instead)
  README.md                        quarto-vcci/README.md without its <!-- dev-only --> blocks
  LICENSE.md, CHANGELOG.md, CITATION.cff, .quartoignore   from src/release/ (CITATION.cff gives GitHub's "Cite this repository")
The version comes from the three src/formats/*/_extension.yml, which must agree.
Everything in --out except .git/ is replaced, so the folder always matches this export.
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

import build

HERE = build.HERE
REPO = 'trongtrd/vcci-quarto'
SRC_RELEASE = os.path.join(HERE, 'src', 'release')
TEMPLATES = {'template.qmd': 'report.qmd', 'wp.qmd': 'wp.qmd', 'memo.qmd': 'memo.qmd', 'references.bib': 'references.bib',
             'charts.qmd': 'charts.qmd'}
EXPECTED = ['.quartoignore', 'CHANGELOG.md', 'CITATION.cff', 'LICENSE.md', 'README.md', '_extensions', 'charts', 'charts.qmd', 'examples',
            'memo.qmd', 'references.bib', 'template.qmd', 'wp.qmd']


def version():
    found = {}
    for fmt in build.FORMATS:
        y = open(os.path.join(HERE, 'src', 'formats', fmt, '_extension.yml'), encoding='utf-8').read()
        found[fmt] = re.search(r'^version:\s*(\S+)', y, re.M).group(1)
    if len(set(found.values())) != 1: sys.exit(f'versions differ: {found}')
    return found[build.FORMATS[0]]


def replace(s, old, new, where):
    """Replace text that must be there: if a source changes, the export stops instead of shipping a stale README."""
    if old not in s: sys.exit(f'release.py: "{old[:60]}" not found in {where}; update release.py')
    return s.replace(old, new)


def readme(ver):
    """README.md is written for users of the release repository; blocks between <!-- dev-only --> and
    <!-- /dev-only --> concern this source folder only and are dropped."""
    s = open(os.path.join(HERE, 'README.md'), encoding='utf-8').read()
    s = re.sub(r'<!-- dev-only -->.*?<!-- /dev-only -->\n\n?', '', s, flags=re.S)
    if 'dev-only' in s: sys.exit('release.py: unbalanced dev-only block in README.md')
    if 'templates/' in s or '](../' in s or 'brand-assets' in s or 'DEVELOPMENT.md' in s:
        sys.exit('release.py: README.md refers to the development repository outside a dev-only block')
    # the README pins and links this version (installation, Word samples attached to the release, the citation)
    stale = sorted(set(re.findall(r'(?:@v|/download/v|phiên bản |version\s*=\s*\{)(\d+\.\d+\.\d+)', s)) - {ver})
    if stale or f'@v{ver}' not in s: sys.exit(f'release.py: README.md must name version {ver}, found {stale}')
    return s


def charts_readme(text):
    w = 'charts/README.md'
    text = replace(text, ' Các file trong thư mục này được `quarto-vcci/build.py` sinh từ `brand-assets/brand-tokens.json`; '
                         'muốn sửa thì sửa nguồn trong `quarto-vcci/src/charts/`, đừng sửa bản sinh ra.',
                   ' Các file trong thư mục này được sinh tự động từ bảng màu và font của bộ nhận diện; đừng sửa tay.', w)
    text = replace(text, 'Cài Lora và Be Vietnam Pro từ `brand-assets/03_Fonts`. Nếu chưa cài, Python và R tự tìm font trong '
                         'extension Quarto (thư mục `fonts` trong `_extensions/`) hoặc trong `brand-assets/03_Fonts`,',
                   'Font Lora và Be Vietnam Pro nằm trong `_extensions/trongtrd/vcci-report/fonts`; cài vào máy để Stata dùng được. '
                   'Nếu chưa cài, Python và R tự tìm font trong extension Quarto (thư mục `fonts` trong `_extensions/`),', w)
    text = replace(text, 'xem mẫu `quarto-vcci/templates/charts.qmd`', 'xem mẫu `charts.qmd`', w)
    if 'brand-assets' in text or 'quarto-vcci/' in text: sys.exit('release.py: charts/README.md still refers to the development repository')
    return text


def charts_qmd(text):
    """The release keeps the chart themes in charts/; the template sources them from there."""
    return replace(text, 'source("theme_vcci.R", encoding = "UTF-8")   # chép theme_vcci.R (thư mục charts/ của quarto-vcci) cạnh file này',
                   'source("charts/theme_vcci.R", encoding = "UTF-8")', 'templates/charts.qmd')


PREVIEW = [('report.pdf', 0), ('report.pdf', 5), ('wp.pdf', 0), ('memo.pdf', 0)]   # cover, a chapter, first pages

def preview():
    """examples/preview.png for the README: four sample pages side by side, drawn from the sample PDFs."""
    import pymupdf
    from PIL import Image
    pages = []
    for f, n in PREVIEW:
        pix = pymupdf.open(os.path.join(HERE, 'examples', f))[n].get_pixmap(dpi=48)
        pages.append(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))
    gap, pad = 24, 24
    out = Image.new('RGB', (sum(p.width for p in pages) + gap * (len(pages) - 1) + 2 * pad, max(p.height for p in pages) + 2 * pad), '#E9E4D8')
    x = pad
    for p in pages:
        out.paste(p, (x, pad)); x += p.width + gap
    out.save(os.path.join(HERE, 'examples', 'preview.png'), optimize=True)


def stage(dst, ver):
    # flat: `quarto use template` reads <repo>/_extensions/<name> only (Quarto 1.9, readExtensions on the staged repo), and
    # installs to _extensions/<GitHub owner>/<name> itself; _extensions/vcci/<name> would install nothing
    for fmt in build.FORMATS:
        shutil.copytree(os.path.join(build.OUT, fmt), os.path.join(dst, '_extensions', fmt))
    for name, src in TEMPLATES.items():
        text = open(os.path.join(HERE, 'templates', src), encoding='utf-8').read()
        if name == 'charts.qmd': text = charts_qmd(text)
        open(os.path.join(dst, name), 'w', encoding='utf-8', newline='\n').write(text)
    os.makedirs(os.path.join(dst, 'charts'))
    for f in os.listdir(build.CHART_OUTS[0]):
        text = open(os.path.join(build.CHART_OUTS[0], f), encoding='utf-8').read()
        if f == 'README.md': text = charts_readme(text)
        open(os.path.join(dst, 'charts', f), 'w', encoding='utf-8', newline='\n').write(text)
    os.makedirs(os.path.join(dst, 'examples'))
    for f in sorted(os.listdir(os.path.join(HERE, 'examples'))):
        if f.endswith(('.pdf', '.png')): shutil.copy2(os.path.join(HERE, 'examples', f), os.path.join(dst, 'examples', f))
    cff = open(os.path.join(SRC_RELEASE, 'CITATION.cff'), encoding='utf-8').read()
    if re.search(r'^version:\s*"?([^"\s]+)', cff, re.M).group(1) != ver: sys.exit(f'release.py: CITATION.cff must name version {ver}')
    for f in ('LICENSE.md', 'CITATION.cff', '.quartoignore'):
        shutil.copy2(os.path.join(SRC_RELEASE, f), os.path.join(dst, f))
    changelog = open(os.path.join(SRC_RELEASE, 'CHANGELOG.md'), encoding='utf-8').read()
    if f'## {ver} ' not in changelog: sys.exit(f'release.py: CHANGELOG.md has no entry for {ver}')
    open(os.path.join(dst, 'CHANGELOG.md'), 'w', encoding='utf-8', newline='\n').write(changelog)
    open(os.path.join(dst, 'README.md'), 'w', encoding='utf-8', newline='\n').write(readme(ver))
    if sorted(os.listdir(dst)) != EXPECTED: sys.exit(f'release.py: unexpected layout {sorted(os.listdir(dst))}')


def export(out):
    """Make out identical to a fresh export, keeping out/.git."""
    if subprocess.run([sys.executable, os.path.join(HERE, 'build.py'), '--check']).returncode:
        sys.exit('release.py: run python quarto-vcci/build.py first')
    existing = set(os.listdir(out)) - {'.git'} if os.path.isdir(out) else set()
    if existing and not {'_extensions', 'template.qmd', '.quartoignore'} <= existing:
        sys.exit(f'release.py: {out} is not empty and is not a quarto-vcci release; refusing to replace it')
    ver = version()
    preview()
    with tempfile.TemporaryDirectory() as tmp:
        stage(tmp, ver)
        os.makedirs(out, exist_ok=True)
        for name in os.listdir(out):   # build.sync would also remove .git
            if name != '.git' and name not in os.listdir(tmp):
                p = os.path.join(out, name)
                shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        for name in os.listdir(tmp):
            s, d = os.path.join(tmp, name), os.path.join(out, name)
            if os.path.isdir(s): build.sync(s, d)
            elif not os.path.exists(d) or not build.same_file(s, d): shutil.copy2(s, d)
    return ver


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True, help='release repository folder (created if missing; .git is kept)')
    a = ap.parse_args()
    ver = export(os.path.abspath(a.out))
    docx = sorted(f for f in os.listdir(os.path.join(HERE, 'examples')) if f.endswith('.docx'))
    print(f'exported vcci-quarto {ver} -> {os.path.abspath(a.out)}')
    print('attach to the GitHub release v' + ver + ':', ', '.join(f'examples/{f}' for f in docx))
