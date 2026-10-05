"""Collect the images used by the brand guidelines into build/guide/img/.

- mockups cropped from the rendered brand board (needs tools/board/render.py first)
- page previews of the Word and PowerPoint templates (from their PDF previews in brand-assets/06_Templates)
Run from the repository root:  python tools/guide/prepare_images.py
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from PIL import Image
from env import ROOT, PDFTOPPM, build

Image.MAX_IMAGE_PIXELS = None
IMG = build('guide', 'img')
rects = {r[1]: r for r in json.load(open(build('board', 'rects.json'), encoding='utf-8'))}
board = Image.open(os.path.join(ROOT, 'board', 'export', 'VCCI-Brand-Identity-Board@2x.png')).convert('RGB')

# board cards -> mockups (2x export; skip the 86 px card label row)
for card, name, width in (('Stationery', 'stationery', None), ('Member App', 'app', 470), ('Website', 'website', None),
                          ('Event Poster', 'poster', None), ('Social Media', 'social', None), ('Event Badge', 'badge', None),
                          ('Gift Box', 'giftbox', None)):
    _, _, x, y, w, h = rects[card]
    w = width or w
    board.crop((2 * x, 2 * (y + 86), 2 * (x + w), 2 * (y + h))).save(os.path.join(IMG, f'mock_{name}.jpg'), quality=88)

# template previews
T = os.path.join(ROOT, 'brand-assets', '06_Templates')
for pdf, prefix in ((os.path.join(T, 'Word', 'Previews', 'VCCI_Report.pdf'), 'tpl_report'),
                    (os.path.join(T, 'Word', 'Previews', 'VCCI_Letterhead.pdf'), 'tpl_letter'),
                    (os.path.join(T, 'Word', 'Previews', 'VCCI_Invitation.pdf'), 'tpl_invite'),
                    (os.path.join(T, 'PowerPoint', 'Previews', 'VCCI_Presentation.pdf'), 'ppt')):
    subprocess.run([PDFTOPPM, '-png', '-r', '80' if prefix == 'ppt' else '110', pdf, os.path.join(IMG, prefix)], check=True)
print('guide images ->', IMG, len(os.listdir(IMG)), 'files')
