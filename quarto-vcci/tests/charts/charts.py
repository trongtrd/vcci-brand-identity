"""Sample charts with the VCCI matplotlib style:  python charts.py OUTDIR [CHARTS_DIR]
Writes py-<chart>.svg for the chart checks in run_tests.py (layer 8). The same charts are drawn in R and Stata."""
import csv, os, sys
OUT = os.path.abspath(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', '..', 'charts'))
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import vcci_charts as vcci

vcci.use('vi')
matplotlib.rcParams['svg.hashsalt'] = 'vcci'   # reproducible SVG ids
DATA = os.path.join(HERE, 'data')
read = lambda n: list(csv.DictReader(open(os.path.join(DATA, n + '.csv'), encoding='utf-8')))
SOURCE = 'Nguồn: VCCI · Số liệu minh họa'

def save(fig, name):
    fig.savefig(os.path.join(OUT, f'py-{name}.svg'), metadata={'Date': None})
    plt.close(fig)

# column chart, one value highlighted in gold with its label
d = read('bar')
fig, ax = plt.subplots()
bars = ax.bar([r['year'] for r in d], [float(r['score']) for r in d], width=0.62)
vcci.highlight(bars, -1)
ax.set_ylim(0, 80)
vcci.title(ax, 'Năm 2025 đạt điểm cao nhất trong sáu năm')
vcci.source(fig, SOURCE)
save(fig, 'bar')

# three lines, named at their ends
d = read('line')
fig, ax = plt.subplots()
for city in dict.fromkeys(r['city'] for r in d):
    rows = [r for r in d if r['city'] == city]
    ax.plot([int(r['year']) for r in rows], [float(r['score']) for r in rows], label=city)
ax.set_ylim(55, 75)
ax.set_xlim(2019.7, 2025.9)
vcci.line_labels(ax)
vcci.title(ax, 'Hà Nội vượt TP.HCM và Đà Nẵng từ năm 2024')
vcci.source(fig, SOURCE)
save(fig, 'line')

# stacked horizontal bars (shares), percentages on the segments
d = read('stack')
groups = list(dict.fromkeys(r['group'] for r in d))[::-1]
ratings = list(dict.fromkeys(r['rating'] for r in d))
fig, ax = plt.subplots(figsize=(6.5, 2.6))
left = [0] * len(groups)
for k, rating in enumerate(ratings):
    vals = [float(next(r['share'] for r in d if r['group'] == g and r['rating'] == rating)) for g in groups]
    bars = ax.barh(groups, vals, left=left, label=rating, height=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + v / 2, b.get_y() + b.get_height() / 2, f'{v:.0f}%', ha='center', va='center', fontsize=7.5,
                fontweight=600, color='white' if k in (0, 2, 3) else vcci.COLOURS['Ink'])
    left = [a + b for a, b in zip(left, vals)]
ax.set_xlim(0, 100)
ax.grid(False)
ax.xaxis.set_visible(False)
ax.spines['bottom'].set_visible(False)
vcci.title(ax, 'Doanh nghiệp nhỏ đánh giá tích cực hơn')
vcci.legend(ax)
vcci.source(fig, SOURCE)
save(fig, 'stack')

# scatter, two groups
d = read('scatter')
fig, ax = plt.subplots()
for sector in dict.fromkeys(r['sector'] for r in d):
    rows = [r for r in d if r['sector'] == sector]
    ax.scatter([float(r['employees']) for r in rows], [float(r['cost']) for r in rows], label=sector, s=18)
ax.set_xlabel('Số lao động')
ax.set_ylabel('Chi phí không chính thức (% doanh thu)')
ax.set_ylim(0, None)
vcci.legend(ax)
vcci.title(ax, 'Chi phí không chính thức tăng theo quy mô')
vcci.source(fig, SOURCE)
save(fig, 'scatter')

# six series: the full series order
d = read('series6')
fig, ax = plt.subplots()
for sector in dict.fromkeys(r['sector'] for r in d):
    rows = [r for r in d if r['sector'] == sector]
    ax.plot([int(r['year']) for r in rows], [float(r['value']) for r in rows], label=sector)
ax.set_xlim(2019.7, 2026.1)
vcci.line_labels(ax)
vcci.title(ax, 'Sáu ngành theo thứ tự màu chuỗi')
vcci.source(fig, SOURCE)
save(fig, 'series6')

# heat map, seven ordered classes (light = low)
d = read('heat')
regions = list(dict.fromkeys(r['region'] for r in d))
years = list(dict.fromkeys(r['year'] for r in d))
grid = [[float(next(r['score'] for r in d if r['region'] == g and r['year'] == y)) for y in years] for g in regions]
fig, ax = plt.subplots()
bounds = [59 + 1.5 * i for i in range(8)]
ax.pcolormesh(grid, cmap='vcci_seq', norm=BoundaryNorm(bounds, 7), edgecolors='white', linewidth=1.5)
for i, row in enumerate(grid):
    for j, v in enumerate(row):
        ax.text(j + 0.5, i + 0.5, vcci.number(v), ha='center', va='center', fontsize=7.5,
                color='white' if v >= 65 else vcci.COLOURS['Ink'])
ax.set_xticks([j + 0.5 for j in range(len(years))], years)
ax.set_yticks([i + 0.5 for i in range(len(regions))], regions)
ax.invert_yaxis()
ax.grid(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(length=0)
vcci.title(ax, 'Đông Nam Bộ dẫn đầu, Tây Nguyên cải thiện nhanh')
vcci.source(fig, SOURCE)
save(fig, 'heat')
print('python charts ->', OUT)
