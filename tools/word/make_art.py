"""Render background artwork PNGs for the Word templates (A4 at 200 dpi)."""
import os, sys, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets'))
import build_assets as BA

ROOT = os.getcwd(); OUT = os.path.join(ROOT, 'build', 'word', 'art'); os.makedirs(OUT, exist_ok=True)
DPI = 200; MM = DPI / 25.4
A4W, A4H = round(210 * MM), round(297 * MM)   # 1654 x 2339
LOGO = 'file:///' + os.path.join(ROOT, 'brand-assets', '01_Logo', 'SVG', 'VCCI_Logo_Primary.svg').replace(os.sep, '/')

def render(name, w, h, body, transparent=False):
    html = os.path.join(OUT, f'_{name}.html')   # one page per image
    open(html, 'w', encoding='utf-8').write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;'
        f'background:{"transparent" if transparent else "#fff"}}}</style></head><body>{body}</body></html>')
    out = os.path.join(OUT, name)
    args = ['--force-device-scale-factor=1', f'--window-size={w},{h}', '--virtual-time-budget=3000', f'--screenshot={out}']
    if transparent: args.insert(1, '--default-background-color=00000000')
    BA.env.run_edge(args + ['file:///' + html.replace(os.sep, '/')])
    print(name)

def ring_svg(size, c, g, w, op, gop, style):
    return (f'<svg viewBox="-300 -300 600 600" style="position:absolute;width:{size}px;height:{size}px;{style}">'
            f'{BA.drum(c, g, w, op, gop)}</svg>')

B, GOLD, PAPER = BA.BLUE, BA.GOLD, BA.PAPER
split = round(178 * MM)   # blue field starts 178 mm from top

# 1. Report cover: paper top, VCCI Blue field below with drum-ring line art; one gold rule.
render('cover.png', A4W, A4H,
       f'<div style="position:absolute;inset:0;background:{PAPER}"></div>'
       f'<div style="position:absolute;left:0;right:0;top:{split}px;bottom:0;background:linear-gradient(160deg,#2B4FA0,#1E3D86);overflow:hidden">'
       + ring_svg(round(250 * MM), '#fff', GOLD, .55, .16, .55, f'right:{round(-62*MM)}px;top:{round(-40*MM)}px') +
       f'</div><div style="position:absolute;left:{round(22*MM)}px;top:{split + round(20*MM)}px;width:{round(16*MM)}px;height:{round(.9*MM)}px;background:{GOLD}"></div>')

# 2. Back cover: full blue with a Paper plate carrying the logo (logo never sits directly on blue).
pw = round(166 * MM); ph = round(70 * MM); px = round(22 * MM); py = round(200 * MM)
lw = round(70 * MM); pad = round(lw / 3.3217 * 0.262)
render('back.png', A4W, A4H,
       f'<div style="position:absolute;inset:0;background:linear-gradient(160deg,#2B4FA0,#1E3D86);overflow:hidden">'
       + ring_svg(round(300 * MM), '#fff', GOLD, .5, .13, .45, f'left:{round(-40*MM)}px;top:{round(-60*MM)}px') +
       f'</div><div style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;background:{PAPER};border-radius:{round(1*MM)}px"></div>'
       f'<img src="{LOGO}" style="position:absolute;left:{px + pad + round(8*MM)}px;top:{py + round(10*MM)}px;width:{lw}px">')

# 3. Letterhead watermark: faint drum ring, bottom-right corner (transparent PNG, 90 x 90 mm).
s = round(90 * MM)
render('watermark.png', s, s, ring_svg(round(140 * MM), B, B, .9, .10, .10, f'left:0;top:0'), transparent=True)

# 4. Invitation footer band: 210 x 30 mm, blue with drum-dot field and a gold rule.
bw, bh = A4W, round(30 * MM)
dots = BA.dot_field(bw, bh * 3)
render('band.png', bw, bh,
       f'<div style="position:absolute;inset:0;background:linear-gradient(90deg,#2B4FA0,#1E3D86);overflow:hidden">'
       f'<svg viewBox="0 {bh*2} {bw} {bh}" style="position:absolute;inset:0;width:{bw}px;height:{bh}px;opacity:.35">{dots}</svg></div>'
       f'<div style="position:absolute;left:{round(22*MM)}px;top:0;width:{round(16*MM)}px;height:{round(.9*MM)}px;background:{GOLD}"></div>')

# 5. Chapter opener strip for reports: 210 x 60 mm, blue with C-arc pattern on the right.
cw, ch = A4W, round(60 * MM)
render('chapter.png', cw, ch,
       f'<div style="position:absolute;inset:0;background:linear-gradient(90deg,#2B4FA0,#1E3D86)"></div>'
       f'<svg viewBox="0 0 {round(70*MM)} {ch}" style="position:absolute;right:0;top:0;width:{round(70*MM)}px;height:{ch}px;opacity:.9">'
       f'{BA.arc_pattern(round(70*MM), ch, round(ch/4), 7, fg="#3A5FB4")}</svg>')

# 6. Sample chart for the report template (brand colours; one gold highlight) and the gold rule image
CW, CH = 1600, 820
vals = [('2021', 63.2), ('2022', 64.5), ('2023', 65.1), ('2024', 66.0), ('2025', 67.4)]
mx, mn, x0, bw, gap, base, top = 80, 0, 150, 170, 110, 700, 90
yv = lambda v: base - (v - mn) / (mx - mn) * (base - top)
bars = ''.join(
    f'<rect x="{x0 + i * (bw + gap)}" y="{yv(v)}" width="{bw}" height="{base - yv(v)}" fill="{GOLD if i == len(vals) - 1 else B}"/>'
    f'<text x="{x0 + i * (bw + gap) + bw / 2}" y="{yv(v) - 22}" text-anchor="middle" font-family="Lora" font-size="38" fill="{B}">{v:.1f}</text>'
    f'<text x="{x0 + i * (bw + gap) + bw / 2}" y="{base + 56}" text-anchor="middle" font-family="BVP" font-size="30" fill="#5C6478">{y}</text>'
    for i, (y, v) in enumerate(vals))
grid = ''.join(f'<line x1="110" x2="1560" y1="{yv(g)}" y2="{yv(g)}" stroke="#E6E1D5" stroke-width="2"/>'
               f'<text x="96" y="{yv(g) + 10}" text-anchor="end" font-family="BVP" font-size="26" fill="#5C6478">{g}</text>' for g in (0, 20, 40, 60, 80))
FONTS_URL = 'file:///' + os.path.join(ROOT, 'brand-assets', '03_Fonts').replace(os.sep, '/').replace(' ', '%20')
render('chart.png', CW, CH,
       f'<style>@font-face{{font-family:Lora;src:url({FONTS_URL}/Lora/Lora-Medium.ttf)}}'
       f'@font-face{{font-family:BVP;src:url({FONTS_URL}/BeVietnamPro/BeVietnamPro-Regular.ttf)}}</style>'
       f'<svg width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}"><rect width="{CW}" height="{CH}" fill="#fff"/>{grid}'
       f'<line x1="110" x2="1560" y1="{base}" y2="{base}" stroke="#5C6478" stroke-width="2"/>{bars}</svg>')
from PIL import Image
import json
Image.new('RGB', (320, 18), (255, 205, 0)).save(os.path.join(OUT, 'gold_rule.png'))
logos = {'lockup': 'VCCI_Lockup_Horizontal_VI-EN_2400px.png', 'logo': 'VCCI_Logo_Primary_1200px.png'}
json.dump({k: Image.open(os.path.join(ROOT, 'brand-assets', '01_Logo', 'PNG', f)).size for k, f in logos.items()},
          open(os.path.join(OUT, 'dims.json'), 'w'))
print('word art ok')
