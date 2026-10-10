"""Write the deliberately broken charts that layer 8 must catch (expect.yml lists which check catches each).
    python quarto-vcci/tests/selftest/charts/make_broken.py
The R and Stata files were drawn once with their tools' default styles:
    r-ggplot-default.svg     ggplot(d, aes(factor(year), score)) + geom_col() + labs(title = ...), theme_grey, svglite
    stata-s2color.svg        graph bar score, over(year) title(...), scheme s2color, graph export
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'charts'))
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import vcci_charts as vcci

YEARS = ['2020', '2021', '2022', '2023', '2024', '2025']
SCORES = [63.2, 64.5, 65.1, 64.8, 66.0, 67.4]
BAR = 'Năm 2025 đạt điểm cao nhất trong sáu năm'
LINE = 'Hà Nội vượt TP.HCM và Đà Nẵng từ năm 2024'
CITIES = {'Hà Nội': [61, 62, 63.5, 65, 66.8, 68.6], 'TP.HCM': [64, 65, 65.5, 66, 66.3, 66.2], 'Đà Nẵng': [66, 65, 65.5, 65.2, 64.5, 63.6]}

def save(fig, name):
    fig.savefig(os.path.join(HERE, name), metadata={'Date': None})
    plt.close(fig)

def bars(title, ylim=(0, 80), **kw):
    fig, ax = plt.subplots()
    b = ax.bar(YEARS, SCORES, **kw)
    ax.set_ylim(*ylim)
    ax.set_title(title)
    return fig, ax, b

def lines(lang='vi'):
    vcci.use(lang)
    fig, ax = plt.subplots()
    for city, vals in CITIES.items(): ax.plot(YEARS, vals, label=city)
    ax.set_ylim(55, 75)
    vcci.title(ax, LINE)
    return fig, ax

# matplotlib defaults: tab colours, DejaVu Sans, no highlighted value, decimal point
matplotlib.rcParams['svg.fonttype'] = 'none'
fig, ax, b = bars(BAR)
ax.bar_label(b, fmt='%.1f')
save(fig, 'py-matplotlib-default.svg')

# brand style, but bars at 60 % opacity
vcci.use()
fig, ax, b = bars(BAR, alpha=0.6)
vcci.highlight(b, -1)
save(fig, 'py-transparent.svg')

# brand style, but the value axis starts at 60 (the drop between bars looks larger than it is)
fig, ax, b = bars(BAR, ylim=(60, 70))
vcci.highlight(b, -1)
save(fig, 'py-axis-not-zero.svg')

# brand style, but text saved as outlines: fonts cannot be checked or set by the document
matplotlib.rcParams['svg.fonttype'] = 'path'
fig, ax, b = bars(BAR)
vcci.highlight(b, -1)
save(fig, 'py-text-as-paths.svg')
matplotlib.rcParams['svg.fonttype'] = 'none'

# brand style, but vertical grid lines
fig, ax = lines()
ax.grid(True, axis='both')
save(fig, 'py-vertical-grid.svg')

# brand style in English: decimal point in a Vietnamese chart
fig, ax = lines('en')
save(fig, 'py-decimal-point.svg')
vcci.use()

# Drum Gold used as the second series colour
from cycler import cycler
fig, ax = plt.subplots()
ax.set_prop_cycle(cycler(color=[vcci.SERIES[0], vcci.HIGHLIGHT['focus']] + vcci.SERIES[2:]))
for i in range(6): ax.plot(YEARS, [40 + 7 * i + k for k in range(6)], label=f'Ngành {i + 1}')
vcci.title(ax, 'Sáu ngành theo thứ tự màu chuỗi')
save(fig, 'py-gold-series.svg')

# status colours (error red, success green) as series colours
fig, ax = plt.subplots()
ax.set_prop_cycle(cycler(color=['#B7191C', '#046B2F', vcci.SERIES[2]]))
for city, vals in CITIES.items(): ax.plot(YEARS, vals, label=city)
vcci.title(ax, LINE)
save(fig, 'py-status-colours.svg')
print('broken charts ->', HERE)
