"""Background artwork for the VCCI PowerPoint template (16:9, 13.333 x 7.5 in at 150 dpi)."""
import os, sys, subprocess, types
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets'))
import build_assets as BA

OUT = os.path.join(os.getcwd(), 'build', 'ppt', 'art'); os.makedirs(OUT, exist_ok=True)

def render(name, w, h, body):
    html = os.path.join(OUT, f'_{name}.html')   # one page per image
    open(html, 'w', encoding='utf-8').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;width:{w}px;'
                                            f'height:{h}px;overflow:hidden}}</style></head><body>{body}</body></html>')
    BA.env.run_edge(['--force-device-scale-factor=1', f'--window-size={w},{h}', '--virtual-time-budget=3000',
                    f'--screenshot={os.path.join(OUT, name)}', 'file:///' + html.replace(os.sep, '/')])
WA = types.SimpleNamespace(render=render)
W, H = 2000, 1125                    # 150 dpi
IN = 150                             # px per inch
GRAD = 'linear-gradient(160deg,#2B4FA0,#1E3D86)'

def ring(cx_in, cy_in, d_in, w=.55, op=.16, gop=.55):
    d = d_in * IN
    return (f'<svg viewBox="-300 -300 600 600" style="position:absolute;width:{d}px;height:{d}px;'
            f'left:{cx_in * IN - d / 2}px;top:{cy_in * IN - d / 2}px">{BA.drum("#fff", BA.GOLD, w, op, gop)}</svg>')

def blue(name, *rings, extra=''):
    WA.render(name, W, H, f'<div style="position:absolute;inset:0;background:{GRAD};overflow:hidden">{"".join(rings)}</div>{extra}')

# light cover: paper left, blue panel right with ring
WA.render('cover_light.png', W, H,
          f'<div style="position:absolute;inset:0;background:{BA.PAPER}"></div>'
          f'<div style="position:absolute;left:{8.4 * IN}px;right:0;top:0;bottom:0;background:{GRAD};overflow:hidden">'
          f'<div style="position:absolute;left:{-8.4 * IN}px;top:0;width:{W}px;height:{H}px">{ring(11.2, 3.2, 8.5)}</div></div>')
blue('blue_event.png', ring(10.6, 3.6, 10.5, op=.15, gop=.5))                 # event cover
blue('blue_section.png', ring(10.75, 3.75, 6.4, op=.18, gop=.6))              # section divider, ring around icon slot
blue('blue_plain.png', ring(12.6, 7.3, 6.0, op=.12, gop=.35))                 # KPI / statement / quote / photo band
blue('blue_closing.png', ring(2.2, 3.2, 9.5, op=.14, gop=.45),
     extra=f'<div style="position:absolute;left:{6.9 * IN}px;top:{3.65 * IN}px;width:{5.63 * IN}px;height:{3.05 * IN}px;'
           f'background:{BA.PAPER};border-radius:{.06 * IN}px"></div>')
print('art ok')
