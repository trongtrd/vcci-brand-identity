"""Render the brand board (board/vcci-brand-board.html) to board/export/ and measure its cards for the guide.

Outputs:  board/export/VCCI-Brand-Identity-Board@2x.png   (4800 px wide)
          board/export/VCCI-Brand-Identity-Board_preview.jpg (1600 px wide)
          board/export/VCCI-Brand-Identity-Board.pdf      (single page, vector text)
          build/board/rects.json                          (card positions, used by tools/guide/prepare_images.py)
Run from the repository root:  python tools/board/render.py [--quick]   (--quick: 1x PNG to build/board/ only)
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from PIL import Image
from env import ROOT, EDGE, build

Image.MAX_IMAGE_PIXELS = None
HTML = os.path.join(ROOT, 'board', 'vcci-brand-board.html')
EXPORT = os.path.join(ROOT, 'board', 'export'); os.makedirs(EXPORT, exist_ok=True)
URL = lambda p: 'file:///' + p.replace(os.sep, '/').replace(' ', '%20')
BG = np.array([0xEE, 0xEA, 0xE0])          # board background colour


def edge(*args):
    return subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', *args],
                          capture_output=True, text=True, encoding='utf-8', errors='replace')


def screenshot(scale, out):
    edge(f'--force-device-scale-factor={scale}', '--window-size=2400,9800', '--virtual-time-budget=6000', f'--screenshot={out}', URL(HTML))
    im = Image.open(out).convert('RGB'); a = np.asarray(im).astype(int)
    rows = np.where((np.abs(a - BG).sum(2) > 12).any(1))[0]
    end = min(im.size[1], rows.max() + 1 + int(80 * scale))   # keep the 80 px bottom margin
    im = im.crop((0, 0, im.size[0], end)); im.save(out)
    return im, end / scale


def measure():
    """Card rectangles (CSS px) via a temporary copy of the board with a measuring script."""
    s = open(HTML, encoding='utf-8').read()
    js = ("<script>window.addEventListener('load',()=>{const r=[...document.querySelectorAll('section.card')].map((e,i)=>{"
          "const b=e.getBoundingClientRect();const t=(e.querySelector('.cl .t')||{}).textContent||e.className;"
          "return [i,t,Math.round(b.left),Math.round(b.top+scrollY),Math.round(b.width),Math.round(b.height)]});"
          "const p=document.createElement('pre');p.id='rects';p.textContent=JSON.stringify(r);document.body.appendChild(p)})</script>")
    tmp = os.path.join(ROOT, 'board', '_measure.html')
    open(tmp, 'w', encoding='utf-8').write(s.replace('</body>', js + '</body>'))
    try:
        dom = edge('--window-size=2400,9800', '--virtual-time-budget=5000', '--dump-dom', URL(tmp)).stdout
    finally:
        os.remove(tmp)
    rects = json.loads(re.search(r'<pre id="rects">(.*?)</pre>', dom, re.S).group(1))
    json.dump(rects, open(build('board', 'rects.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    return rects


if __name__ == '__main__':
    if '--quick' in sys.argv:
        im, h = screenshot(1, build('board', 'board@1x.png')); print('quick render', im.size); sys.exit()
    im, h = screenshot(2, os.path.join(EXPORT, 'VCCI-Brand-Identity-Board@2x.png'))
    im.resize((1600, round(im.size[1] * 1600 / im.size[0])), Image.LANCZOS).save(os.path.join(EXPORT, 'VCCI-Brand-Identity-Board_preview.jpg'), quality=90)
    # PDF: one page sized to the board
    s = open(HTML, encoding='utf-8').read()
    s = re.sub(r'@page\{size:[^}]*\}', f'@page{{size:2400px {round(h)}px;margin:0}}', s)
    tmp = os.path.join(ROOT, 'board', '_print.html'); open(tmp, 'w', encoding='utf-8').write(s)
    try:
        edge('--no-pdf-header-footer', '--virtual-time-budget=6000', f'--print-to-pdf={os.path.join(EXPORT, "VCCI-Brand-Identity-Board.pdf")}', URL(tmp))
    finally:
        os.remove(tmp)
    rects = measure()
    print('board', im.size, f'{round(h)} css px;', len(rects), 'cards measured')
