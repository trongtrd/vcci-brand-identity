"""Build the VCCI brand asset package (brand-assets/) from the master SVG decoded from Logo_VCCI.cdr.

Run from the repository root:  python tools/assets/build_assets.py           (everything)
                                python tools/assets/build_assets.py colours   (02_Colour only, no Edge needed)
The master SVG comes from tools/cdr (build/logo/); without it, the committed brand-assets copy is reused.
"""
import json, math, os, re, shutil, struct, subprocess, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import env
import colour_system as CS

ROOT = os.getcwd()
OUT = os.path.join(ROOT, 'brand-assets')
FONTS = os.path.join(ROOT, 'brand-assets', '03_Fonts')
EDGE = env.EDGE
def _master(built, committed):
    p = env.build('logo', built, mkdir=False)
    return open(p if os.path.exists(p) else os.path.join(ROOT, 'brand-assets', '01_Logo', *committed), encoding='utf-8').read()

# ---------------------------------------------------------------- palette
PALETTE = [
    # name, role, hex, cmyk, source
    ('VCCI Blue',   'primary',   '#264896', (100, 80, 0, 0),   'Master .CDR (logo letters)'),
    ('Drum Gold',   'secondary', '#FFCD00', (0, 20, 100, 0),   'Master .CDR (drum)'),
    ('Drum Bronze', 'secondary', '#CC713C', (0, 60, 80, 20),   'Master .CDR (drum figures)'),
    ('Deep Navy',   'support',   '#0B1A4F', (100, 90, 30, 40), 'Brand system'),
    ('Blue Tint',   'support',   '#E7ECF6', (8, 4, 0, 0),      'Brand system'),
    ('Sky',         'support',   '#8FA6D6', (45, 28, 0, 0),    'Brand system (chart series 2, light blue fields)'),
    ('Bronze Ink',  'support',   '#9C570C', (20, 65, 100, 15), 'Brand system (text-safe bronze)'),
    ('Ink',         'neutral',   '#161A26', (75, 65, 50, 70),  'Brand system'),
    ('Slate',       'neutral',   '#5C6478', (62, 50, 32, 12),  'Brand system'),
    ('Stone',       'neutral',   '#E6E1D5', (9, 8, 15, 0),     'Brand system'),
    ('Ivory',       'neutral',   '#F4F0E6', (3, 4, 9, 0),      'Brand system'),
    ('Paper',       'neutral',   '#FBF9F4', (1, 2, 4, 0),      'Brand system'),
]
HEX = {p[0]: p[2] for p in PALETTE}
BLUE, GOLD, BRONZE, SLATE, PAPER = HEX['VCCI Blue'], HEX['Drum Gold'], HEX['Drum Bronze'], HEX['Slate'], HEX['Paper']

def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

# ---------------------------------------------------------------- master logo
MASTER = _master('vcci-logo.svg', ('SVG', 'VCCI_Logo_Primary.svg'))
DRUM = _master('vcci-drum.svg', ('_Construction-only', 'VCCI_Drum_CONSTRUCTION-ONLY.svg'))
LW, LH = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', MASTER).groups())  # 3321.68 x 1000
LOGO_INNER = re.search(r'<svg[^>]*>(.*)</svg>', MASTER, re.S).group(1)
X = 262.0  # clear-space unit = drum radius (cap height = 1000)

def svg_doc(w, h, body, vb=None):
    vb = vb or f'0 0 {w:.2f} {h:.2f}'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w:.0f}" height="{h:.0f}">{body}</svg>'

# ---------------------------------------------------------------- text to outlines
class Face:
    def __init__(self, path):
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upem = self.tt['head'].unitsPerEm
        blob = hb.Blob.from_file_path(path)
        self.hbfont = hb.Font(hb.Face(blob))
        os2 = self.tt['OS/2']
        self.cap = getattr(os2, 'sCapHeight', 0.7 * self.upem) or 0.7 * self.upem

    def run(self, text, size, tracking=0.0):
        """Return (svg path d, advance width) for text at size with baseline at y=0."""
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {'kern': True, 'liga': True})
        s = size / self.upem; x = 0.0; d = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.order[info.codepoint]
            pen = SVGPathPen(self.gs)
            tp = TransformPen(pen, (s, 0, 0, -s, x + pos.x_offset * s, -pos.y_offset * s))
            self.gs[name].draw(tp)
            d.append(pen.getCommands())
            x += pos.x_advance * s + tracking * size
        return ' '.join(d), x - tracking * size

BVP_SB = Face(os.path.join(FONTS, 'BeVietnamPro', 'BeVietnamPro-SemiBold.ttf'))
LORA_I = Face(os.path.join(FONTS, 'Lora', 'Lora-Italic.ttf'))

VI1, VI2 = 'Liên đoàn Thương mại và', 'Công nghiệp Việt Nam'
EN = 'Vietnam Chamber of Commerce and Industry'

def lockup_horizontal(plate=False):
    rule_x = LW + X; text_x = rule_x + 16 + X
    s1, s2 = 176, 158
    d1, w1 = BVP_SB.run(VI1, s1, 0.005); d2, w2 = BVP_SB.run(VI2, s1, 0.005); d3, w3 = LORA_I.run(EN, s2)
    cap = BVP_SB.cap / BVP_SB.upem * s1
    lh = s1 * 1.34
    block_h = cap + lh + s2 * 1.55              # cap-top of line 1 to baseline of EN line
    top = (LH - block_h) / 2
    b1 = top + cap; b2 = b1 + lh; b3 = b2 + s2 * 1.55
    W = text_x + max(w1, w2, w3)
    body = LOGO_INNER
    body += f'<rect x="{rule_x:.1f}" y="70" width="16" height="860" fill="{BLUE}"/>'
    body += f'<path fill="{BLUE}" transform="translate({text_x:.1f},{b1:.1f})" d="{d1}"/>'
    body += f'<path fill="{BLUE}" transform="translate({text_x:.1f},{b2:.1f})" d="{d2}"/>'
    body += f'<path fill="{SLATE}" transform="translate({text_x:.1f},{b3:.1f})" d="{d3}"/>'
    return wrap_plate(W, LH, body) if plate else svg_doc(W, LH, body)

def lockup_stacked(lines, plate=False):
    size, track = 150, 0.20
    runs = [BVP_SB.run(t, size, track) for t in lines]
    tw = max(w for _, w in runs)
    W = max(LW, tw)
    cap = BVP_SB.cap / BVP_SB.upem * size
    lx = (W - LW) / 2
    body = f'<g transform="translate({lx:.1f},0)">{LOGO_INNER}</g>'
    rule_y = LH + X
    body += f'<rect x="{W/2-260:.1f}" y="{rule_y:.1f}" width="520" height="22" fill="{GOLD}"/>'
    y = rule_y + 22 + 190 + cap
    for d, w in runs:
        body += f'<path fill="{BLUE}" transform="translate({(W-w)/2:.1f},{y:.1f})" d="{d}"/>'
        y += size * 1.62
    H = y - size * 1.62 + size * 0.3
    return wrap_plate(W, H, body) if plate else svg_doc(W, H, body)

def wrap_plate(w, h, body):
    """Logo on a Paper plate; padding = x on all sides (for use on dark or busy fields)."""
    P = X
    W, H = w + 2 * P, h + 2 * P
    inner = f'<rect width="{W:.1f}" height="{H:.1f}" rx="30" fill="{PAPER}"/><g transform="translate({P},{P})">{body}</g>'
    return svg_doc(W, H, inner)

# ---------------------------------------------------------------- graphics (ported from the board)
def P(a, r): return (math.cos(a) * r, math.sin(a) * r)

def star_pts(R, r, n=14, rot=0.0):
    return ' '.join(f'{P(rot + i * math.pi / n, r if i % 2 else R)[0]:.2f},{P(rot + i * math.pi / n, r if i % 2 else R)[1]:.2f}' for i in range(2 * n))

def drum(c='#fff', g=GOLD, w=1.0, op=1.0, gop=1.0, R=280):
    s = f'<g fill="none" stroke="{c}" stroke-width="{w}" opacity="{op}">'
    for k in (1, .965, .93, .78, .76, .72): s += f'<circle r="{R*k:.2f}"/>'
    for n, r1, r2 in ((144, .93, .965), (96, .72, .76)):
        for i in range(n):
            a = i * 2 * math.pi / n; x1, y1 = P(a, R * r1); x2, y2 = P(a, R * r2)
            s += f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/>'
    s += f'</g><g fill="{c}" opacity="{op}">'
    for i in range(72):
        x, y = P(i * 2 * math.pi / 72 + .04, R * .855); s += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{1.6*w:.2f}"/>'
    s += f'</g><g fill="none" stroke="{g}" stroke-width="{w*1.2:.2f}" opacity="{gop}"><polygon points="{star_pts(R*.62, R*.2)}"/><circle r="{R*.13:.2f}"/></g><g fill="{g}" opacity="{gop}">'
    for i in range(14):
        a = (i + .5) * 2 * math.pi / 14
        for k, dd in ((.5, 0), (.44, -.05), (.44, .05)):
            x, y = P(a + dd, R * k); s += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{2.2*w:.2f}"/>'
    return s + '</g>'

def radiance(col=BLUE):
    s = f'<g fill="none" stroke="{col}">'
    s += f'<polygon points="{star_pts(250,70)}" stroke-width="2.2"/><polygon points="{star_pts(190,56)}" stroke-width="1.2" opacity=".55"/>'
    s += f'<polygon points="{star_pts(130,40)}" stroke-width="1" opacity=".35"/><circle r="34" stroke-width="2.2"/>'
    s += '<circle r="268" stroke-width="1" opacity=".4"/><circle r="282" stroke-width="1" opacity=".25"/>'
    for i in range(14):
        a = (i + .5) * 2 * math.pi / 14; x1, y1 = P(a, 96); x2, y2 = P(a, 268)
        s += f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke-width=".8" opacity=".3"/>'
    return s + f'</g><circle r="34" fill="{col}"/>'

def carc(R):
    ri, cx = R * .6, R * .35; yo = math.sqrt(R * R - cx * cx); yi = math.sqrt(ri * ri - cx * cx)
    return f'M{cx:.2f},{-yo:.2f} A{R:.2f},{R:.2f} 0 1 0 {cx:.2f},{yo:.2f} L{cx:.2f},{yi:.2f} A{ri:.2f},{ri:.2f} 0 1 1 {cx:.2f},{-yi:.2f} Z'

def arc_pattern(W, H, T, gold_every, fg=BLUE):
    R = T * .42; rots = [0, 90, 180, 270, 180, 270, 0, 90]; s = ''
    for y in range(int(H / T) + 1):
        for x in range(int(W / T) + 1):
            r = rots[(x * 3 + y * 5) % 8]; cx, cy = x * T + T / 2, y * T + T / 2
            s += f'<g transform="translate({cx},{cy}) rotate({r})"><path d="{carc(R)}" fill="{fg}"/>'
            if (x * 7 + y * 3) % gold_every == 0: s += f'<circle r="{R*.6-1:.2f}" fill="{GOLD}"/>'
            s += '</g>'
    return s

def dot_field(W, H):
    s = ''; cx, cy = -40, H + 40
    for ring in range(1, 40):
        r = ring * 28; n = round(r * 2 * math.pi / 18)
        for i in range(n):
            a = -math.pi / 2 + i * 2 * math.pi / n; x = cx + math.cos(a) * r; y = cy + math.sin(a) * r
            if x < -5 or x > W + 5 or y < -5 or y > H + 5: continue
            gold = ring % 6 == 3; sz = 4 if gold else max(2.4 - ring * .04, 1.2)
            s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{sz:.2f}" fill="{GOLD if gold else BLUE}" opacity="{1 if gold else .75}"/>'
    return s

# ---------------------------------------------------------------- rasterise / pdf via Edge
def edge(args):
    env.run_edge(args)

def to_png(svg_path, png_base, widths=(600, 1200, 2400, 4800)):
    src = open(svg_path, encoding='utf-8').read()
    vw, vh = map(float, re.search(r'viewBox="[\d.-]+ [\d.-]+ ([\d.]+) ([\d.]+)"', src).groups())
    big = max(widths); bh = round(big * vh / vw)
    html = env.build('assets', f'_r_{os.path.basename(png_base)}.html')
    open(html, 'w', encoding='utf-8').write(
        f'<!doctype html><html><body style="margin:0;background:transparent">'
        f'<img src="file:///{svg_path.replace(os.sep, "/")}" style="display:block;width:{big}px;height:{bh}px"></body></html>')
    tmp = env.build('assets', f'_r_{os.path.basename(png_base)}.png')
    edge(['--default-background-color=00000000', '--force-device-scale-factor=1', f'--window-size={big},{bh}',
          '--virtual-time-budget=3000', f'--screenshot={tmp}', 'file:///' + html.replace(os.sep, '/')])
    im = Image.open(tmp).convert('RGBA').crop((0, 0, big, bh))
    for w in widths:
        h = round(w * vh / vw)
        im.resize((w, h), Image.LANCZOS).save(f'{png_base}_{w}px.png', optimize=True)

def to_pdf(svg_path, pdf_path):
    src = open(svg_path, encoding='utf-8').read()
    vw, vh = map(float, re.search(r'viewBox="[\d.-]+ [\d.-]+ ([\d.]+) ([\d.]+)"', src).groups())
    wmm = 100.0; hmm = wmm * vh / vw    # 100 mm wide artboard, scales losslessly (vector)
    html = env.build('assets', f'_p_{os.path.basename(pdf_path)}.html')
    open(html, 'w', encoding='utf-8').write(
        f'<!doctype html><html><head><style>@page{{size:{wmm}mm {hmm:.3f}mm;margin:0}}html,body{{margin:0}}'
        f'img{{display:block;width:{wmm}mm;height:{hmm:.3f}mm}}</style></head><body>'
        f'<img src="file:///{svg_path.replace(os.sep, "/")}"></body></html>')
    edge(['--no-pdf-header-footer', '--virtual-time-budget=3000', f'--print-to-pdf={pdf_path}', 'file:///' + html.replace(os.sep, '/')])

# ---------------------------------------------------------------- colour files
def ase(path, groups):
    """Adobe Swatch Exchange in named groups: logo colours as CMYK process, everything else as RGB."""
    def name_bytes(n):
        nm = (n + '\0').encode('utf-16-be')
        return struct.pack('>H', len(nm) // 2) + nm
    blocks, count = b'', 0
    for group, swatches in groups:
        g = name_bytes(group)
        blocks += struct.pack('>HI', 0xC001, len(g)) + g; count += 1
        for name, h, cmyk in swatches:
            if cmyk:
                model, vals = b'CMYK', struct.pack('>4f', *[v / 100 for v in cmyk])
            else:
                model, vals = b'RGB ', struct.pack('>3f', *[v / 255 for v in rgb(h)])
            body = name_bytes(name) + model + vals + struct.pack('>H', 2)
            blocks += struct.pack('>HI', 0x0001, len(body)) + body; count += 1
        blocks += struct.pack('>HI', 0xC002, 0); count += 1
    open(path, 'wb').write(b'ASEF' + struct.pack('>HHI', 1, 0, count) + blocks)

def office_theme(path):
    scheme = CS.office_clr_scheme().replace('<a:clrScheme ', '<a:clrScheme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" ', 1)
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + re.sub(r'(<a:(?!clrScheme)\w+>)', r'\n  \1', scheme).replace('</a:clrScheme>', '\n</a:clrScheme>\n')
    open(path, 'w', encoding='utf-8').write(xml)

def colour_files(col):
    """02_Colour: core palette plus the extended system (tonal scales, status colours, chart palettes)."""
    scales, status, dv = CS.system()
    bad = CS.check(scales, status)
    assert not bad, f'contrast rule broken: {bad[:5]}'
    tok = json.load(open(os.path.join(OUT, 'brand-tokens.json'), encoding='utf-8'))   # hand-maintained copy must match
    assert {k: {kk.split('-')[1]: h for kk, h in v.items()} for k, v in ((n.lower(), v) for n, v in scales.items())} ==            {k: v for k, v in tok['colour']['scales'].items() if k != 'note'}, 'brand-tokens.json colour.scales out of date'
    assert [list(c) for c in dv['categorical']] == tok['dataviz']['categorical'], 'brand-tokens.json dataviz out of date'
    assert all(tok['colour']['status'][n]['strong'] == v['strong'] and tok['colour']['status'][n]['background'] == v['background']
               for n, v in status.items()), 'brand-tokens.json colour.status out of date'
    slug = lambda n: n.lower().replace(' ', '-')
    json.dump({'palette': [dict(name=n, role=r, hex=h, rgb=list(rgb(h)), cmyk=list(c), grade=CS.brand_grade(n), source=s)
                           for n, r, h, c, s in PALETTE],
               'contrast': {'Paper on VCCI Blue': '8.1:1 AAA', 'Drum Gold on VCCI Blue': '5.7:1 AA', 'Bronze Ink on Paper': '5.3:1 AA',
                            'Drum Bronze on Paper': '3.3:1 (graphics / large text only)'},
               'balance_percent': {'VCCI Blue': 44, 'Paper': 34, 'Stone': 10, 'Drum Gold': 7, 'Drum Bronze': 5},
               'grade_rule': 'Grade 0 = white, 100 = near black. Grade difference >= 40: 3:1 (large text, graphics); '
                             '>= 50: 4.5:1 (AA body text); >= 70: 7:1 (AAA).',
               'scales': scales,
               'status': status,
               'dataviz': {'categorical': [dict(name=n, hex=h) for n, h in dv['categorical']], 'highlight': dv['highlight'],
                           'sequential_7': dv['sequential_7'], 'sequential_5': dv['sequential_5'], 'diverging_7': dv['diverging_7']},
               'screen_conversion': 'CMYK -> sRGB via Coated FOGRA39, relative colorimetric. Scales, status and chart colours are '
                                    'defined in sRGB only; for offset print ask the printer to convert and proof.'},
              open(os.path.join(col, 'VCCI_Colours.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    css = ':root{\n  /* core palette */\n'
    css += ''.join(f'  --vcci-{slug(n)}: {h};  /* CMYK {"/".join(map(str, c))} · grade {CS.brand_grade(n)} */\n' for n, _, h, c, _ in PALETTE)
    css += '  /* tonal scales: grade difference >= 50 between text and background = 4.5:1 */\n'
    css += ''.join(f'  --vcci-{k}: {h};\n' for sc in scales.values() for k, h in sc.items())
    css += '  /* status: strong = text, icons, borders; -bg = background */\n'
    css += ''.join(f'  --vcci-{slug(n)}: {v["strong"]};\n  --vcci-{slug(n)}-bg: {v["background"]};\n' for n, v in status.items())
    css += '  /* charts: categorical series in this order; gold only for one highlighted value */\n'
    css += ''.join(f'  --vcci-chart-{i}: {h};  /* {n} */\n' for i, (n, h) in enumerate(dv['categorical'], 1))
    css += f'  --vcci-chart-highlight: {dv["highlight"]["focus"]};\n  --vcci-chart-muted: {dv["highlight"]["muted"]};\n'
    css += ''.join(f'  --vcci-seq-{i}: {h};\n' for i, h in enumerate(dv['sequential_7'], 1))
    css += ''.join(f'  --vcci-div-{i}: {h};\n' for i, h in enumerate(dv['diverging_7'], 1))
    css += '}\n'
    open(os.path.join(col, 'VCCI_Colours.css'), 'w', encoding='utf-8').write(css)
    master = {n: c for n, _, _, c, src in PALETTE if src.startswith('Master')}
    ase(os.path.join(col, 'VCCI_Colours.ase'), [
        ('VCCI Core', [(n, h, master.get(n)) for n, _, h, _, _ in PALETTE]),
        ('VCCI Scales', [(k.replace('-', ' ').title(), h, None) for sc in scales.values() for k, h in sc.items()]),
        ('VCCI Status', [(f'{n} {part}'.strip(), v[key], None) for n, v in status.items() for part, key in (('', 'strong'), ('BG', 'background'))]),
        ('VCCI Charts', [(f'Chart {i} {n}', h, None) for i, (n, h) in enumerate(dv['categorical'], 1)]
                        + [(f'Sequential {i}', h, None) for i, h in enumerate(dv['sequential_7'], 1)]
                        + [(f'Diverging {i}', h, None) for i, h in enumerate(dv['diverging_7'], 1)]),
    ])
    office_theme(os.path.join(col, 'VCCI_Office_Theme_Colours.xml'))

# ---------------------------------------------------------------- main
def main():
    # regenerate generated folders only; README.md, brand-tokens.json and font licences are hand-maintained
    for sub in ('01_Logo', '02_Colour', '04_Graphics'):
        if os.path.exists(os.path.join(OUT, sub)): shutil.rmtree(os.path.join(OUT, sub))
    d = lambda *p: os.makedirs(os.path.join(OUT, *p), exist_ok=True) or os.path.join(OUT, *p)
    logo_svg, logo_png, logo_pdf = d('01_Logo', 'SVG'), d('01_Logo', 'PNG'), d('01_Logo', 'PDF')
    src_dir, cons_dir = d('01_Logo', 'Source'), d('01_Logo', '_Construction-only')

    logos = {
        'VCCI_Logo_Primary': MASTER,
        'VCCI_Logo_Primary_Plate': wrap_plate(LW, LH, LOGO_INNER),
        'VCCI_Lockup_Horizontal_VI-EN': lockup_horizontal(),
        'VCCI_Lockup_Horizontal_VI-EN_Plate': lockup_horizontal(plate=True),
        'VCCI_Lockup_Stacked_VI': lockup_stacked(['LIÊN ĐOÀN THƯƠNG MẠI VÀ', 'CÔNG NGHIỆP VIỆT NAM']),
        'VCCI_Lockup_Stacked_EN': lockup_stacked(['VIETNAM CHAMBER OF', 'COMMERCE AND INDUSTRY']),
    }
    for name, svg in logos.items():
        sp = os.path.join(logo_svg, name + '.svg'); open(sp, 'w', encoding='utf-8').write(svg)
        to_png(sp, os.path.join(logo_png, name))
        to_pdf(sp, os.path.join(logo_pdf, name + '.pdf'))
        print('logo', name)
    shutil.copy(os.path.join(ROOT, 'source', 'logo', 'Logo_VCCI.cdr'), os.path.join(src_dir, 'VCCI_Logo_Master_CMYK.cdr'))
    open(os.path.join(cons_dir, 'VCCI_Drum_CONSTRUCTION-ONLY.svg'), 'w', encoding='utf-8').write(DRUM)

    colour_files(d('02_Colour'))

    # 03_Fonts is maintained by hand (font files + OFL licences)

    g = d('04_Graphics')
    graphics = {
        'VCCI_Drum-Ring_Line_Gold-on-Blue': (600, 600, f'<rect x="-300" y="-300" width="600" height="600" fill="{BLUE}"/>' + drum('#fff', GOLD, .9, .22, .75), '-300 -300 600 600'),
        'VCCI_Drum-Ring_Line_Transparent_Blue': (600, 600, drum(BLUE, GOLD, .9, .35, .9), '-300 -300 600 600'),
        'VCCI_Radiance-14_Blue': (600, 600, radiance(BLUE), '-300 -300 600 600'),
        'VCCI_C-Arc_Pattern_Tile': (704, 704, f'<rect width="704" height="704" fill="{HEX["Ivory"]}"/>' + arc_pattern(704, 704, 88, 5), None),
        'VCCI_Drum-Dot_Field': (600, 900, dot_field(600, 900), None),
    }
    for name, (w, h, body, vb) in graphics.items():
        sp = os.path.join(g, name + '.svg'); open(sp, 'w', encoding='utf-8').write(svg_doc(w, h, body, vb))
        to_png(sp, os.path.join(g, name), widths=(2000,))
        print('graphic', name)
    print('done')

if __name__ == '__main__':
    if sys.argv[1:] == ['colours']:
        col = os.path.join(OUT, '02_Colour'); os.makedirs(col, exist_ok=True)
        colour_files(col); print('colours ->', col)
    else:
        main()
