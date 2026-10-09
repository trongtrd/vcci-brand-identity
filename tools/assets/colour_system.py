"""VCCI extended colour system: tonal scales with contrast grades, status colours and data-visualisation palettes.

Grade (0 = white, 100 = near black) is defined from WCAG relative luminance Y:
    grade(Y) = 50 * log(1.05 / (Y + 0.05)) / log(4.6)
so the contrast ratio of two colours is 4.6 ** (grade difference / 50):
    difference >= 40 -> 3:1 (large text, graphics), >= 50 -> 4.5:1 (AA text), >= 70 -> 7:1 (AAA text).
Scale steps are solved in OKLCH (hue and chroma of the anchor colour, lightness searched until the
luminance hits the target grade). Brand colours keep their exact values and are reported with their own grade.

Run directly to print the system and check every contrast claim:  python tools/assets/colour_system.py
"""
import math

# ---------------------------------------------------------------- colour maths (sRGB <-> OKLab)
def hex2rgb(h): return tuple(int(h.lstrip('#')[i:i + 2], 16) / 255 for i in (0, 2, 4))
def rgb2hex(c): return '#' + ''.join(f'{round(min(1, max(0, v)) * 255):02X}' for v in c)
def lin(v): return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
def delin(v): return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055

def luminance(h):
    r, g, b = map(lin, hex2rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

K = 4.6   # contrast per 50 grades; slightly above 4.5 so that rounding to hex never breaks the rule
def grade(h): return 50 * math.log(1.05 / (luminance(h) + 0.05)) / math.log(K)
def target_y(g): return 1.05 * K ** (-g / 50) - 0.05

def to_oklch(h):
    r, g, b = map(lin, hex2rgb(h))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360

def oklch_rgb(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)

def in_gamut(c): return all(-1e-6 <= v <= 1 + 1e-6 for v in c)

def solve(H, C, g):
    """Colour with hue H, chroma as close to C as the sRGB gamut allows, and luminance at grade g."""
    ty = target_y(g)
    lo, hi = 0.0, 1.0
    for _ in range(60):                       # lightness search; chroma reduced until in gamut
        L = (lo + hi) / 2
        c = C
        while c > 0 and not in_gamut(oklch_rgb(L, c, H)): c -= 0.002
        rgb = oklch_rgb(L, max(c, 0), H)
        y = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]   # rgb is linear here
        lo, hi = (L, hi) if y < ty else (lo, L)
    return rgb2hex([delin(min(1, max(0, v))) for v in rgb])

# ---------------------------------------------------------------- definitions
STEPS = (5, 10, 20, 30, 40, 50, 60, 70, 80, 90)

def family(anchor, chroma_scale=1.0, hue=None, peak=None):
    """Scale in the hue of `anchor`. Chroma follows the anchor, tapering towards white and black."""
    L0, C0, H0 = to_oklch(anchor)
    H = H0 if hue is None else hue
    peak = grade(anchor) if peak is None else peak
    out = {}
    for g in STEPS:
        # lighter than the anchor: chroma fades towards white (keeps tints calm, like Sky); darker: gentle taper
        taper = (g / peak) ** 0.55 if g < peak else 1 - ((g - peak) / 100) ** 1.6
        out[g] = solve(H, C0 * chroma_scale * max(taper, 0.15), g)
    return out

# Core palette (v1.0 colours plus Sky, which was already accent 5 of the Office theme and the second chart series).
BRAND = {
    'VCCI Blue': '#264896', 'Drum Gold': '#FFCD00', 'Drum Bronze': '#CC713C', 'Deep Navy': '#0B1A4F', 'Blue Tint': '#E7ECF6',
    'Sky': '#8FA6D6', 'Bronze Ink': '#9C570C', 'Ink': '#161A26', 'Slate': '#5C6478', 'Stone': '#E6E1D5', 'Ivory': '#F4F0E6',
    'Paper': '#FBF9F4',
}
def brand_grade(name):
    """Published grade of a brand colour: its step number when it is a step of a scale (Sky = Blue 30), else rounded."""
    for sc in build_scales().values():
        for k, h in sc.items():
            if h == BRAND[name]: return int(k.split('-')[1])
    return round(grade(BRAND[name]))

# Tonal scales. A brand colour of the family replaces the computed step when its grade is within 1 of the step.
SCALES = {
    'Blue':   {'anchor': '#264896', 'steps': STEPS, 'members': ('VCCI Blue', 'Deep Navy', 'Blue Tint', 'Sky')},
    'Gold':   {'anchor': '#FFCD00', 'steps': (5, 10, 20), 'peak': 10, 'members': ('Drum Gold',)},   # darker yellows turn olive
    'Bronze': {'anchor': '#CC713C', 'steps': STEPS, 'members': ('Drum Bronze', 'Bronze Ink')},
    'Slate':  {'anchor': '#5C6478', 'steps': STEPS, 'members': ('Slate', 'Ink')},   # cool grey: text, rules, muted data
}

def build_scales():
    res = {}
    for name, spec in SCALES.items():
        steps = family(spec['anchor'], peak=spec.get('peak'))
        sc = {}
        for g in spec['steps']:
            h = steps[g]
            for member in spec['members']:
                if abs(grade(BRAND[member]) - g) <= 1: h = BRAND[member]
            sc[f'{name.lower()}-{g}'] = h
        res[name] = sc
    return res

# Status colours: a strong tone for text, icons and borders (grade 62 -> >= 6.4:1 on white) and a background tint (grade 5).
STATUS = {
    'Error':   {'hue': 27,  'chroma': 0.19, 'bg': 0.25, 'vi': 'Lỗi, không đạt, nguy hiểm'},
    'Warning': {'hue': 85,  'chroma': 0.14, 'bg': 0.45, 'vi': 'Cảnh báo, cần chú ý'},
    'Success': {'hue': 150, 'chroma': 0.13, 'bg': 0.25, 'vi': 'Thành công, đạt, hoàn thành'},
    'Info':    {'hue': None, 'chroma': None, 'vi': 'Thông tin, gợi ý'},   # VCCI Blue on Blue Tint
}

def build_status(scales):
    out = {}
    for name, s in STATUS.items():
        if s['hue'] is None:
            strong, tint = BRAND['VCCI Blue'], BRAND['Blue Tint']
        else:
            strong, tint = solve(s['hue'], s['chroma'], 62), solve(s['hue'], s['chroma'] * s['bg'], 5)
        out[name] = {'strong': strong, 'background': tint, 'use': s['vi']}
    return out

def build_dataviz(scales):
    B, Z, S = scales['Blue'], scales['Bronze'], scales['Slate']
    return {
        'categorical': [('VCCI Blue', BRAND['VCCI Blue']), ('Sky', BRAND['Sky']), ('Drum Bronze', BRAND['Drum Bronze']),
                        ('Slate', BRAND['Slate']), ('Bronze 20', Z['bronze-20']), ('Deep Navy', BRAND['Deep Navy'])],
        'highlight': {'focus': BRAND['Drum Gold'], 'context': BRAND['VCCI Blue'], 'muted': S['slate-20']},
        'sequential_7': [B[f'blue-{g}'] for g in (10, 20, 30, 40, 50, 60, 70)],
        'sequential_5': [B[f'blue-{g}'] for g in (10, 30, 50, 70, 90)],
        'diverging_7': [Z['bronze-60'], Z['bronze-40'], Z['bronze-20'], BRAND['Ivory'], B['blue-20'], B['blue-40'], B['blue-60']],
    }

# Office theme: accents 1-5 follow the chart series order, so new charts in Word, Excel and PowerPoint pick the VCCI order;
# accent 6 keeps Drum Gold in the theme palette for the one gold gesture (a 6th chart series is set to Deep Navy = Dark 2 by hand).
OFFICE = {'dk1': 'Ink', 'lt1': None, 'dk2': 'Deep Navy', 'lt2': 'Ivory', 'accent1': 'VCCI Blue', 'accent2': 'Sky', 'accent3': 'Drum Bronze',
          'accent4': 'Slate', 'accent5': ('Bronze 20', '#F2B18E'), 'accent6': 'Drum Gold', 'hlink': 'VCCI Blue', 'folHlink': 'Bronze Ink'}

def office_clr_scheme():
    def val(v):
        if v is None: return 'FFFFFF'
        return (v[1] if isinstance(v, tuple) else BRAND[v]).lstrip('#')
    return '<a:clrScheme name="VCCI">' + ''.join(f'<a:{k}><a:srgbClr val="{val(v)}"/></a:{k}>' for k, v in OFFICE.items()) + '</a:clrScheme>'

def system():
    sc = build_scales()
    return sc, build_status(sc), build_dataviz(sc)

def published_grade(key_or_name, h):
    """The grade people read: the step number for scale colours, the rounded grade for brand colours."""
    if '-' in key_or_name and key_or_name.split('-')[1].isdigit(): return int(key_or_name.split('-')[1])
    if key_or_name in BRAND: return brand_grade(key_or_name)
    return round(grade(h))

def check(scales, status):
    """Every pair whose published grades differ by 40 / 50 / 70 must reach 3 / 4.5 / 7 : 1."""
    bad = []
    flat = [(k, h) for s in scales.values() for k, h in s.items()] + list(BRAND.items()) + [('White', '#FFFFFF')]
    for ka, a in flat:
        for kb, b in flat:
            d = abs(published_grade(ka, a) - published_grade(kb, b)); c = contrast(a, b)
            for lim, need in ((40, 3.0), (50, 4.5), (70, 7.0)):
                if d >= lim and c < need: bad.append((ka, kb, d, round(c, 2), need))
    for n, s in status.items():
        for bg in ('#FFFFFF', BRAND['Paper'], s['background']):
            if contrast(s['strong'], bg) < 4.5: bad.append((n, bg, round(contrast(s['strong'], bg), 2)))
    return bad

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sc, st, dv = system()
    names = {h: n for n, h in BRAND.items()}
    for name, steps in sc.items():
        print(name)
        for k, h in steps.items():
            print(f'  {k:10s} {h}  grade {grade(h):5.1f}  on white {contrast(h, "#FFFFFF"):5.2f}  {names.get(h, "")}')
    print('Brand grades:', {n: brand_grade(n) for n in BRAND})
    print('Status'); [print(' ', n, v) for n, v in st.items()]
    print('Dataviz'); [print(' ', n, v) for n, v in dv.items()]
    print('contrast violations:', check(sc, st) or 'none')
