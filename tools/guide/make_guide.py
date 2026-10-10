"""Build the VCCI brand guidelines (Vietnamese, A4 landscape) as HTML, then print to PDF with Edge.

Run from the repository root:  python tools/guide/make_guide.py  (after tools/guide/prepare_images.py)
"""
import os, re, sys, json, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets'))
import build_assets as BA
import colour_system as CS
SC, ST, DV = CS.system()

ROOT = os.getcwd()
G = os.path.join(ROOT, 'build', 'guide')
OUT_DIR = os.path.join(ROOT, 'brand-assets', '07_Guidelines')
os.makedirs(OUT_DIR, exist_ok=True)
from urllib.parse import quote
U = lambda *p: 'file:///' + quote(os.path.normpath(os.path.join(ROOT, *p)).replace(os.sep, '/'), safe='/:')
LOGO = U('brand-assets', '01_Logo', 'SVG', 'VCCI_Logo_Primary.svg')
LOGO_PLATE = U('brand-assets', '01_Logo', 'SVG', 'VCCI_Logo_Primary_Plate.svg')
WHITE = U('board', 'assets', 'vcci-logo-white-misuse.svg')
ICON = lambda tier, variant, f: U('brand-assets', '05_Icons', tier, 'SVG', variant, f)
IMG = lambda n: U('build', 'guide', 'img', n)
FONT = lambda f: U('brand-assets', '03_Fonts', f)

# ---------------------------------------------------------------- icon catalogue (from the ChatGPT handback)
md = open(os.path.join(ROOT, 'brand-assets', '05_Icons', 'HANDBACK_TO_CLAUDE.md'), encoding='utf-8').read()
CAT = re.findall(r'^\| (UI|Hero \d\d)\s*\| ([\w-]+) \| ([^|]+) \| ([^|]+) \|$', md, re.M)
UI = [(slug, vi.strip()) for t, slug, vi, en in CAT if t == 'UI']
HERO = [(t.split()[1], slug, vi.strip()) for t, slug, vi, en in CAT if t.startswith('Hero')]
assert len(UI) == 48 and len(HERO) == 24, (len(UI), len(HERO))

def hero_svg_inner(num, slug, variant='Blue-Gold'):
    p = os.path.join(ROOT, 'brand-assets', '05_Icons', 'Hero', 'SVG', variant, f'VCCI_Hero_{num}_{slug}.svg')
    s = open(p, encoding='utf-8').read()
    attrs = re.search(r'<svg([^>]*)>', s).group(1)
    inner = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    return attrs, inner

def drum(c, g, w, op, gop): return f'<svg viewBox="-300 -300 600 600" class="ring">{BA.drum(c, g, w, op, gop)}</svg>'

# ---------------------------------------------------------------- CSS
CSS = f"""
@font-face{{font-family:Lora;src:url({FONT('Lora/Lora-Regular.ttf')});font-weight:400}}
@font-face{{font-family:Lora;src:url({FONT('Lora/Lora-Italic.ttf')});font-weight:400;font-style:italic}}
@font-face{{font-family:Lora;src:url({FONT('Lora/Lora-Medium.ttf')});font-weight:500}}
@font-face{{font-family:Lora;src:url({FONT('Lora/Lora-MediumItalic.ttf')});font-weight:500;font-style:italic}}
@font-face{{font-family:Lora;src:url({FONT('Lora/Lora-SemiBold.ttf')});font-weight:600}}
@font-face{{font-family:BVP;src:url({FONT('BeVietnamPro/BeVietnamPro-Light.ttf')});font-weight:300}}
@font-face{{font-family:BVP;src:url({FONT('BeVietnamPro/BeVietnamPro-Regular.ttf')});font-weight:400}}
@font-face{{font-family:BVP;src:url({FONT('BeVietnamPro/BeVietnamPro-Medium.ttf')});font-weight:500}}
@font-face{{font-family:BVP;src:url({FONT('BeVietnamPro/BeVietnamPro-SemiBold.ttf')});font-weight:600}}
@font-face{{font-family:BVP;src:url({FONT('BeVietnamPro/BeVietnamPro-Bold.ttf')});font-weight:700}}
""" + r"""
@page{size:297mm 210mm;margin:0}
:root{--blue:#264896;--gold:#FFCD00;--bronze:#CC713C;--ink2:#9C570C;--deep:#0B1A4F;--tint:#E7ECF6;--ink:#161A26;--slate:#5C6478;
 --stone:#E6E1D5;--ivory:#F4F0E6;--paper:#FBF9F4;--hair:rgba(38,72,150,.14)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{-webkit-print-color-adjust:exact;print-color-adjust:exact;background:#fff}
body{font-family:BVP;color:var(--ink);font-size:9.2pt;line-height:1.55}
.page{width:297mm;height:210mm;position:relative;overflow:hidden;page-break-after:always;break-after:page;background:#fff;counter-increment:pg}
.page:last-child{page-break-after:auto}
.chrome{position:absolute;left:16mm;right:16mm;top:9mm;display:flex;justify-content:space-between;font:600 6.4pt BVP;letter-spacing:.2em;text-transform:uppercase;color:var(--slate)}
.chrome b{color:var(--ink2)}
.foot{position:absolute;left:16mm;right:16mm;bottom:8mm;display:flex;justify-content:space-between;font:500 6.4pt BVP;letter-spacing:.12em;color:var(--slate)}
.foot .n::after{content:counter(pg, decimal-leading-zero)}
.m{position:absolute;left:16mm;right:16mm;top:20mm;bottom:17mm}
h1{font:500 30pt/1.08 Lora;color:var(--blue);letter-spacing:-.01em}
h2{font:500 20pt/1.15 Lora;color:var(--blue);margin-bottom:4mm}
h2 em,h1 em{color:var(--ink2);font-style:italic}
h3{font:600 7.2pt BVP;letter-spacing:.2em;text-transform:uppercase;color:var(--ink2);margin:0 0 2mm}
p{margin:0 0 2.6mm}
p.lead{font:400 12.5pt/1.5 Lora;color:var(--blue)}
.small{font-size:7.6pt;color:var(--slate);line-height:1.5}
.rule{width:14mm;height:.8mm;background:var(--gold);margin:4mm 0 5mm}
.grid{display:grid;gap:6mm}
.card{background:var(--paper);border-radius:1.2mm;position:relative;overflow:hidden}
.cap{font:600 6.4pt BVP;letter-spacing:.16em;text-transform:uppercase;color:var(--slate)}
.cap b{color:var(--blue)}
ul.rules{list-style:none}
ul.rules li{position:relative;padding:1.6mm 0 1.6mm 6mm;border-top:.25mm solid var(--hair)}
ul.rules li::before{content:"";position:absolute;left:0;top:3.2mm;width:2.2mm;height:2.2mm;background:var(--blue)}
ul.rules.no li::before{background:none;border:.35mm solid var(--ink2);transform:rotate(45deg);width:1.8mm;height:1.8mm}
ul.rules li b{color:var(--blue);font-weight:600}
.ok,.bad{font:700 6.4pt BVP;letter-spacing:.18em;text-transform:uppercase}
.ok{color:var(--blue)} .bad{color:#B3261E}
.x::after{content:"";position:absolute;inset:0;background:linear-gradient(to top right,transparent calc(50% - .2mm),rgba(179,38,30,.8) 50%,transparent calc(50% + .2mm))}
/* opener */
.opener .panel{position:absolute;left:0;top:0;bottom:0;width:100mm;background:linear-gradient(160deg,#2B4FA0,#1E3D86);color:#fff;overflow:hidden}
.opener .panel .ring{position:absolute;width:170mm;height:170mm;left:-35mm;bottom:-75mm}
.opener .panel .num{position:absolute;left:16mm;top:22mm;font:500 64pt/1 Lora;color:var(--gold)}
.opener .panel .ttl{position:absolute;left:16mm;right:12mm;top:52mm;font:500 24pt/1.12 Lora;color:#fff}
.opener .panel .intro{position:absolute;left:16mm;right:14mm;top:84mm;font:400 9.2pt/1.6 BVP;color:rgba(255,255,255,.82)}
.opener .chrome{left:116mm}
.opener .chrome span:first-child{display:none}
.opener .m{left:116mm}
.opener .foot{left:116mm}
.panel .plabel{position:absolute;left:16mm;top:9mm;font:600 6.4pt BVP;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.6)}
/* swatches */
.sw{border-radius:1.2mm;padding:4mm 4.5mm;position:relative}
.sw .nm{font:500 13pt Lora}
.sw .rl{font:600 6pt BVP;letter-spacing:.18em;text-transform:uppercase;opacity:.75;margin-top:1mm}
.sw table{position:absolute;left:4.5mm;bottom:3.5mm;border-collapse:collapse;font:500 7.2pt BVP;letter-spacing:.04em}
.sw td{padding:.5mm 4mm .5mm 0}
.sw td:first-child{font-weight:700;font-size:6pt;letter-spacing:.14em;opacity:.7}
.icons{display:grid;grid-template-columns:repeat(8,1fr);border-top:.25mm solid var(--hair);border-left:.25mm solid var(--hair)}
.icons div{border-right:.25mm solid var(--hair);border-bottom:.25mm solid var(--hair);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.4mm;padding:2.2mm 1mm}
.icons img{width:7.5mm;height:7.5mm}
.icons span{font:500 6pt/1.25 BVP;color:var(--slate);text-align:center}
.heros{display:grid;grid-template-columns:repeat(8,1fr);gap:3mm}
.heros div{background:var(--paper);border-radius:1.2mm;display:flex;flex-direction:column;align-items:center;padding:3mm 1.5mm 2.5mm;gap:1.6mm}
.heros img{width:15mm;height:15mm}
.heros span{font:500 6.2pt/1.3 BVP;color:var(--ink);text-align:center}
.heros b{font:600 5.6pt BVP;color:var(--ink2);letter-spacing:.14em}
.shot{width:100%;display:block;border-radius:1mm;box-shadow:0 .6mm 1.6mm rgba(20,16,8,.12),0 3mm 8mm rgba(20,16,8,.10)}
.page img{display:block}
"""

# ---------------------------------------------------------------- page helpers
SECTIONS = {1: 'Thương hiệu', 2: 'Logo', 3: 'Màu sắc', 4: 'Kiểu chữ', 5: 'Họa tiết', 6: 'Icon & Minh họa', 7: 'Bố cục',
            8: 'Dữ liệu & Biểu đồ', 9: 'Ứng dụng'}
def chrome(sec): return f'<div class="chrome"><span><b>{sec:02d}</b>&nbsp;&nbsp;{SECTIONS[sec]}</span><span>Hướng dẫn Nhận diện Thương hiệu VCCI</span></div>'
FOOT = '<div class="foot"><span>Liên đoàn Thương mại và Công nghiệp Việt Nam · Phiên bản 1.1 · 10/2026</span><span class="n"></span></div>'
def page(sec, body, cls=''): return f'<section class="page {cls}">{chrome(sec)}<div class="m">{body}</div>{FOOT}</section>'
START = {}
def opener(sec, title, intro, body):
    START[sec] = len(P) + 1
    panel = (f'<div class="panel">{drum("#fff", BA.GOLD, .7, .16, .5)}<div class="plabel">Phần {sec:02d}</div>'
             f'<div class="num">{sec:02d}</div><div class="ttl">{title}</div><div class="intro">{intro}</div></div>')
    return f'<section class="page opener">{panel}{chrome(sec)}<div class="m">{body}</div>{FOOT}</section>'

def swatch(name, role, bg, fg, rows, h):
    t = ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in rows)
    return f'<div class="sw" style="background:{bg};color:{fg};height:{h}"><div class="nm">{name}</div><div class="rl">{role}</div><table>{t}</table></div>'

P = []

# ================================================================ 01 COVER
P.append(f'''<section class="page" style="background:var(--paper)">
 <div style="position:absolute;right:0;top:0;bottom:0;width:118mm;background:linear-gradient(160deg,#2B4FA0,#1E3D86);overflow:hidden">
   <svg viewBox="-300 -300 600 600" style="position:absolute;width:230mm;height:230mm;left:-20mm;top:-10mm">{BA.drum('#fff', BA.GOLD, .55, .16, .6)}</svg>
   <div style="position:absolute;left:14mm;bottom:14mm;font:600 6.6pt BVP;letter-spacing:.22em;text-transform:uppercase;color:rgba(255,255,255,.65)">Phiên bản 1.1 &nbsp;·&nbsp; Tháng 10 / 2026</div>
 </div>
 <img src="{LOGO}" style="position:absolute;left:20mm;top:22mm;width:92mm">
 <div style="position:absolute;left:20mm;top:84mm;width:140mm">
   <div class="cap" style="color:var(--ink2);margin-bottom:5mm">Liên đoàn Thương mại và Công nghiệp Việt Nam</div>
   <h1 style="font-size:38pt">Hướng dẫn<br>Nhận diện Thương hiệu</h1>
   <div class="rule" style="margin:7mm 0"></div>
   <p class="lead" style="width:120mm">Logo, màu sắc, kiểu chữ, họa tiết, icon và cách áp dụng cho mọi ấn phẩm của VCCI.</p>
 </div>
</section>''')

# ================================================================ 02 CONTENTS + HOW TO USE
toc = [(1, 'Thương hiệu', 'Định vị, tính cách, giọng điệu'), (2, 'Logo', 'Cấu trúc, dựng hình, phiên bản, quy tắc'),
       (3, 'Màu sắc', 'Bảng màu, thang sắc độ, màu trạng thái'), (4, 'Kiểu chữ', 'Hai họ chữ và thang chữ'),
       (5, 'Họa tiết', 'Ngôn ngữ đồ họa từ trống đồng'), (6, 'Icon & Minh họa', 'Hai cấp icon, nguyên tắc minh họa'),
       (7, 'Bố cục', 'Lưới, khoảng cách, sự nhất quán'), (8, 'Dữ liệu & Biểu đồ', 'Màu biểu đồ, chọn biểu đồ, trình bày'),
       (9, 'Ứng dụng', 'Template, ấn phẩm, sự kiện, tài sản')]
rows = ''.join(f'''<div style="display:grid;grid-template-columns:14mm 1fr 10mm;align-items:baseline;padding:2.1mm 0;border-top:.25mm solid var(--hair)">
  <span style="font:500 13pt Lora;color:var(--gold);-webkit-text-stroke:.15mm var(--ink2)">{n:02d}</span>
  <span><span style="font:500 12.5pt Lora;color:var(--blue)">{t}</span><span class="small" style="margin-left:4mm">{d}</span></span>
  <span style="text-align:right;font:500 9pt BVP;color:var(--slate)">@@PG{n}@@</span></div>''' for n, t, d in toc)
P.append(f'''<section class="page"><div class="chrome"><span><b>00</b>&nbsp;&nbsp;Mở đầu</span><span>Hướng dẫn Nhận diện Thương hiệu VCCI</span></div><div class="m">
 <div class="grid" style="grid-template-columns:150mm 1fr;gap:16mm;height:100%">
  <div><h2>Mục lục</h2><div style="margin-top:6mm">{rows}</div></div>
  <div style="padding-top:2mm">
   <h3>Về tài liệu này</h3>
   <p>Tài liệu quy định cách thể hiện thương hiệu VCCI trên mọi ấn phẩm: văn bản, báo cáo, sự kiện, kênh số và quà tặng. Mục tiêu là để mọi người, dù ở đơn vị nào, đều tạo ra sản phẩm nhất quán và chuyên nghiệp.</p>
   <p>Các quy tắc có hai mức. <b style="color:var(--blue)">Bắt buộc</b> áp dụng cho logo và màu, vì đây là phần nhận diện cốt lõi. <b style="color:var(--blue)">Khuyến nghị</b> áp dụng cho bố cục và minh họa, để người thiết kế còn không gian sáng tạo.</p>
   <h3 style="margin-top:6mm">Tài sản đi kèm</h3>
   <p>Mọi file gốc nằm trong thư mục <b>brand-assets</b>: logo (SVG, PNG, PDF, bản gốc CorelDRAW), màu (Office, Adobe, CSS, gồm cả thang sắc độ và màu biểu đồ), font, họa tiết, icon và template Word. Danh mục chi tiết ở trang cuối.</p>
   <h3 style="margin-top:6mm">Khi có thắc mắc</h3>
   <p>Mọi trường hợp chưa được nêu trong tài liệu cần được bộ phận phụ trách thương hiệu duyệt trước khi phát hành.</p>
  </div>
 </div></div>{FOOT}</section>''')

# ================================================================ 03 BRAND
attrs = [('Uy tín', 'Tổ chức đại diện cho cộng đồng doanh nghiệp ở tầm quốc gia, đối thoại trực tiếp với Chính phủ.'),
         ('Bản sắc', 'Trống đồng Đông Sơn đặt ngay trong tên gọi: niềm tự hào về văn hóa và lịch sử Việt.'),
         ('Tin cậy', 'Nguồn thông tin, dịch vụ và chứng nhận mà doanh nghiệp, đối tác quốc tế có thể dựa vào.'),
         ('Đồng hành', 'Gần gũi với doanh nghiệp như một người bạn, không như một cơ quan hành chính.')]
P.append(opener(1, 'Tiếng nói của doanh nghiệp Việt Nam',
  'VCCI là tổ chức quốc gia tập hợp, đại diện và bảo vệ cộng đồng doanh nghiệp, doanh nhân và người sử dụng lao động Việt Nam, thành lập năm 1963.',
  f'''<p class="lead" style="font-size:15pt;width:150mm">Bản sắc thương hiệu VCCI phải mang <em style="color:var(--ink2)">sức nặng của một thể chế</em> và sự ấm áp của một người đồng hành: vững vàng, đáng tin, và rõ ràng là của Việt Nam.</p>
  <div class="rule"></div>
  <div class="grid" style="grid-template-columns:repeat(2,1fr);gap:5mm 8mm;margin-top:4mm">
   {''.join(f'<div style="border-top:.4mm solid var(--blue);padding-top:3mm"><div style="font:500 14pt Lora;color:var(--blue);margin-bottom:1.5mm">{a}</div><p class="small" style="font-size:8.4pt">{b}</p></div>' for a, b in attrs)}
  </div>
  <div class="grid" style="grid-template-columns:repeat(3,1fr);gap:6mm;margin-top:9mm">
   <div><h3>Đối tượng</h3><p class="small" style="font-size:8.4pt">Doanh nghiệp, hiệp hội, cơ quan nhà nước, nhà đầu tư và đối tác quốc tế</p></div>
   <div><h3>Định vị</h3><p class="small" style="font-size:8.4pt">Thể chế uy tín, hiện đại, cởi mở với thế giới</p></div>
   <div><h3>Tinh thần</h3><p class="small" style="font-size:8.4pt">Trang trọng mà không xa cách; tự hào mà không phô trương</p></div>
  </div>'''))

sl = [('Truyền thống', 'Hiện đại', 42), ('Trang trọng', 'Gần gũi', 34), ('Tiết chế', 'Phô diễn', 26), ('Quốc gia', 'Quốc tế', 46), ('Cổ điển', 'Kỹ thuật', 30)]
sliders = ''.join(f'''<div style="display:grid;grid-template-columns:26mm 1fr 26mm;gap:4mm;align-items:center;padding:2.2mm 0">
 <span class="small">{a}</span><div style="position:relative;height:.5mm;background:var(--stone)"><i style="position:absolute;left:0;top:0;height:.5mm;width:{v}%;background:var(--blue)"></i>
 <i style="position:absolute;left:{v}%;top:50%;width:3.4mm;height:3.4mm;border-radius:50%;background:var(--blue);transform:translate(-50%,-50%);box-shadow:0 0 0 1mm rgba(38,72,150,.15)"></i></div>
 <span class="small" style="text-align:right">{b}</span></div>''' for a, b, v in sl)
words = [('Uy quyền', 'Câu khẳng định, dẫn chứng rõ ràng, số liệu có nguồn.'), ('Điềm tĩnh', 'Không cường điệu, không dấu chấm than, không chữ in hoa để gây chú ý.'),
         ('Bản sắc', 'Tiếng Việt chuẩn mực; tiếng Anh dùng khi cần cho đối tác quốc tế.'), ('Cởi mở', 'Gọi doanh nghiệp là đối tác, nói về lợi ích của họ trước.')]
P.append(page(1, f'''<div class="grid" style="grid-template-columns:1fr 1fr;gap:14mm">
 <div><h2>Tính cách và <em>giọng điệu</em></h2><p>Thương hiệu VCCI nghiêng về phía trang trọng và tiết chế, nhưng không cứng nhắc. Các thang dưới đây cho biết vị trí cân bằng mà mọi ấn phẩm cần hướng tới.</p>
  <div style="margin-top:6mm">{sliders}</div>
  <div style="margin-top:8mm;border-left:.8mm solid var(--gold);padding-left:5mm;font:italic 400 13pt/1.45 Lora;color:var(--blue)">Rõ ràng hơn là khéo léo; tầm nhìn dài hạn hơn là khoảnh khắc ồn ào.</div></div>
 <div>{''.join(f'<div style="border-top:.25mm solid var(--hair);padding:3mm 0"><div style="font:500 14pt Lora;color:var(--blue)">{a}<span style="color:var(--ink2)">.</span></div><p class="small" style="font-size:8.4pt;margin:1mm 0 0">{b}</p></div>' for a, b in words)}
  <div class="grid" style="grid-template-columns:1fr 1fr;gap:6mm;margin-top:5mm">
   <div><div class="ok" style="margin-bottom:2mm">Nên</div><ul class="rules"><li>Đi thẳng vào nội dung chính</li><li>Dùng số liệu có nguồn</li><li>Câu ngắn, mỗi đoạn một ý</li></ul></div>
   <div><div class="bad" style="margin-bottom:2mm">Không nên</div><ul class="rules no"><li>Khẩu hiệu sáo rỗng</li><li>Từ lóng, biểu tượng cảm xúc</li><li>Viết hoa cả câu để nhấn mạnh</li></ul></div>
  </div></div></div>'''))

# ================================================================ 04 LOGO
P.append(opener(2, 'Logo', 'Logo VCCI gồm bốn chữ cái hình học và trống đồng Đông Sơn đặt trong lòng chữ C thứ nhất. Đây là tài sản quan trọng nhất của thương hiệu, phải luôn được dùng đúng bản gốc.',
  f'''<div class="card" style="height:112mm;background:#fff;box-shadow:inset 0 0 0 .25mm var(--hair)">
   <img src="{LOGO}" style="position:absolute;left:50%;top:50%;width:132mm;transform:translate(-50%,-50%)">
   <div style="position:absolute;left:8mm;top:9mm" class="cap"><b>Chữ VCCI</b> · hình học, nét đậm, màu VCCI Blue</div>
   <div style="position:absolute;left:8mm;bottom:9mm" class="cap"><b>Trống đồng</b> · mặt trời 14 cánh, vành hoa văn</div>
   <div style="position:absolute;right:8mm;bottom:9mm" class="cap"><b>Vòng ngăn</b> · khoảng hở giữa trống và chữ C</div>
  </div>
  <div class="grid" style="grid-template-columns:repeat(3,1fr);gap:7mm;margin-top:7mm">
   <div><h3>Ý nghĩa</h3><p class="small" style="font-size:8.4pt">Trống đồng là biểu tượng lâu đời của văn minh Việt. Đặt trống trong chữ C là đặt bản sắc vào trung tâm của tổ chức.</p></div>
   <div><h3>Bản gốc</h3><p class="small" style="font-size:8.4pt">File gốc là <b>VCCI_Logo_Master_CMYK.cdr</b>. Mọi bản SVG, PNG, PDF đều được dựng từ file này.</p></div>
   <div><h3>Nguyên tắc</h3><p class="small" style="font-size:8.4pt">Không vẽ lại, không gõ lại bằng font chữ, không tách trống đồng ra dùng riêng.</p></div>
  </div>'''))

cons = f'''<svg viewBox="0 0 3321.68 1000" style="position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible">
 <g fill="none" stroke="#9C570C" stroke-width="1.2" vector-effect="non-scaling-stroke">
  <line x1="-200" y1="0" x2="3520" y2="0" stroke-dasharray="5 4"/><line x1="-200" y1="1000" x2="3520" y2="1000" stroke-dasharray="5 4"/>
  <line x1="-200" y1="500" x2="3520" y2="500" opacity=".5"/><line x1="1650" y1="-180" x2="1650" y2="1180" opacity=".5"/>
  <circle cx="1650" cy="500" r="500" stroke="#D49B00" stroke-width="2"/><circle cx="1650" cy="500" r="296" stroke-dasharray="4 4"/>
  <circle cx="1650" cy="500" r="262" stroke="#D49B00" stroke-width="2"/></g></svg>'''
P.append(page(2, f'''<h2>Dựng hình và <em>tỉ lệ</em></h2>
 <div class="grid" style="grid-template-columns:1fr 78mm;gap:12mm">
  <div class="card" style="height:118mm;background:#fff;box-shadow:inset 0 0 0 .25mm var(--hair)">
   <div style="position:absolute;left:18mm;right:18mm;top:50%;transform:translateY(-50%);aspect-ratio:3.3217"><img src="{LOGO}" style="width:100%">{cons}</div>
   <div style="position:absolute;right:6mm;top:6mm" class="cap">H = chiều cao chữ</div></div>
  <div>
   <div style="border-top:.4mm solid var(--blue);padding:3mm 0"><div style="font:500 20pt Lora;color:var(--blue)">r ≈ ½ R</div><p class="small">Bán kính trống đồng bằng khoảng một nửa bán kính ngoài của chữ C. Hai đường tròn có chung một tâm.</p></div>
   <div style="border-top:.25mm solid var(--hair);padding:3mm 0"><div style="font:500 20pt Lora;color:var(--blue)">0,52 H</div><p class="small">Đường kính trống đồng bằng khoảng một nửa chiều cao chữ. Đây là mô-đun gốc của logo.</p></div>
   <div style="border-top:.25mm solid var(--hair);padding:3mm 0"><div style="font:500 20pt Lora;color:var(--blue)">3,32 : 1</div><p class="small">Tỉ lệ ngang trên cao của logo. Luôn thu phóng đồng đều theo tỉ lệ này.</p></div>
   <div style="border-top:.25mm solid var(--hair);padding:3mm 0"><div style="font:500 20pt Lora;color:var(--blue)">x = r</div><p class="small">Bán kính trống (≈ 0,26 H) là đơn vị x, dùng cho khoảng trống bảo vệ, lề ô nền sáng và lề trang.</p></div>
  </div></div>'''))

xbox = lambda pos: f'<div style="position:absolute;{pos};width:var(--x);height:var(--x);border:.25mm solid rgba(156,87,12,.6);background:rgba(255,205,0,.14);display:flex;align-items:center;justify-content:center;font:italic 500 9pt Lora;color:var(--ink2)">x</div>'
P.append(page(2, f'''<h2>Khoảng trống bảo vệ và <em>cỡ tối thiểu</em></h2>
 <div class="grid" style="grid-template-columns:1fr 1fr;gap:12mm">
  <div><div class="card" style="height:92mm;background:#fff;box-shadow:inset 0 0 0 .25mm var(--hair);display:flex;align-items:center;justify-content:center">
    <div style="--x:8.45mm;position:relative;padding:var(--x);outline:.3mm dashed rgba(156,87,12,.7)"><img src="{LOGO}" style="width:107mm">
     {xbox('left:0;top:0')}{xbox('right:0;top:0')}{xbox('left:0;bottom:0')}{xbox('right:0;bottom:0')}</div></div>
   <p style="margin-top:5mm">Giữ khoảng trống tối thiểu bằng <b style="color:var(--blue)">x</b> (bán kính trống đồng) ở cả bốn phía. Không đặt chữ, hình ảnh hay mép trang vào vùng này. Khi có thể, hãy để khoảng trống rộng hơn.</p></div>
  <div><div class="grid" style="grid-template-columns:repeat(3,1fr);gap:4mm">
    <div class="card" style="height:40mm;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4mm"><img src="{LOGO}" style="width:25mm"><span class="cap">In · 25 mm</span></div>
    <div class="card" style="height:40mm;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4mm"><img src="{LOGO}" style="width:25.4mm"><span class="cap">Màn hình · 96 px</span></div>
    <div class="card" style="height:40mm;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4mm;background:var(--blue)"><img src="{LOGO_PLATE}" style="width:28mm"><span class="cap" style="color:rgba(255,255,255,.75)">Ô nền sáng · 96 px</span></div></div>
   <p style="margin-top:5mm">Dưới các cỡ này, chi tiết trống đồng và vòng ngăn không còn đọc được. Với favicon và biểu tượng ứng dụng, dùng logo đầy đủ trên ô nền sáng hình vuông.</p>
   <h3 style="margin-top:6mm">Vị trí khuyến nghị</h3>
   <ul class="rules"><li><b>Góc trên bên trái</b> cho văn bản, báo cáo và trang web</li><li><b>Căn giữa</b> cho bìa trang trọng, chứng nhận, sân khấu</li><li><b>Không</b> đặt logo trôi giữa nội dung hoặc lặp lại nhiều lần trên một trang</li></ul></div></div>'''))

vers = [('VCCI_Logo_Primary', 'Logo chính', 'Mọi trường hợp; ưu tiên số một.', '#fff', 78),
        ('VCCI_Lockup_Horizontal_VI-EN', 'Lockup ngang song ngữ', 'Tiêu đề thư, báo cáo, website, biển hiệu.', '#fff', 88),
        ('VCCI_Lockup_Stacked_VI', 'Lockup đứng tiếng Việt', 'Bìa, chứng nhận, kỷ niệm chương, sân khấu trong nước.', '#fff', 78),
        ('VCCI_Lockup_Stacked_EN', 'Lockup đứng tiếng Anh', 'Ấn phẩm và sự kiện quốc tế.', '#fff', 78)]
vcards = ''.join(f'''<div><div class="card" style="height:48mm;background:{bg};box-shadow:inset 0 0 0 .25mm var(--hair);display:flex;align-items:center;justify-content:center">
  <img src="{U('brand-assets', '01_Logo', 'SVG', f + '.svg')}" style="width:{w}%;max-height:38mm"></div>
  <div style="font:500 11pt Lora;color:var(--blue);margin-top:3mm">{n}</div><p class="small">{d}</p></div>''' for f, n, d, bg, w in vers)
P.append(page(2, f'''<h2>Các phiên bản <em>logo</em></h2><p style="width:180mm">Bốn phiên bản dưới đây là toàn bộ các phiên bản hợp lệ. Mỗi phiên bản có sẵn ở dạng SVG, PNG và PDF, kèm bản đặt trên ô nền sáng.</p>
 <div class="grid" style="grid-template-columns:1.1fr 1.5fr 1fr 1fr;gap:6mm;margin-top:4mm">{vcards}</div>
 <div style="margin-top:6mm;padding:4mm 5mm;background:var(--tint);border-left:.8mm solid var(--blue)" class="small"><b style="color:var(--blue)">Chỉ một phiên bản màu.</b> VCCI chỉ dùng logo với chữ VCCI Blue và trống đồng màu gốc. Không có phiên bản chữ trắng, chữ vàng, đơn sắc hay trống đồng đứng riêng.</div>'''))

bgs = [('var(--paper)', LOGO, 'Paper', 'Nền mặc định', True), ('var(--stone)', LOGO, 'Stone', 'Nền trung tính', True),
       ('var(--blue)', LOGO_PLATE, 'VCCI Blue', 'Dùng ô nền sáng', True), ('var(--deep)', LOGO_PLATE, 'Deep Navy', 'Dùng ô nền sáng', True),
       (f'url({IMG("mock_stationery.jpg")}) center/cover', LOGO_PLATE, 'Ảnh chụp', 'Dùng ô nền sáng', True)]
bcards = ''.join(f'''<div><div class="card" style="height:36mm;background:{bg};display:flex;align-items:center;justify-content:center"><img src="{src}" style="width:{'40' if 'Plate' in src else '42'}mm"></div>
 <div class="cap" style="margin-top:2.4mm"><b>{n}</b> · {d}</div></div>''' for bg, src, n, d, ok in bgs)
P.append(page(2, f'''<h2>Logo trên các <em>nền</em></h2>
 <div class="grid" style="grid-template-columns:repeat(5,1fr);gap:5mm;margin-top:2mm">{bcards}</div>
 <div class="grid" style="grid-template-columns:1fr 1fr;gap:12mm;margin-top:9mm">
  <div><h3>Ô nền sáng (logo plate)</h3><p>Trên nền xanh, nền tối, ảnh hoặc nền nhiều chi tiết, đặt logo trên một ô màu Paper (#FBF9F4). Lề trong của ô bằng x ở cả bốn phía, góc bo nhẹ. File có sẵn: <b>*_Plate.svg / .png / .pdf</b>.</p></div>
  <div style="display:grid;grid-template-columns:44mm 1fr;gap:6mm;align-items:center">
   <div class="card x" style="height:26mm;background:var(--blue);display:flex;align-items:center;justify-content:center"><img src="{WHITE}" style="width:36mm"></div>
   <div><h3 style="color:#B3261E">Quy tắc văn hóa</h3><p class="small" style="font-size:8.4pt">Không dùng logo với chữ cái màu trắng. Trong văn hóa Việt Nam, kiểu thể hiện này bị kiêng kị. Đây là quy tắc bắt buộc, không có ngoại lệ.</p></div></div></div>'''))

mis = [('transform:scaleX(1.35) scaleY(.8)', '', 'Kéo giãn hoặc bóp méo'), ('transform:rotate(-12deg)', '', 'Xoay nghiêng'),
       ('filter:hue-rotate(150deg) saturate(1.3)', '', 'Đổi màu logo'), ('filter:drop-shadow(1mm 1.2mm .8mm rgba(0,0,0,.45))', '', 'Thêm bóng, viền, hiệu ứng'),
       ('', 'background:linear-gradient(120deg,#c9a14a,#8395c2)', 'Đặt trên nền gây nhiễu'), ('opacity:.35', '', 'Làm mờ, trong suốt'),
       ('', 'background:var(--blue)', 'Logo chữ trắng', WHITE), ('width:20mm!important', '', 'Tách trống đồng dùng riêng', U('brand-assets', '01_Logo', '_Construction-only', 'VCCI_Drum_CONSTRUCTION-ONLY.svg'))]
mcards = ''.join(f'''<div><div class="card x" style="height:34mm;{m[1] or 'background:#fff;box-shadow:inset 0 0 0 .25mm var(--hair)'};display:flex;align-items:center;justify-content:center">
  <img src="{m[3] if len(m) > 3 else LOGO}" style="width:44mm;{m[0]}"></div><div class="small" style="margin-top:2mm;color:var(--ink)">{m[2]}</div></div>''' for m in mis)
P.append(page(2, f'''<h2>Những điều <em>không được làm</em></h2><p style="width:180mm">Mọi thay đổi trên logo, dù nhỏ, đều làm suy yếu sự nhận diện. Luôn dùng file gốc trong thư mục <b>01_Logo</b>.</p>
 <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:6mm 6mm;margin-top:4mm">{mcards}</div>
 <p class="small" style="margin-top:5mm">Ngoài ra: không gõ lại chữ VCCI bằng font khác, không thay trống đồng bằng hình khác, không đặt logo vào trong khung hoặc huy hiệu mới, không ghép logo với khẩu hiệu thành một khối cố định.</p>'''))

# ================================================================ 05 COLOUR
P.append(opener(3, 'Màu sắc', 'Màu xanh mang tầm vóc thể chế. Vàng và nâu đồng lấy từ chính trống đồng, dùng tiết chế như một chữ ký. Các màu logo được quy định trong file gốc CorelDRAW.',
  f'''<div class="grid" style="grid-template-columns:1.25fr 1fr;gap:5mm;height:118mm">
   {swatch('VCCI Blue', 'Màu chính · Uy tín', 'var(--blue)', '#fff', [('HEX', '#264896'), ('RGB', '38 · 72 · 150'), ('CMYK', '100 · 80 · 0 · 0'), ('NGUỒN', 'File gốc .CDR')], '118mm')}
   <div class="grid" style="grid-template-rows:1fr 1fr;gap:5mm">
    {swatch('Drum Gold', 'Màu phụ · Thịnh vượng', 'var(--gold)', 'var(--blue)', [('HEX', '#FFCD00'), ('RGB', '255 · 205 · 0'), ('CMYK', '0 · 20 · 100 · 0')], '100%')}
    {swatch('Drum Bronze', 'Màu phụ · Di sản', 'var(--bronze)', '#fff', [('HEX', '#CC713C'), ('RGB', '204 · 113 · 60'), ('CMYK', '0 · 60 · 80 · 20')], '100%')}
   </div></div>
  <p class="small" style="margin-top:5mm">Khi in, luôn dùng giá trị CMYK. Mã HEX/RGB là giá trị quy đổi cho màn hình (hồ sơ màu FOGRA39). File gốc không ghi mã Pantone; khi cần in màu pha, nhờ nhà in đề xuất mã gần nhất từ CMYK và in thử trước.</p>'''))

neut = [('Deep Navy', '#0B1A4F', '11 · 26 · 79', 'Nền tối', '#fff'), ('Sky', '#8FA6D6', '143 · 166 · 214', 'Chuỗi biểu đồ thứ hai, mảng nhạt', 'var(--deep)'),
        ('Blue Tint', '#E7ECF6', '231 · 236 · 246', 'Bề mặt giao diện', 'var(--blue)'),
        ('Bronze Ink', '#9C570C', '156 · 87 · 12', 'Chữ nhãn cỡ nhỏ', '#fff'), ('Ink', '#161A26', '22 · 26 · 38', 'Chữ thân bài', '#fff'),
        ('Slate', '#5C6478', '92 · 100 · 120', 'Chữ phụ', '#fff'), ('Stone', '#E6E1D5', '230 · 225 · 213', 'Nền trung tính', 'var(--ink)'),
        ('Ivory', '#F4F0E6', '244 · 240 · 230', 'Nền nhấn', 'var(--ink)'), ('Paper', '#FBF9F4', '251 · 249 · 244', 'Nền mặc định', 'var(--ink)')]
ncard = lambda n, h, rgb, r, fg: f'''<div class="sw" style="background:{h};color:{fg};height:34mm;{'box-shadow:inset 0 0 0 .25mm rgba(0,0,0,.08)' if fg == 'var(--ink)' else ''}">
 <div class="nm" style="font-size:11pt">{n}</div><div class="rl">{r}</div><table><tr><td>HEX</td><td>{h}</td></tr><tr><td>RGB</td><td>{rgb}</td></tr></table></div>'''
ncards = (f'<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:4mm">{"".join(ncard(*c) for c in neut[:4])}</div>'
          f'<div class="grid" style="grid-template-columns:repeat(5,1fr);gap:4mm;margin-top:4mm">{"".join(ncard(*c) for c in neut[4:])}</div>')
bar = ''.join(f'<i style="flex:{f};background:{c}"></i>' for f, c in ((44, 'var(--blue)'), (34, 'var(--paper)'), (10, 'var(--stone)'), (7, 'var(--gold)'), (5, 'var(--bronze)')))
pairs = [('var(--blue)', 'var(--paper)', '8,1 : 1', 'AAA'), ('var(--blue)', 'var(--gold)', '5,7 : 1', 'AA'), ('var(--paper)', 'var(--ink2)', '5,3 : 1', 'AA'), ('var(--paper)', 'var(--bronze)', '3,3 : 1', 'Chỉ chữ lớn')]
pcards = ''.join(f'<div style="background:{b};color:{f};height:16mm;border-radius:1mm;display:flex;align-items:center;justify-content:space-between;padding:0 4mm;{"box-shadow:inset 0 0 0 .25mm var(--hair)" if b == "var(--paper)" else ""}"><span style="font:500 15pt Lora">Aa</span><span style="font:700 6.4pt/1.3 BVP;letter-spacing:.1em;text-align:right">{r}<br>{l}</span></div>' for b, f, r, l in pairs)
P.append(page(3, f'''<h2 style="margin-bottom:3mm">Màu hỗ trợ, <em>tỉ lệ</em> và độ tương phản</h2>
 {ncards.replace('height:34mm', 'height:29mm')}
 <div class="grid" style="grid-template-columns:1fr 1fr;gap:12mm;margin-top:6mm">
  <div><h3>Tỉ lệ màu trên một ấn phẩm</h3><div style="display:flex;height:9mm;border-radius:1mm;overflow:hidden;box-shadow:inset 0 0 0 .25mm rgba(0,0,0,.06);margin:3mm 0">{bar}</div>
   <div class="small" style="display:flex;justify-content:space-between"><span>Xanh 44%</span><span>Paper 34%</span><span>Stone 10%</span><span>Vàng 7%</span><span>Đồng 5%</span></div>
   <p class="small" style="margin-top:3mm"><b style="color:var(--blue)">Một điểm nhấn vàng</b> trên mỗi bố cục: một đường gạch, một con số hoặc một mảng icon. Vàng là chữ ký, không phải màu nền.</p></div>
  <div><h3>Phối màu chữ đạt chuẩn đọc (WCAG)</h3><div class="grid" style="grid-template-columns:1fr 1fr;gap:3mm;margin-top:3mm">{pcards}</div></div></div>'''))


# --- tonal scales and grades
def tcol(h): return '#fff' if CS.grade(h) >= 45 else 'var(--ink)'
BRAND_AT = {h: n for n, h in CS.BRAND.items()}
def scale_row(name, steps, extra=(), cols=None):
    """One scale as a strip of cells (a dot marks a brand colour); brand colours that are not steps are listed with their grade."""
    cells = ''
    for k, h in steps.items():
        g = k.split('-')[1]; tag = BRAND_AT.get(h, '')
        tag_html = '<div style="position:absolute;right:1.8mm;top:1.6mm;font:400 7pt BVP">●</div>' if tag else ''
        cells += (f'<div style="background:{h};color:{tcol(h)};height:19mm;padding:1.6mm 1.8mm;position:relative;'
                  f'{"box-shadow:inset 0 0 0 .25mm rgba(0,0,0,.07);" if CS.grade(h) < 8 else ""}">'
                  f'<div style="font:600 9.5pt BVP">{g}</div><div style="font:500 5.4pt BVP;letter-spacing:.04em;opacity:.85;position:absolute;left:1.8mm;bottom:1.5mm">{h}</div>'
                  f'{tag_html}</div>')
    cols = cols or len(steps)
    members = [(BRAND_AT[h], k.replace('-', ' ').title()) for k, h in steps.items() if h in BRAND_AT]
    note = ''.join(f'<span style="margin-right:4mm">● {n} = {k}</span>' for n, k in members)
    note += ''.join(f'<span style="display:inline-flex;align-items:center;gap:1.4mm;margin-right:4mm"><i style="width:3mm;height:3mm;border-radius:.5mm;background:{CS.BRAND[n]}"></i>{n} = {CS.brand_grade(n)}</span>' for n in extra)
    return (f'<div style="display:grid;grid-template-columns:18mm 1fr;gap:3mm;align-items:start;margin-bottom:3.4mm">'
            f'<div style="font:500 11pt Lora;color:var(--blue);padding-top:1mm">{name}</div>'
            f'<div><div style="display:grid;grid-template-columns:repeat({cols},1fr);border-radius:1mm;overflow:hidden">{cells}</div>'
            f'<div class="small" style="margin-top:1.2mm;font-size:6.6pt">{note}</div></div></div>')
gold_steps = SC['Gold']
P.append(page(3, f"""<div class="grid" style="grid-template-columns:1fr 70mm;gap:10mm">
 <div><h2 style="margin-bottom:2mm">Thang sắc độ và <em>cấp độ sáng</em></h2>
  <p style="width:175mm">Mỗi màu chính có một thang sắc độ cho giao diện, biểu đồ và nền phân cấp. Con số trên mỗi ô là cấp độ sáng, từ 0 (trắng) đến 100 (gần đen). Màu thương hiệu giữ nguyên mã và nằm trong thang ở cấp của nó.</p>
  <div style="margin-top:4mm">
   {scale_row('Blue', SC['Blue'], ('Deep Navy',))}
   {scale_row('Bronze', SC['Bronze'], ('Drum Bronze', 'Bronze Ink'))}
   {scale_row('Slate', SC['Slate'], ('Slate', 'Ink'))}
   {scale_row('Gold', gold_steps, ('Drum Gold',), cols=10)}
  </div></div>
 <div style="padding-top:12mm"><h3>Quy tắc trừ cấp độ</h3>
  {''.join(f'<div style="border-top:.25mm solid var(--hair);padding:2.6mm 0;display:grid;grid-template-columns:19mm 1fr;gap:3mm;align-items:baseline"><div style="font:500 17pt Lora;color:var(--blue)">≥ {d}</div><div><b style="color:var(--blue);font-weight:600">{r}</b><div class="small">{u}</div></div></div>' for d, r, u in (('40', '3 : 1', 'Chữ lớn từ 18 pt, icon, đường và cột biểu đồ'), ('50', '4,5 : 1 · AA', 'Chữ thân bài, nhãn, số liệu'), ('70', '7 : 1 · AAA', 'Chữ nhỏ, bảng dày số liệu')))}
  <div style="margin-top:4mm;padding:3.5mm 4mm;background:var(--tint);border-left:.8mm solid var(--blue)" class="small"><b style="color:var(--blue)">Ví dụ.</b> Chữ VCCI Blue (70) trên Blue Tint (5): chênh 65, đạt AA. Chữ trắng (0) trên Blue 40: chênh 40, chỉ dùng cho chữ lớn.</div>
  <p class="small" style="margin-top:4mm">Thang sắc độ dùng cho màn hình và in kỹ thuật số (mã HEX). Khi in offset, nhờ nhà in quy đổi và in thử. Logo luôn dùng màu gốc, không dùng thang này.</p></div></div>"""))

# --- status colours
def ui_icon(slug, col, size='5.2mm'):
    svg = open(os.path.join(ROOT, 'brand-assets', '05_Icons', 'UI', 'SVG', 'currentColor', f'VCCI_UI_{slug}.svg'), encoding='utf-8').read()
    return svg.replace('<svg ', f'<svg style="width:{size};height:{size};color:{col};flex:none" ', 1)
STATUS_VI = {'Error': ('Lỗi', 'close', 'Chưa đạt yêu cầu', 'Hồ sơ thiếu giấy chứng nhận đăng ký doanh nghiệp.'),
             'Warning': ('Cảnh báo', 'alert-triangle', 'Sắp hết hạn', 'Thẻ hội viên hết hạn sau 15 ngày.'),
             'Success': ('Thành công', 'check-circle', 'Đã gửi đăng ký', 'VCCI sẽ xác nhận qua email trong hai ngày làm việc.'),
             'Info': ('Thông tin', 'info', 'Lưu ý', 'Có thể nộp hồ sơ C/O trực tuyến trên eCoSys.')}
def status_card(key):
    v = ST[key]; vi, icon, title, body = STATUS_VI[key]
    return (f'<div><div style="display:grid;grid-template-columns:1fr 1fr;height:16mm;border-radius:1mm;overflow:hidden">'
            f'<div style="background:{v["strong"]};color:#fff;padding:2mm 2.4mm;font:600 6.4pt BVP;letter-spacing:.06em">ĐẬM<br>{v["strong"]}</div>'
            f'<div style="background:{v["background"]};color:{v["strong"]};padding:2mm 2.4mm;font:600 6.4pt BVP;letter-spacing:.06em">NỀN<br>{v["background"]}</div></div>'
            f'<div style="font:500 12pt Lora;color:var(--blue);margin:3mm 0 .6mm">{vi}</div><p class="small" style="margin-bottom:3mm">{v["use"]} · chữ đậm trên nền trắng {CS.contrast(v["strong"], "#FFFFFF"):.1f} : 1</p>'
            f'<div style="background:{v["background"]};border-left:.8mm solid {v["strong"]};border-radius:.8mm;padding:3mm 3.4mm;display:flex;gap:2.6mm">{ui_icon(icon, v["strong"])}'
            f'<div><div style="font:600 8.6pt BVP;color:{v["strong"]}">{title}</div><div style="font:400 7.8pt/1.45 BVP;color:var(--ink)">{body}</div></div></div></div>')
pill = lambda key, t: f'<span style="display:inline-flex;align-items:center;gap:1mm;background:{ST[key]["background"]};color:{ST[key]["strong"]};font:600 6.8pt BVP;padding:.8mm 2.2mm .8mm 1.4mm;border-radius:3mm">{ui_icon(STATUS_VI[key][1], ST[key]["strong"], "3mm")}{t}</span>'
rows_demo = [('Hồ sơ năng lực', 'Success', 'Đạt'), ('Báo cáo tài chính 2025', 'Warning', 'Cần bổ sung'), ('Giấy phép môi trường', 'Error', 'Chưa đạt'), ('Danh sách người lao động', 'Info', 'Đang xem xét')]
P.append(page(3, f"""<h2 style="margin-bottom:2mm">Màu <em>trạng thái</em></h2>
 <p style="width:200mm">Dùng trên website, ứng dụng hội viên, biểu mẫu và bảng đánh giá để báo lỗi, cảnh báo, xác nhận và ghi chú. Mỗi trạng thái có một màu đậm cho chữ, icon, đường viền và một màu nền nhạt.</p>
 <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:6mm;margin-top:4mm">{''.join(status_card(k) for k in ST)}</div>
 <div class="grid" style="grid-template-columns:1fr 1fr;gap:12mm;margin-top:7mm">
  <div><h3>Quy tắc</h3><ul class="rules">
   <li>Luôn có <b>icon và chữ</b>; không báo trạng thái chỉ bằng màu.</li>
   <li>Chỉ dùng để báo trạng thái. Không dùng trang trí, không làm nền khối lớn, không dùng làm màu chuỗi biểu đồ.</li>
   <li>Cảnh báo dùng vàng đất, khác Drum Gold. Màu trạng thái không tính là điểm nhấn vàng của bố cục.</li>
   <li>Thông tin dùng chính VCCI Blue trên Blue Tint.</li></ul></div>
  <div><h3>Ví dụ: bảng đánh giá hồ sơ</h3>
   <div style="border-top:.4mm solid var(--blue)">{''.join(f'<div style="display:grid;grid-template-columns:1fr 34mm;align-items:center;padding:2.2mm 0;border-bottom:.25mm solid var(--hair);font:400 8.4pt BVP">{a}<span>{pill(k, t)}</span></div>' for a, k, t in rows_demo)}</div></div></div>"""))

# ================================================================ 06 TYPE
P.append(opener(4, 'Kiểu chữ', 'Hai họ chữ, cả hai đều miễn phí (giấy phép SIL OFL) và hỗ trợ đầy đủ tiếng Việt. Lora mang giọng trang trọng cho tiêu đề; Be Vietnam Pro rõ ràng cho nội dung.',
  f'''<div class="grid" style="grid-template-columns:1fr 1fr;gap:8mm">
   <div style="border-top:.4mm solid var(--blue);padding-top:4mm"><div style="font:500 70pt/1 Lora;color:var(--blue)">Aa</div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin:3mm 0"><span style="font:500 15pt Lora;color:var(--blue)">Lora</span><span class="cap">Tiêu đề · Serif</span></div>
    <p class="small">Regular · Medium · SemiBold · Italic</p><p class="small">Dùng cho tiêu đề, đoạn dẫn, trích dẫn và số liệu nổi bật.</p>
    <div style="font:400 12pt/1.5 Lora;color:var(--ink);margin-top:3mm">Đồng hành cùng doanh nghiệp Việt<br>ĂÂĐÊÔƠƯ ăâđêôơư 0123456789</div></div>
   <div style="border-top:.4mm solid var(--blue);padding-top:4mm"><div style="font:500 70pt/1 BVP;color:var(--blue)">Aa</div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin:3mm 0"><span style="font:500 15pt Lora;color:var(--blue)">Be Vietnam Pro</span><span class="cap">Nội dung · Sans</span></div>
    <p class="small">Light · Regular · Medium · SemiBold · Bold</p><p class="small">Dùng cho thân bài, nhãn, bảng biểu, giao diện và số liệu kỹ thuật.</p>
    <div style="font:400 12pt/1.5 BVP;color:var(--ink);margin-top:3mm">Đồng hành cùng doanh nghiệp Việt<br>ĂÂĐÊÔƠƯ ăâđêôơư 0123456789</div></div></div>
  <p class="small" style="margin-top:6mm">Khi không cài được font (ví dụ trên máy tính của đối tác), dùng <b>Cambria</b> thay cho Lora và <b>Arial</b> thay cho Be Vietnam Pro. Template Word của VCCI đã nhúng sẵn font nên không cần thay.</p>'''))

scale = [('Tiêu đề lớn', 'Lora Medium · 32–40 pt', 'font:500 26pt/1.1 Lora;color:var(--blue)', 'Kết nối doanh nghiệp Việt'),
         ('Tiêu đề 1', 'Lora Medium · 22 pt', 'font:500 19pt/1.2 Lora;color:var(--blue)', 'Môi trường kinh doanh 2026'),
         ('Tiêu đề 2', 'Lora SemiBold · 14 pt', 'font:600 13pt/1.3 Lora;color:var(--blue)', 'Những phát hiện chính'),
         ('Tiêu đề 3 / Nhãn', 'Be Vietnam Pro SemiBold · 8,5 pt · in hoa', 'font:600 7.6pt BVP;letter-spacing:.2em;text-transform:uppercase;color:var(--ink2)', 'Phương pháp nghiên cứu'),
         ('Đoạn dẫn', 'Lora Regular · 13 pt', 'font:400 11.5pt/1.45 Lora;color:var(--blue)', 'Hai đến ba câu nêu thông điệp quan trọng nhất.'),
         ('Thân bài', 'Be Vietnam Pro Regular · 10 pt · giãn dòng 1,4', 'font:400 9.4pt/1.55 BVP', 'Rõ ràng, chừng mực, cung cấp thông tin cho hội viên và đối tác bằng ngôn ngữ trang trọng.'),
         ('Chú thích', 'Be Vietnam Pro Regular · 7,5 pt', 'font:400 7.2pt BVP;color:var(--slate)', 'Bảng 1. Chỉ số theo năm · Nguồn: VCCI')]
srows = ''.join(f'<div style="display:grid;grid-template-columns:48mm 1fr;gap:6mm;align-items:baseline;padding:2.6mm 0;border-top:.25mm solid var(--hair)"><div><div class="cap" style="color:var(--ink2)">{a}</div><div class="small">{b}</div></div><div style="{c}">{d}</div></div>' for a, b, c, d in scale)
P.append(page(4, f'''<div class="grid" style="grid-template-columns:1fr 74mm;gap:12mm"><div><h2>Thang chữ</h2>{srows}</div>
 <div style="padding-top:12mm"><h3>Quy tắc</h3><ul class="rules">
  <li>Tiêu đề dùng <b>Lora</b>, nội dung dùng <b>Be Vietnam Pro</b>. Không thêm họ chữ thứ ba.</li>
  <li>Căn trái là mặc định. Chỉ căn giữa trên bìa, chứng nhận và slide tiêu đề.</li>
  <li>Không viết hoa toàn bộ câu dài. Chữ in hoa chỉ dùng cho nhãn ngắn, có giãn chữ.</li>
  <li>Dòng chữ thân bài dài từ 60 đến 80 ký tự.</li>
  <li>Kiểm tra dấu tiếng Việt khi đặt tiêu đề lớn sát nhau: giãn dòng tối thiểu 1,08.</li>
  <li>Chữ vàng chỉ đặt trên nền xanh. Trên nền sáng, nhấn bằng Bronze Ink hoặc chữ nghiêng Lora.</li></ul></div></div>'''))

# ================================================================ 07 MOTIFS
gtiles = [('VCCI_Drum-Ring_Line_Gold-on-Blue.svg', 'Vòng trống đồng', 'Bìa, phông sân khấu, nền khối xanh. Dùng cỡ lớn, cắt ra ngoài mép.', 'var(--blue)'),
          ('VCCI_Radiance-14_Blue.svg', 'Mặt trời 14 cánh', 'Biểu tượng mở đầu chương, điểm nhấn trên bìa sự kiện.', 'var(--gold)'),
          ('VCCI_C-Arc_Pattern_Tile.svg', 'Pattern cung chữ C', 'Dải trang trí, mặt sau danh thiếp, bao bì.', 'var(--ivory)'),
          ('VCCI_Drum-Dot_Field.svg', 'Trường chấm', 'Nền nhẹ cho slide, dải chân trang, ảnh bìa mạng xã hội.', '#fff')]
gcards = ''.join(f'''<div><div class="card" style="height:62mm;background:{bg};box-shadow:inset 0 0 0 .25mm var(--hair)"><img src="{U('brand-assets', '04_Graphics', f)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"></div>
 <div style="font:500 11pt Lora;color:var(--blue);margin-top:3mm">{n}</div><p class="small">{d}</p></div>''' for f, n, d, bg in gtiles)
P.append(opener(5, 'Họa tiết', 'Mọi họa tiết đều được phát triển từ trống đồng và hình chữ C trong logo. Chúng tạo nên không khí thương hiệu, kể cả khi logo không xuất hiện.',
  f'<div class="grid" style="grid-template-columns:1fr 1fr;gap:6mm 7mm">{gcards}</div>'.replace('height:62mm', 'height:50mm')))

P.append(page(5, f'''<h2>Dùng họa tiết <em>đúng cách</em></h2>
 <div class="grid" style="grid-template-columns:1fr 1fr 1fr;gap:7mm">
  <div><div class="card" style="height:74mm;background:linear-gradient(160deg,#2B4FA0,#1E3D86)"><svg viewBox="-300 -300 600 600" style="position:absolute;width:120mm;height:120mm;right:-45mm;top:-30mm">{BA.drum('#fff', BA.GOLD, .7, .18, .6)}</svg>
   <div style="position:absolute;left:6mm;bottom:7mm;font:500 14pt/1.15 Lora;color:#fff">Vietnam Business<br><span style="color:var(--gold)">Summit 2026</span></div></div>
   <div class="ok" style="margin-top:3mm">Đúng</div><p class="small">Họa tiết lớn, cắt ra ngoài mép, nét mảnh, độ mờ thấp. Chữ nằm ở vùng trống.</p></div>
  <div><div class="card x" style="height:74mm;background:var(--blue)"><div style="display:grid;grid-template-columns:repeat(4,1fr);align-content:center;height:100%">{''.join(f'<svg viewBox="-300 -300 600 600" style="width:100%;height:100%">{BA.drum("#fff", BA.GOLD, 1.6, .9, 1)}</svg>' for _ in range(8))}</div></div>
   <div class="bad" style="margin-top:3mm">Sai</div><p class="small">Lặp nhỏ, dày đặc, độ đậm cao: họa tiết lấn át nội dung và giống giấy gói quà.</p></div>
  <div><div class="card x" style="height:74mm;background:#fff;box-shadow:inset 0 0 0 .25mm var(--hair)"><svg viewBox="-300 -300 600 600" style="position:absolute;width:60mm;height:60mm;left:50%;top:50%;transform:translate(-50%,-50%)">{BA.drum('#C23B22', '#2E9E5B', 1.4, .9, 1)}</svg></div>
   <div class="bad" style="margin-top:3mm">Sai</div><p class="small">Đổi sang màu ngoài bảng màu, hoặc đặt họa tiết vào giữa như một logo thứ hai.</p></div></div>
 <ul class="rules" style="margin-top:6mm;columns:2;column-gap:12mm">
  <li>Mỗi bố cục dùng <b>một</b> họa tiết chính.</li><li>Trên nền xanh: nét trắng mờ 12–20%, phần sao và chấm màu vàng.</li>
  <li>Trên nền sáng: nét xanh mờ 8–15%, không dùng vàng đậm.</li><li>Không đặt họa tiết sau đoạn văn dài; chỉ dùng ở vùng trống.</li>
  <li>Không ghép họa tiết với logo thành một khối mới.</li><li>Không dùng ảnh chụp trống đồng thay cho họa tiết vẽ nét.</li></ul>'''))

# ================================================================ 08 ICONS & ILLUSTRATION
P.append(opener(6, 'Icon và minh họa', 'Hệ thống icon gồm hai cấp: 48 icon nhỏ cho giao diện và văn bản, 24 hero icon riêng cho các lĩnh vực hoạt động của VCCI. Phần này cũng đặt nguyên tắc cho minh họa.',
  f'''<div class="grid" style="grid-template-columns:1fr 1fr;gap:8mm">
   <div class="card" style="padding:6mm;height:118mm"><h3>Cấp 1 · Icon nhỏ (UI)</h3><div style="font:500 13pt Lora;color:var(--blue);margin-bottom:4mm">Chức năng, nhận biết nhanh</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:5mm;margin:6mm 0">{''.join(f'<img src="{ICON("UI", "Blue", f"VCCI_UI_{s}.svg")}" style="width:10mm;height:10mm">' for s, _ in UI[14:26])}</div>
    <ul class="rules"><li>Lưới 24 × 24, nét 1,6</li><li>Dựa trên thư viện Lucide (giấy phép ISC)</li><li>Cỡ dùng: 16–32 px, 4–8 mm</li></ul></div>
   <div class="card" style="padding:6mm;height:118mm"><h3>Cấp 2 · Hero icon</h3><div style="font:500 13pt Lora;color:var(--blue);margin-bottom:4mm">Chủ đề, nhận diện riêng VCCI</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin:6mm 0">{''.join(f'<img src="{ICON("Hero", "Blue-Gold", f"VCCI_Hero_{n}_{s}.svg")}" style="width:17mm;height:17mm">' for n, s, _ in HERO[:6])}</div>
    <ul class="rules"><li>Lưới 64 × 64, nét 2</li><li>Thiết kế riêng, một mảng vàng ≤ 25%</li><li>Cỡ dùng: từ 48 px, 12 mm trở lên</li></ul></div></div>'''))

uicells = ''.join(f'<div><img src="{ICON("UI", "Blue", f"VCCI_UI_{s}.svg")}"><span>{vi}</span></div>' for s, vi in UI)
P.append(page(6, f'''<div class="grid" style="grid-template-columns:1fr 62mm;gap:10mm"><div><h2>Icon nhỏ <em>· 48 icon</em></h2><div class="icons">{uicells}</div></div>
 <div style="padding-top:12mm"><img src="{U('docs', 'handoff-icons', 'pack', 'templates', 'VCCI_UI-Icon_Grid_24.svg')}" style="width:40mm;margin-bottom:3mm">
  <p class="cap" style="margin-bottom:4mm">Lưới 24 px · vùng vẽ 20 px</p>
  <ul class="rules"><li><b>Nét</b> 1,6 px, đầu và góc bo tròn</li><li><b>Không tô</b> mảng, chỉ dùng nét</li><li><b>Màu</b> xanh trên nền sáng; vàng hoặc trắng trên nền xanh</li><li><b>File</b> SVG (currentColor, Blue, Gold, White) và PNG 48/96 px</li></ul></div></div>'''))

hcells = ''.join(f'<div><img src="{ICON("Hero", "Blue-Gold", f"VCCI_Hero_{n}_{s}.svg")}"><b>{n}</b><span>{vi}</span></div>' for n, s, vi in HERO)
P.append(page(6, f'''<h2>Hero icon <em>· 24 lĩnh vực</em></h2><div class="heros">{hcells}</div>
 <p class="small" style="margin-top:4mm">Các chủ đề chính sách (01–06, 09–10) mang tính trừu tượng: luôn đặt nhãn chữ bên cạnh ở lần xuất hiện đầu tiên. Gợi ý ghép icon với loại tài liệu nằm trong file <b>05_Icons/HANDBACK_TO_CLAUDE.md</b>.</p>'''))

def hero_demo(bg, variant, ok, label, note, n='13', slug='membership'):
    return (f'<div><div class="card {"" if ok else "x"}" style="height:54mm;background:{bg};display:flex;align-items:center;justify-content:center;{"box-shadow:inset 0 0 0 .25mm var(--hair)" if bg in ("#fff", "var(--paper)") else ""}">'
            f'<img src="{ICON("Hero", variant, f"VCCI_Hero_{n}_{slug}.svg")}" style="width:28mm;height:28mm"></div>'
            f'<div class="{"ok" if ok else "bad"}" style="margin-top:2.4mm">{label}</div><p class="small">{note}</p></div>')
P.append(page(6, f'''<h2>Dùng icon <em>đúng cách</em></h2>
 <div class="grid" style="grid-template-columns:repeat(6,1fr);gap:5mm">
  {hero_demo('var(--paper)', 'Blue-Gold', True, 'Đúng', 'Xanh và vàng trên nền sáng. Bản chính.')}
  {hero_demo('#fff', 'Blue', True, 'Đúng', 'Chỉ nét xanh, khi trang đã có điểm nhấn vàng khác.')}
  {hero_demo('var(--blue)', 'Gold-on-dark', True, 'Đúng', 'Nét vàng trên nền xanh.')}
  {hero_demo('var(--deep)', 'White', True, 'Đúng', 'Nét trắng trên nền tối.')}
  {hero_demo('var(--paper)', 'Gold-on-dark', False, 'Sai', 'Vàng hoặc trắng trên nền sáng: không đủ tương phản.')}
  {hero_demo('var(--blue)', 'Blue', False, 'Sai', 'Xanh trên nền xanh.')}</div>
 <div class="grid" style="grid-template-columns:1fr 1fr;gap:12mm;margin-top:7mm">
  <div><h3>Nhãn và khả năng tiếp cận</h3><ul class="rules"><li>Hero icon luôn đi kèm nhãn chữ, trừ khi tiêu đề bên cạnh đã nêu rõ chủ đề.</li><li>Không dùng icon đơn lẻ để truyền đạt khái niệm chính sách hay trạng thái.</li><li>Trên web: đặt tên mô tả (alt) cho icon mang nghĩa; ẩn icon trang trí.</li></ul></div>
  <div><h3>Không được</h3><ul class="rules no"><li>Đặt logo hoặc trống đồng vào trong icon.</li><li>Thêm khung, huy hiệu, tia sáng hay bóng đổ quanh icon.</li><li>Thay đổi độ dày nét, thu phóng không đều, hoặc tự vẽ thêm icon khác phong cách.</li></ul></div></div>'''))

# --- illustration principles (constructed examples)
attrs_dialog, inner_dialog = hero_svg_inner('06', 'public-private-dialogue', 'Blue')
attrs_train, inner_train = hero_svg_inner('18', 'training', 'Blue')
def scene(stroke_w=2, col='#264896', accent=True, accent_big=False, extra='', filt='', stroke_col_override=None):
    sc = stroke_col_override or col
    a = inner_dialog.replace('#264896', sc); b = inner_train.replace('#264896', sc)
    acc = ''
    if accent: acc = f'<circle cx="150" cy="60" r="{90 if accent_big else 26}" fill="#FFCD00"/>'
    return (f'<svg viewBox="0 0 240 120" style="width:100%;height:100%;{filt}">{acc}{extra}'
            f'<g transform="translate(18,30) scale(1.25)" fill="none" stroke="{sc}" stroke-width="{stroke_w}" stroke-linecap="round" stroke-linejoin="round">{re.sub(r"stroke-width=\"[\d.]+\"", "", a)}</g>'
            f'<g transform="translate(140,34) scale(1.15)" fill="none" stroke="{sc}" stroke-width="{stroke_w}" stroke-linecap="round" stroke-linejoin="round">{re.sub(r"stroke-width=\"[\d.]+\"", "", b)}</g>'
            f'<line x1="10" y1="112" x2="230" y2="112" stroke="{sc}" stroke-width="{stroke_w}" stroke-linecap="round"/></svg>')
hatch = '<defs><pattern id="h" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="4" stroke="#264896" stroke-width="1"/></pattern></defs><rect x="30" y="60" width="70" height="44" fill="url(#h)"/>'
P.append(page(6, f'''<div class="grid" style="grid-template-columns:78mm 1fr;gap:12mm"><div><h2>Nguyên tắc <em>minh họa</em></h2>
  <p>Ưu tiên ảnh chụp thật về doanh nghiệp và con người Việt Nam. Minh họa dùng khi chủ đề trừu tượng, nhạy cảm hoặc phức tạp, hoặc khi cần giọng điệu nhẹ nhàng hơn.</p>
  <ul class="rules"><li><b>Nét đơn, liền, cùng một độ dày</b> trong toàn bộ minh họa, cùng độ dày với icon đi kèm.</li><li><b>Chỉ màu thương hiệu:</b> xanh, vàng, nâu đồng, trắng và các sắc độ nhạt.</li><li><b>Vàng đặc ≤ 1/4</b> diện tích minh họa.</li><li><b>Không đổ bóng</b>, không gạch bóng, không chấm, không chuyển màu trong hình.</li><li>Minh họa mua từ thư viện ảnh được phép dùng nếu chỉnh về đúng nét và màu.</li></ul></div>
 <div><div class="grid" style="grid-template-columns:1fr 1fr;gap:6mm">
  <div><div class="card" style="height:84mm;padding:8mm">{scene()}</div><div class="ok" style="margin-top:2.4mm">Đúng</div><p class="small">Nét xanh đều, một mảng vàng phía sau, nhiều khoảng trống.</p></div>
  <div><div class="card" style="height:84mm;padding:8mm;background:var(--blue)">{scene(col='#FFCD00', accent=False, stroke_col_override='#FFFFFF').replace('<line x1="10"', '<circle cx="150" cy="60" r="26" fill="#FFCD00" opacity=".9"/><line x1="10"')}</div><div class="ok" style="margin-top:2.4mm">Đúng</div><p class="small">Bản nét trắng trên nền xanh, điểm nhấn vàng nhỏ.</p></div></div>
  <div style="margin-top:6mm;padding:4mm 5mm;background:var(--tint);border-left:.8mm solid var(--blue)" class="small"><b style="color:var(--blue)">Kết hợp đồ họa.</b> Icon, họa tiết trống đồng và ảnh chụp có thể ghép thành một "bộ nhận diện chủ đề" cho một chương trình hay một năm hoạt động, miễn là mỗi thành phần vẫn theo đúng quy tắc riêng của nó.</div></div></div>'''))

wrong = [(scene(stroke_w=3.4).replace('stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">', 'stroke-width="1" stroke-linecap="round" stroke-linejoin="round">', 1), 'Nhiều độ dày nét trong cùng một hình.'),
         (scene(extra=hatch), 'Gạch bóng, đổ bóng hoặc tạo khối.'),
         (scene(col='#C23B22', stroke_col_override='#C23B22').replace('#FFCD00', '#2E9E5B'), 'Màu ngoài bảng màu thương hiệu.'),
         (scene(accent_big=True), 'Vàng đặc phủ quá 1/4 diện tích.'),
         (scene(filt='filter:drop-shadow(2px 3px 2px rgba(0,0,0,.45))'), 'Bóng đổ và hiệu ứng nổi.'),
         (scene().replace('<line x1="10"', f'<image href="{U("brand-assets", "01_Logo", "_Construction-only", "VCCI_Drum_CONSTRUCTION-ONLY.svg")}" x="100" y="2" width="40" height="40"/><line x1="10"'), 'Đưa logo hoặc trống đồng vào minh họa.')]
wcards = ''.join(f'<div><div class="card x" style="height:60mm;padding:6mm">{s}</div><div class="bad" style="margin-top:2.4mm">Sai</div><p class="small">{d}</p></div>' for s, d in wrong)
P.append(page(6, f'''<h2>Minh họa: những điều <em>không được làm</em></h2>
 <div class="grid" style="grid-template-columns:repeat(3,1fr);gap:6mm 8mm">{wcards}</div>'''))

# ================================================================ 09 LAYOUT
P.append(opener(7, 'Bố cục', 'Bố cục VCCI dựa trên lưới 12 cột, khoảng cách bội số của 8 và nhiều khoảng trống. Sự nhất quán đến từ việc lặp lại một vài quyết định đơn giản trên mọi ấn phẩm.',
  f'''<div class="grid" style="grid-template-columns:auto 1fr;gap:10mm;align-items:start">
   <div style="width:72mm;height:102mm;background:#fff;box-shadow:0 1mm 4mm rgba(0,0,0,.14);position:relative">
    <div style="position:absolute;inset:7mm;display:grid;grid-template-columns:repeat(12,1fr);gap:1.4mm">{''.join('<i style="background:rgba(255,205,0,.14)"></i>' for _ in range(12))}</div>
    <div style="position:absolute;inset:7mm;outline:.25mm dashed var(--ink2)"></div>
    <img src="{LOGO}" style="position:absolute;left:7mm;top:7mm;width:20mm">
    <div style="position:absolute;left:7mm;top:20mm;width:5mm;height:.5mm;background:var(--gold)"></div>
    <div style="position:absolute;left:7mm;top:24mm;font:500 10pt/1.15 Lora;color:var(--blue)">Báo cáo<br>thường niên 2026</div>
    {''.join(f'<i style="position:absolute;left:7mm;top:{40 + i * 3.2}mm;height:.9mm;width:{58 - (i % 3) * 6}mm;background:var(--stone)"></i>' for i in range(8))}
    <div style="position:absolute;left:0;right:0;bottom:0;height:28mm;background:var(--blue)"></div>
    <span class="cap" style="position:absolute;left:1mm;top:1.5mm;font-size:5pt;color:var(--ink2)">lề = 2x</span></div>
   <div><h3>Thang khoảng cách (pt / px)</h3>{''.join(f'<div style="display:grid;grid-template-columns:12mm 1fr;align-items:center;height:5.6mm"><span class="small">{v}</span><i style="height:2.2mm;width:{v * .42}mm;background:var(--gold)"></i></div>' for v in (8, 16, 24, 32, 48, 64, 96, 128))}
    <ul class="rules" style="margin-top:5mm"><li><b>Lề trang</b> bằng 2x (hai lần bán kính trống đồng của logo đặt trên trang); với A4 khoảng 20–22 mm.</li><li><b>Lưới 12 cột</b> cho A4, slide và web.</li><li><b>Bo góc</b> 4 px cho ấn phẩm in, 8 px cho giao diện.</li></ul></div></div>'''))

P.append(page(7, f'''<h2>Năm quy tắc <em>nhất quán</em></h2>
 <div class="grid" style="grid-template-columns:repeat(5,1fr);gap:6mm;margin-top:4mm">
 {''.join(f'<div style="border-top:.5mm solid var(--blue);padding-top:4mm"><div style="font:500 40pt Lora;color:var(--gold);-webkit-text-stroke:.2mm var(--ink2)">{i}</div><div style="font:500 14pt/1.25 Lora;color:var(--blue);margin:3mm 0 3mm">{a}</div><p class="small" style="font-size:9pt">{b}</p></div>' for i, (a, b) in enumerate([
   ('Logo một màu, trên nền sáng', 'Chữ VCCI Blue, trống đồng màu gốc. Trên nền xanh hoặc ảnh, dùng ô nền sáng.'),
   ('Một điểm nhấn vàng', 'Một đường gạch, một con số hoặc một icon. Không dùng vàng làm màu nền chính.'),
   ('Hai họ chữ', 'Lora cho tiêu đề, Be Vietnam Pro cho nội dung. Không thêm font thứ ba.'),
   ('40% khoảng trống', 'Tối thiểu 40% diện tích để trống. Thà bỏ bớt nội dung còn hơn nhồi nhét.'),
   ('Bắt đầu từ template', 'Mọi văn bản, báo cáo, thư mời đều tạo từ template chính thức của VCCI.')], 1))}</div>
 <div class="grid" style="grid-template-columns:1fr 1fr;gap:12mm;margin-top:16mm;padding-top:8mm;border-top:.25mm solid var(--hair)">
  <div><h3>Ảnh chụp</h3><p class="small" style="font-size:8.4pt">Ảnh thật về doanh nghiệp, nhà máy, hội nghị và con người Việt Nam; ánh sáng tự nhiên; bố cục có khoảng trống để đặt chữ. Tránh ảnh stock dàn dựng, ảnh bắt tay khuôn sáo, ảnh có màu sắc quá rực.</p></div>
  <div><h3>Song ngữ</h3><p class="small" style="font-size:8.4pt">Tiếng Việt đứng trước. Bản tiếng Anh đặt bên dưới hoặc bên phải, cỡ nhỏ hơn, dùng chữ nghiêng Lora hoặc màu Slate để phân cấp. Tên chính thức: Liên đoàn Thương mại và Công nghiệp Việt Nam / Vietnam Chamber of Commerce and Industry.</p></div></div>'''))

# ================================================================ 08 DATA & CHARTS
DEMO = '<span class="cap" style="color:var(--slate)">Số liệu minh họa</span>'
def axis_text(x, y, t, anchor='middle', size=9, col='#5C6478', weight=400, fam='BVP'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{weight}" font-size="{size}" fill="{col}">{t}</text>'

def column_chart(vals, colours, w=300, h=170, lo=0, hi=None, labels=True, label_idx=None):
    hi = hi or max(v for _, v in vals) * 1.15; n = len(vals)
    x0, x1, y0, y1 = 26, w - 6, 14, h - 22
    bw = (x1 - x0) / n * .62; step = (x1 - x0) / n
    yv = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)
    g = ''.join(f'<line x1="{x0}" x2="{x1}" y1="{yv(t):.1f}" y2="{yv(t):.1f}" stroke="#E6E1D5" stroke-width=".6"/>{axis_text(x0 - 4, yv(t) + 3, t, "end", 7.5)}'
                for t in range(int(lo), int(hi) + 1, max(1, int((hi - lo) / 4 // 5 * 5) or 1)) if t <= hi)
    b = ''
    for i, ((lab, v), c) in enumerate(zip(vals, colours)):
        x = x0 + i * step + (step - bw) / 2
        b += f'<rect x="{x:.1f}" y="{yv(v):.1f}" width="{bw:.1f}" height="{y1 - yv(v):.1f}" fill="{c}"/>'
        if labels and (label_idx is None or i in label_idx):
            b += axis_text(x + bw / 2, yv(v) - 3, f'{v:g}'.replace('.', ','), size=8, col='#264896', weight=500, fam='Lora')
        b += axis_text(x + bw / 2, y1 + 11, lab, size=7.5)
    return f'<svg viewBox="0 0 {w} {h}" style="width:100%;display:block">{g}<line x1="{x0}" x2="{x1}" y1="{y1}" y2="{y1}" stroke="#5C6478" stroke-width=".8"/>{b}</svg>'

def line_chart(series, years, w=300, h=170, lo=0, hi=100):
    x0, x1, y0, y1 = 26, w - 70, 12, h - 22
    xv = lambda i: x0 + i * (x1 - x0) / (len(years) - 1)
    yv = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)
    g = ''.join(f'<line x1="{x0}" x2="{x1}" y1="{yv(t):.1f}" y2="{yv(t):.1f}" stroke="#E6E1D5" stroke-width=".6"/>{axis_text(x0 - 4, yv(t) + 3, t, "end", 7.5)}' for t in range(lo, hi + 1, (hi - lo) // 4))
    g += ''.join(axis_text(xv(i), y1 + 11, y, size=7.5) for i, y in enumerate(years))
    out = ''
    for name, col, vals in series:
        pts = ' '.join(f'{xv(i):.1f},{yv(v):.1f}' for i, v in enumerate(vals))
        out += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
        out += f'<circle cx="{xv(len(vals) - 1):.1f}" cy="{yv(vals[-1]):.1f}" r="2.4" fill="{col}"/>'
        out += axis_text(xv(len(vals) - 1) + 6, yv(vals[-1]) + 3, name, 'start', 8, col if col != '#8FA6D6' else '#5474B7', 600)
    return f'<svg viewBox="0 0 {w} {h}" style="width:100%;display:block">{g}{out}</svg>'

def stacked_bars(rows, cats, colours, w=300, h=170):
    x0, x1 = 84, w - 6; bh = 15; gap = (h - 40 - len(rows) * bh) / max(len(rows) - 1, 1)
    out = ''
    for r, (lab, vals) in enumerate(rows):
        y = 6 + r * (bh + gap); x = x0; tot = sum(vals)
        out += axis_text(x0 - 5, y + bh / 2 + 3, lab, 'end', 7.5, '#161A26')
        for v, c in zip(vals, colours):
            ww = (x1 - x0) * v / tot
            out += f'<rect x="{x:.1f}" y="{y:.1f}" width="{ww:.1f}" height="{bh}" fill="{c}" stroke="#fff" stroke-width=".8"/>'
            if ww > 16: out += axis_text(x + ww / 2, y + bh / 2 + 3, f'{round(100 * v / tot)}%', size=7, col='#fff' if CS.grade(c) >= 45 else '#161A26', weight=600)
            x += ww
    lx = x0; ly = h - 12
    for cname, c in zip(cats, colours):
        out += f'<rect x="{lx}" y="{ly - 6}" width="7" height="7" fill="{c}"/>' + axis_text(lx + 10, ly, cname, 'start', 7.2, '#161A26')
        lx += 12 + len(cname) * 4.4
    return f'<svg viewBox="0 0 {w} {h}" style="width:100%;display:block">{out}</svg>'

cat = DV['categorical']
cat_strip = ''.join(f'<div><div style="height:14mm;border-radius:1mm;background:{h};color:{"#fff" if CS.grade(h) >= 45 else "var(--ink)"};padding:1.6mm 2mm;font:600 9pt BVP">{i}</div>'
                    f'<div style="font:500 7.4pt BVP;color:var(--ink);margin-top:1.4mm">{n}</div><div class="small" style="font-size:6.4pt">{h}</div></div>' for i, (n, h) in enumerate(cat, 1))
principles = [('Rõ ràng', 'Mỗi biểu đồ nói một thông điệp; tiêu đề nêu thông điệp đó.'), ('Chính xác', 'Trục cột bắt đầu từ 0, khoảng chia đều, không bóp méo tỉ lệ.'),
              ('Dễ tiếp cận', 'Không truyền tải thông tin chỉ bằng màu; ghi nhãn trực tiếp.'), ('Nhất quán', 'Cùng thứ tự màu, cùng kiểu chữ trên mọi báo cáo và slide.'),
              ('Có nguồn', 'Ghi nguồn và năm số liệu dưới mỗi biểu đồ.')]
P.append(opener(8, 'Dữ liệu và biểu đồ', 'VCCI công bố nhiều báo cáo số liệu. Biểu đồ phải đọc đúng, đọc nhanh, và nhìn qua là nhận ra của VCCI.',
  f"""<h3>Năm nguyên tắc</h3>
  <div class="grid" style="grid-template-columns:repeat(5,1fr);gap:5mm;margin-bottom:9mm">{''.join(f'<div style="border-top:.4mm solid var(--blue);padding-top:2.6mm"><div style="font:500 12pt Lora;color:var(--blue);margin-bottom:1.2mm">{a}</div><p class="small">{b}</p></div>' for a, b in principles)}</div>
  <h3>Màu chuỗi dữ liệu · theo đúng thứ tự</h3>
  <div class="grid" style="grid-template-columns:repeat(6,1fr);gap:3mm">{cat_strip}</div>
  <div style="margin-top:6mm;padding:3.5mm 4.5mm;background:var(--tint);border-left:.8mm solid var(--blue)" class="small"><b style="color:var(--blue)">Vàng không phải màu chuỗi.</b> Drum Gold chỉ dùng để nhấn <b>một</b> giá trị quan trọng nhất, luôn kèm nhãn số. Tối đa sáu chuỗi; nhiều hơn thì gộp nhóm nhỏ thành "Khác" hoặc tách thành nhiều biểu đồ nhỏ.<br><b style="color:var(--blue)">Trong Office.</b> Theme Office VCCI (Word, Excel, PowerPoint) xếp accent 1–5 theo đúng thứ tự màu chuỗi, accent 6 là Drum Gold. Biểu đồ mới tự nhận màu chuỗi 1–5; nếu có chuỗi thứ sáu, đổi tay sang Deep Navy (Text/Background Dark 2).</div>
  <h3 style="margin-top:8mm">Nhấn một giá trị</h3>
  <div class="grid" style="grid-template-columns:repeat(3,1fr);gap:5mm">{''.join(f'<div style="display:grid;grid-template-columns:14mm 1fr;gap:3mm;align-items:center"><i style="height:14mm;border-radius:1mm;background:{h}"></i><div><div style="font:500 10pt Lora;color:var(--blue)">{a}</div><div class="small">{b} · {h}</div></div></div>' for a, b, h in (('Giá trị nhấn', 'Drum Gold, kèm nhãn số', DV['highlight']['focus']), ('Giá trị thường', 'VCCI Blue', DV['highlight']['context']), ('Giá trị lùi', 'Slate 20, khi nhiều mục', DV['highlight']['muted'])))}</div>"""))

yrs = ['2020', '2021', '2022', '2023', '2024', '2025']
line = line_chart([('Hà Nội', cat[0][1], [61, 62, 63.5, 65, 66.8, 68.6]), ('TP.HCM', cat[1][1], [64, 65, 65.5, 66, 66.3, 66.2]), ('Đà Nẵng', cat[2][1], [66, 65, 65.5, 65.2, 64.5, 63.6])], yrs, lo=55, hi=75, h=150)
hl_vals = list(zip(yrs, [63.2, 64.5, 65.1, 64.8, 66.0, 67.4]))
hl = column_chart(hl_vals, [cat[0][1]] * 5 + [DV['highlight']['focus']], label_idx={5}, hi=80, h=150)
muted = column_chart(list(zip(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], [42, 38, 35, 33, 31, 28, 24, 20])), [DV['highlight']['muted']] * 3 + [cat[0][1]] + [DV['highlight']['muted']] * 4, label_idx={3}, hi=50, h=150)
stack = stacked_bars([('Doanh nghiệp nhỏ', [46, 30, 16, 8]), ('Doanh nghiệp vừa', [38, 34, 19, 9]), ('Doanh nghiệp lớn', [29, 37, 24, 10])],
                     ['Tốt', 'Khá', 'Trung bình', 'Kém'], [cat[0][1], cat[1][1], cat[4][1], cat[2][1]], h=150)
def chart_card(title, svg, note, ok=True):
    return (f'<div><div class="card" style="background:#fff;box-shadow:inset 0 0 0 .25mm var(--hair);padding:4mm 4mm 3mm">'
            f'<div style="font:500 10pt/1.3 Lora;color:var(--blue);margin-bottom:2mm">{title}</div>{svg}'
            f'<div class="small" style="font-size:6.4pt;margin-top:1mm">Nguồn: VCCI · {DEMO}</div></div>'
            f'<p class="small" style="margin:1.6mm 0 0"><span class="{"ok" if ok else "bad"}">{"Đúng" if ok else "Sai"}</span>&nbsp; {note}</p></div>')
P.append(page(8, f"""<div class="grid" style="grid-template-columns:1fr 66mm;gap:10mm">
 <div><h2 style="margin-bottom:2.4mm">Màu chuỗi và <em>điểm nhấn</em></h2>
 <div class="grid" style="grid-template-columns:1fr 1fr;gap:3.4mm 6mm">
  {chart_card('Hà Nội vượt TP.HCM và Đà Nẵng từ năm 2024', line, 'Ba chuỗi theo thứ tự 1–2–3. Ghi tên ở cuối đường thay cho chú giải.')}
  {chart_card('Năm 2025 đạt điểm cao nhất trong sáu năm', hl, 'Một cột vàng có nhãn số; các cột còn lại VCCI Blue.')}
  {chart_card('Ngành D đứng thứ tư trong tám ngành', muted, 'Khi cần làm nổi một mục giữa nhiều mục: mục đó VCCI Blue, còn lại Slate 20.')}
  {chart_card('Doanh nghiệp nhỏ đánh giá tích cực hơn', stack, 'Cơ cấu phần trăm: thang thứ bậc từ tốt (xanh) đến kém (đồng), chữ số trên mảng.')}</div></div>
 <div style="padding-top:13mm">
  <div><h3>Chữ trong biểu đồ</h3><ul class="rules">
   <li><b>Tiêu đề</b> Lora Medium, nêu thông điệp chứ không chỉ tên số liệu.</li>
   <li><b>Nhãn, trục, chú giải</b> Be Vietnam Pro Regular màu Slate; nhãn số Lora màu VCCI Blue.</li>
   <li><b>Nguồn</b> cỡ chú thích, đặt dưới biểu đồ: "Nguồn: VCCI, Khảo sát PCI 2025".</li></ul></div>
  <div style="margin-top:5mm"><h3>Đường nét</h3><ul class="rules">
   <li>Lưới ngang mảnh màu Stone; bỏ lưới dọc và khung viền.</li>
   <li>Trục đáy màu Slate. Số thập phân dùng dấu phẩy theo cách viết tiếng Việt.</li>
   <li>Không 3D, không bóng đổ, không chuyển màu trong cột.</li></ul></div></div>"""))

# --- sequential and diverging
regions = ['Đồng bằng sông Hồng', 'Trung du và miền núi phía Bắc', 'Bắc Trung Bộ và duyên hải miền Trung', 'Tây Nguyên', 'Đông Nam Bộ', 'Đồng bằng sông Cửu Long']
hm = [[64.1, 65.0, 65.8, 66.2, 67.5, 68.3], [60.2, 60.9, 61.8, 62.0, 63.1, 63.9], [62.0, 62.6, 63.9, 64.4, 65.2, 66.0],
      [59.0, 59.8, 60.1, 61.2, 61.9, 62.7], [65.2, 65.9, 66.1, 67.0, 67.8, 68.9], [62.8, 63.5, 64.0, 64.9, 65.5, 66.6]]
seq = DV['sequential_7']; lo_, hi_ = 59, 69.5
cls = lambda v: seq[min(6, max(0, int((v - lo_) / (hi_ - lo_) * 7)))]
heat = ''.join(f'<div style="display:grid;grid-template-columns:44mm repeat(6,1fr);gap:.8mm;margin-bottom:.8mm"><div style="font:400 7.2pt/1.25 BVP;align-self:center">{r}</div>'
               + ''.join(f'<div style="background:{cls(v)};color:{"#fff" if CS.grade(cls(v)) >= 45 else "var(--ink)"};font:500 7pt BVP;text-align:center;padding:1.6mm 0">{f"{v:.1f}".replace(".", ",")}</div>' for v in row) + '</div>'
               for r, row in zip(regions, hm))
heat_head = '<div style="display:grid;grid-template-columns:44mm repeat(6,1fr);gap:.8mm;margin-bottom:1mm"><span></span>' + ''.join(f'<span class="small" style="text-align:center;font-size:6.8pt">{y}</span>' for y in yrs) + '</div>'
div = DV['diverging_7']
chg = [('Tiếp cận đất đai', -1.8), ('Chi phí thời gian', -0.9), ('Chi phí không chính thức', -0.3), ('Tính minh bạch', 0.2), ('Cạnh tranh bình đẳng', 0.9), ('Đào tạo lao động', 1.6), ('Hỗ trợ doanh nghiệp', 2.3)]
def dcol(v):
    a = abs(v); k = 0 if a < .5 else (1 if a < 1.2 else (2 if a < 2 else 3))
    return div[3 - k] if v < 0 else div[3 + k]
cx, sc_ = 150, 40
dbars = ''
for i, (lab, v) in enumerate(chg):
    y = 6 + i * 21; x = cx if v >= 0 else cx + v * sc_; col = dcol(v) if abs(v) >= .5 else (div[2] if v < 0 else div[4])
    dbars += f'<rect x="{x:.1f}" y="{y}" width="{abs(v) * sc_:.1f}" height="13" fill="{col}"/>'
    dbars += axis_text(cx - 6 if v >= 0 else x - 4, y + 9.5, lab, 'end', 7.5, '#161A26')
    dbars += axis_text(x + abs(v) * sc_ + 4 if v >= 0 else cx + 4, y + 9.5, (f'+{v:.1f}' if v > 0 else f'{v:.1f}').replace('.', ','), 'start', 7.5, '#264896' if v > 0 else '#9C570C', 600)
dsvg = f'<svg viewBox="0 0 300 156" style="width:100%;display:block"><line x1="{cx}" x2="{cx}" y1="0" y2="152" stroke="#5C6478" stroke-width=".8"/>{dbars}</svg>'
def ramp(cols, labels):
    cells = ''.join(f'<i style="height:7mm;background:{c}"></i>' for c in cols)
    return (f'<div style="display:grid;grid-template-columns:repeat({len(cols)},1fr);border-radius:1mm;overflow:hidden">{cells}</div>'
            f'<div class="small" style="display:flex;justify-content:space-between;font-size:6.6pt;margin-top:1mm">{"".join(f"<span>{t}</span>" for t in labels)}</div>')
P.append(page(8, f"""<h2 style="margin-bottom:3mm">Thang <em>tuần tự</em> và thang <em>phân kỳ</em></h2>
 <div class="grid" style="grid-template-columns:1.15fr 1fr;gap:12mm">
  <div><h3>Tuần tự · giá trị có thứ bậc, bản đồ</h3>{ramp(seq, ['Thấp', 'Blue 10 → Blue 70', 'Cao'])}
   <p class="small" style="margin-top:3mm">Dùng cho điểm số, tỉ lệ, xếp hạng và bản đồ tô màu theo tỉnh (ví dụ PCI). Nhạt là thấp, đậm là cao. Bản đồ có ít nhóm dùng bản 5 bậc: {", ".join(DV["sequential_5"])}.</p>
   <div class="card" style="background:#fff;box-shadow:inset 0 0 0 .25mm var(--hair);padding:4mm;margin-top:3mm">
    <div style="font:500 10pt Lora;color:var(--blue);margin-bottom:2.4mm">Đông Nam Bộ và Đồng bằng sông Hồng dẫn đầu</div>{heat_head}{heat}
    <div class="small" style="font-size:6.4pt;margin-top:1.6mm">Nguồn: VCCI · {DEMO}</div></div></div>
  <div><h3>Phân kỳ · tăng và giảm quanh một mốc</h3>{ramp(div, ['Giảm', 'Ivory = không đổi', 'Tăng'])}
   <p class="small" style="margin-top:3mm">Dùng khi số liệu xoay quanh một mốc: thay đổi so với năm trước, chênh lệch so với trung bình. Đồng là thấp hơn mốc, xanh là cao hơn; độ đậm theo độ lớn. Không dùng đỏ và xanh lá: khó phân biệt với người mù màu và trùng màu trạng thái.</p>
   <div class="card" style="background:#fff;box-shadow:inset 0 0 0 .25mm var(--hair);padding:4mm;margin-top:3mm">
    <div style="font:500 10pt Lora;color:var(--blue);margin-bottom:2.4mm">Đất đai và chi phí thời gian giảm điểm so với 2024</div>{dsvg}
    <div class="small" style="font-size:6.4pt;margin-top:1.6mm">Thay đổi điểm chỉ số thành phần, 2025 so với 2024 · Nguồn: VCCI · {DEMO}</div></div></div></div>"""))

# --- choosing a chart
kinds = [('Thay đổi theo thời gian', 'Đường; cột nếu ít mốc', 'Điểm PCI qua các năm'), ('So sánh, xếp hạng', 'Cột ngang, sắp xếp theo giá trị', 'Xếp hạng 63 tỉnh, thành'),
         ('Cơ cấu, tỉ trọng', 'Cột chồng 100%; tròn khi không quá 4 phần', 'Cơ cấu doanh nghiệp theo quy mô'), ('Chênh lệch quanh một mốc', 'Cột phân kỳ', 'Thay đổi so với năm trước'),
         ('Phân bố', 'Cột tần suất, biểu đồ chấm', 'Phân bố điểm của doanh nghiệp'), ('Tương quan', 'Phân tán', 'Chi phí không chính thức và quy mô'),
         ('Theo địa bàn', 'Bản đồ tô màu, bảng nhiệt', 'Chỉ số theo tỉnh hoặc vùng'), ('Một con số quan trọng', 'Số liệu nổi bật, không cần biểu đồ', 'Tỉ lệ doanh nghiệp hài lòng')]
ktable = ''.join(f'<div style="display:grid;grid-template-columns:48mm 56mm 1fr;gap:4mm;padding:2.2mm 0;border-top:.25mm solid var(--hair);font:400 8.2pt/1.4 BVP"><b style="font-weight:600;color:var(--blue)">{a}</b><span>{b}</span><span class="small" style="font-size:7.6pt">{c}</span></div>' for a, b, c in kinds)
bad_axis = column_chart(list(zip(['2023', '2024', '2025'], [64.8, 66.0, 67.4])), [cat[0][1]] * 3, lo=64, hi=68, w=200, h=130)
bad_many = column_chart(list(zip(list('ABCDEFG'), [30, 26, 22, 19, 15, 12, 9])), ['#264896', '#FFCD00', '#CC713C', '#2E9E5B', '#C23B22', '#8FA6D6', '#7B4FA0'], w=200, h=130)
pie_slices, acc = '', 0
for v, c in zip([22, 18, 14, 12, 10, 9, 8, 7], ['#264896', '#8FA6D6', '#CC713C', '#5C6478', '#F2B18E', '#0B1A4F', '#A9C0EC', '#E09166']):
    a0, a1 = acc / 100 * 6.2832, (acc + v) / 100 * 6.2832; acc += v
    import math
    pie_slices += f'<path d="M100,65 L{100 + 50 * math.sin(a0):.1f},{65 - 50 * math.cos(a0):.1f} A50,50 0 {1 if v > 50 else 0} 1 {100 + 50 * math.sin(a1):.1f},{65 - 50 * math.cos(a1):.1f} Z" fill="{c}" stroke="#fff" stroke-width="1"/>'
bad_pie = f'<svg viewBox="0 0 200 130" style="width:100%;display:block">{pie_slices}</svg>'
bad = lambda svg, note: f'<div><div class="card x" style="background:#fff;box-shadow:inset 0 0 0 .25mm var(--hair);padding:3mm;height:40mm;display:flex;align-items:center">{svg}</div><div class="bad" style="margin-top:2mm">Sai</div><p class="small">{note}</p></div>'
P.append(page(8, f"""<div class="grid" style="grid-template-columns:1.3fr 1fr;gap:12mm">
 <div><h2 style="margin-bottom:3mm">Chọn <em>biểu đồ</em></h2>
  <div style="display:grid;grid-template-columns:48mm 56mm 1fr;gap:4mm;padding-bottom:1.6mm"><span class="cap">Muốn cho thấy</span><span class="cap">Dùng</span><span class="cap">Ví dụ</span></div>{ktable}
  <p class="small" style="margin-top:3mm">Bảng chọn biểu đồ dựa trên hướng dẫn của GOV.UK và Văn phòng Thống kê Quốc gia Anh (ONS), điều chỉnh cho báo cáo của VCCI.</p></div>
 <div><h2 style="margin-bottom:3mm">Những điều <em>không được làm</em></h2>
  <div class="grid" style="grid-template-columns:1fr 1fr;gap:5mm">
   {bad(bad_axis, 'Trục cột không bắt đầu từ 0: chênh lệch nhỏ bị phóng to. Cần thu hẹp trục thì dùng biểu đồ đường và ghi rõ.')}
   {bad(bad_many, 'Màu ngoài bảng, vàng làm màu chuỗi, mỗi cột một màu không mang nghĩa.')}
   {bad(bad_pie, 'Biểu đồ tròn quá nhiều phần: không so sánh được. Dùng cột ngang sắp xếp.')}
   <div style="padding-top:2mm"><h3>Không được</h3><ul class="rules no"><li>Hiệu ứng 3D, bóng đổ, chuyển màu</li><li>Hai trục tung trên một biểu đồ</li><li>Biểu đồ không ghi nguồn</li><li>Dùng màu trạng thái làm màu chuỗi</li></ul></div></div></div></div>"""))

# ================================================================ 10 APPLICATIONS
tpl = lambda f, w: f'<img class="shot" src="{IMG(f)}" style="width:{w}">'
P.append(opener(9, 'Ứng dụng', 'Template Word, PowerPoint và mẫu thiết kế giúp mọi đơn vị tạo ra ấn phẩm đúng chuẩn ngay từ đầu. Các file nằm trong thư mục 06_Templates.',
  f'''<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:7mm">
   <div>{tpl('tpl_letter-1.png', '100%')}<div style="font:500 11pt Lora;color:var(--blue);margin-top:3mm">Thư / Letterhead</div><p class="small">VCCI_Letterhead.dotx · thư, công văn, thư ngỏ</p></div>
   <div>{tpl('tpl_invite-1.png', '100%')}<div style="font:500 11pt Lora;color:var(--blue);margin-top:3mm">Thư mời</div><p class="small">VCCI_Invitation.dotx · thư mời sự kiện một trang</p></div>
   <div>{tpl('tpl_report-1.png', '100%')}<div style="font:500 11pt Lora;color:var(--blue);margin-top:3mm">Báo cáo</div><p class="small">VCCI_Report.dotx · bìa, mục lục, thân bài, bìa sau</p></div></div>'''))

P.append(page(9, f'''<h2>Báo cáo <em>từ template</em></h2>
 <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:6mm;margin-top:2mm">
  {''.join(f'<div>{tpl(f, "100%")}<p class="small" style="margin-top:2.4mm">{d}</p></div>' for f, d in [('tpl_report-2.png', 'Mục lục tự động từ Heading 1–3'), ('tpl_report-3.png', 'Mở chương: nhãn, tiêu đề, gạch vàng, đoạn dẫn, số liệu nổi bật'), ('tpl_report-4.png', 'Bảng chuẩn và biểu đồ theo màu thương hiệu'), ('tpl_report-6.png', 'Bìa sau: logo trên ô nền sáng, thông tin liên hệ')])}</div>
 <p class="small" style="margin-top:5mm">Dùng Styles có sẵn (Title, VCCI Label, Heading 1–3, VCCI Lead, Quote, VCCI Callout, Caption). Đổi hero icon trên bìa theo chủ đề báo cáo bằng lệnh <b>Change Picture</b>. Hướng dẫn đầy đủ: 06_Templates/README.md.</p>'''))

slides = [('ppt-01.png', '01 Bìa sáng', 'Họp, làm việc với đối tác'), ('ppt-02.png', '12 Bìa sự kiện', 'Sân khấu; logo trên ô nền sáng'),
          ('ppt-04.png', '13 Chuyển chương', 'Số chương, hero icon, hiệu ứng Fade'), ('ppt-05.png', '03 Tiêu đề và nội dung', 'Chữ 18 pt, tối đa 5 ý'),
          ('ppt-08.png', '14 Số liệu nổi bật', 'Chỉ con số đầu tiên màu vàng'), ('ppt-09.png', '07 Biểu đồ và bảng', 'Biểu đồ thật, một cột vàng làm điểm nhấn'),
          ('ppt-15.png', '06 Nội dung dày', 'Chữ 14 pt, cho bài gửi đọc'), ('ppt-17.png', '18 Kết thúc', 'Lời cảm ơn và thông tin liên hệ')]
P.append(page(9, f'''<h2>Trình chiếu <em>từ template</em></h2>
 <p style="width:250mm">VCCI_Presentation.potx: khổ 16:9, 18 layout (11 nền sáng, 7 nền xanh), font đã nhúng, mở ra với 17 slide mẫu có ghi chú cách dùng.</p>
 <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:5mm 6mm;margin-top:3mm">
  {''.join(f'<div>{tpl(f, "100%")}<div style="font:500 9.5pt Lora;color:var(--blue);margin-top:2mm">{n}</div><p class="small" style="margin:0">{d}</p></div>' for f, n, d in slides)}</div>
 <div class="grid" style="grid-template-columns:repeat(3,1fr);gap:10mm;margin-top:6mm">
  <div><h3>Nhịp sáng và xanh</h3><p class="small">Slide nội dung dùng nền sáng cho dễ đọc. Bìa, chuyển chương, số liệu nổi bật và trích dẫn dùng nền xanh để tạo nhịp.</p></div>
  <div><h3>Logo và chân trang</h3><p class="small">Logo ở bìa, slide kết thúc và góc slide nền sáng. Chân trang: Insert → Header &amp; Footer → Apply to All.</p></div>
  <div><h3>Tiết chế</h3><p class="small">Một điểm nhấn vàng mỗi slide. Hiệu ứng Fade chỉ dùng cho slide chuyển chương; không thêm hiệu ứng khác.</p></div></div>'''))

qv = [('qv_report.png', 'Báo cáo tư vấn', 'vcci-report · bìa, mục lục, chương, bìa sau; chú thích cuối trang'),
      ('qv_wp.png', 'Working paper', 'vcci-wp · số hiệu, tóm tắt song ngữ, mã JEL; trích dẫn APA'),
      ('qv_memo.png', 'Tờ trình', 'vcci-memo · Gửi, Từ, Về việc, chữ ký'),
      ('qv_charts.png', 'Báo cáo có biểu đồ', 'Biểu đồ ggplot2 chạy ngay trong tài liệu')]
code = [('Python · matplotlib', 'vcci_charts.py, vcci.mplstyle', ['import vcci_charts as vcci', 'vcci.use()', 'vcci.highlight(bars, -1)', 'vcci.source(fig, "Nguồn: …")']),
        ('R · ggplot2', 'theme_vcci.R', ['source("theme_vcci.R")', 'vcci_setup()', 'fill = vcci_highlight(year == 2025)', 'labs(caption = "Nguồn: …")']),
        ('Stata', 'scheme-vcci.scheme, vcci_graph.do', ['do vcci_graph.do', 'graph bar …, note("Nguồn: …")', 'graph export bieu-do.svg'])]
P.append(page(9, f'''<h2>Tài liệu và biểu đồ <em>từ mã</em></h2>
 <p style="width:250mm">Nhóm nghiên cứu soạn báo cáo, working paper và tờ trình bằng Quarto (Markdown). Một lệnh dựng ra bản PDF đúng bộ nhận diện và bản Word để đồng nghiệp sửa. Theme biểu đồ cho Python, R và Stata dùng chung màu, chữ và quy tắc của phần 08.</p>
 <div class="grid" style="grid-template-columns:1.75fr 1fr;gap:10mm;margin-top:3mm;align-items:start">
  <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:5mm">
   {''.join(f'<div>{tpl(f, "100%")}<div style="font:500 9.5pt Lora;color:var(--blue);margin-top:2.4mm">{n}</div><p class="small" style="margin:0">{d}</p></div>' for f, n, d in qv)}</div>
  <div>{''.join(f"""<div style="padding:2.6mm 0;border-top:.25mm solid var(--hair)"><div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font:600 8.4pt BVP;color:var(--blue)">{t}</b><span class="small" style="font-size:6.6pt">{f}</span></div>
    <div style="margin-top:1.6mm;padding:2mm 3mm;background:var(--tint);font:400 7.2pt/1.6 BVP;color:var(--ink)">{'<br>'.join(lines)}</div></div>""" for t, f, lines in code)}</div></div>
 <div class="grid" style="grid-template-columns:repeat(3,1fr);gap:10mm;margin-top:6mm">
  <div><h3>Bắt đầu</h3><p class="small">Cài extension bằng lệnh <b>quarto add</b>, chép một tài liệu mẫu, rồi chạy <b>quarto render</b>. Thông tin bìa, tác giả, số hiệu khai báo ở đầu tài liệu.</p></div>
  <div><h3>Biểu đồ</h3><p class="small">Chép file theme cạnh file mã. Màu chuỗi, lưới, chữ và dấu phẩy thập phân tự đúng; vàng chỉ nhấn một giá trị. Chú thích hình nêu thông điệp, nguồn ghi dưới biểu đồ.</p></div>
  <div><h3>Tệp</h3><p class="small">Extension, mẫu và hướng dẫn: thư mục <b>quarto-vcci</b>. Theme biểu đồ cho người không dùng Quarto: <b>06_Templates/Charts</b>.</p></div></div>'''))

P.append(page(9, f'''<h2>Kênh số và <em>sự kiện</em></h2>
 <div class="grid" style="grid-template-columns:1.55fr .75fr .95fr;gap:6mm;align-items:start">
  <div>{tpl('mock_website.jpg', '100%')}<p class="small" style="margin-top:2.4mm">Website: logo đầy đủ trên thanh điều hướng sáng, khối hero xanh có họa tiết vòng trống.</p>
   <div style="margin-top:5mm">{tpl('mock_social.jpg', '100%')}<p class="small" style="margin-top:2.4mm">Mạng xã hội: ba khuôn mẫu Quan điểm, Cột mốc, Chương trình. Logo luôn trên ô nền sáng khi đặt trên nền xanh.</p></div></div>
  <div>{tpl('mock_app.jpg', '100%')}<p class="small" style="margin-top:2.4mm">Ứng dụng hội viên: logo trên ô nền sáng trong thanh tiêu đề.</p></div>
  <div>{tpl('mock_poster.jpg', '100%')}<p class="small" style="margin-top:2.4mm">Poster sự kiện A2.</p>
   <div style="margin-top:4mm">{tpl('mock_badge.jpg', '100%')}<p class="small" style="margin-top:2.4mm">Thẻ đại biểu: đầu thẻ nền sáng, dải vàng ghi tên sự kiện.</p></div></div></div>'''))

assets = [('01_Logo', 'Logo chính, lockup, bản ô nền sáng: SVG, PNG, PDF; bản gốc .CDR'), ('02_Colour', 'Bảng màu, thang sắc độ, màu trạng thái, màu biểu đồ: Office theme, Adobe ASE, CSS, JSON'),
          ('03_Fonts', 'Lora, Be Vietnam Pro và giấy phép SIL OFL'), ('04_Graphics', 'Vòng trống, mặt trời 14 cánh, cung chữ C, trường chấm'),
          ('05_Icons', '48 icon nhỏ, 24 hero icon; quy cách ICON_SPEC.md'), ('06_Templates', 'Template Word (thư, báo cáo, thư mời), PowerPoint 16:9, theme biểu đồ Python, R, Stata'),
          ('07_Guidelines', 'Tài liệu này'), ('brand-tokens.json', 'Toàn bộ thông số dạng máy đọc được, cho lập trình viên')]
P.append(page(9, f'''<div class="grid" style="grid-template-columns:1.1fr 1fr;gap:12mm">
 <div><h2>Văn phòng phẩm và <em>quà tặng</em></h2>{tpl('mock_stationery.jpg', '100%')}<div class="grid" style="grid-template-columns:1fr 1fr;gap:5mm;margin-top:5mm"><div>{tpl('mock_giftbox.jpg', '100%')}</div><p class="small">Bao bì và quà tặng: hộp xanh, nhãn giấy sáng in logo đầy đủ. Không in logo chữ trắng hay chữ vàng ép kim lên bề mặt xanh.</p></div></div>
 <div><h2>Danh mục <em>tài sản</em></h2>{''.join(f'<div style="display:grid;grid-template-columns:40mm 1fr;gap:4mm;padding:2.6mm 0;border-top:.25mm solid var(--hair)"><b style="font:600 8.4pt BVP;color:var(--blue)">{a}</b><span class="small" style="font-size:8.2pt">{b}</span></div>' for a, b in assets)}
  <div style="margin-top:6mm;padding:4mm 5mm;background:var(--tint);border-left:.8mm solid var(--blue)" class="small">Cài font và bảng màu theo hướng dẫn trong <b>brand-assets/README.md</b>. Luôn lấy file từ bộ tài sản chính thức, không chụp màn hình hay sao chép logo từ website.</div></div></div>'''))

# ================================================================ BACK COVER
P.append(f'''<section class="page" style="background:linear-gradient(160deg,#2B4FA0,#1E3D86)">
 <svg viewBox="-300 -300 600 600" style="position:absolute;width:260mm;height:260mm;left:-60mm;top:-40mm">{BA.drum('#fff', BA.GOLD, .5, .14, .5)}</svg>
 <div style="position:absolute;right:20mm;bottom:22mm;width:150mm;height:62mm;background:var(--paper);border-radius:1.2mm;padding:9mm 10mm">
  <img src="{LOGO}" style="width:66mm">
  <div style="margin-top:7mm;font:600 9pt BVP;color:var(--blue)">Liên đoàn Thương mại và Công nghiệp Việt Nam</div>
  <div class="small" style="font-size:8pt">Số 9 Đào Duy Anh, Đống Đa, Hà Nội · T +84 24 3574 2022 · vcci.com.vn</div>
  <div class="small" style="font-size:7pt;margin-top:3mm">Hướng dẫn Nhận diện Thương hiệu · Phiên bản 1.1 · Tháng 10/2026</div></div>
</section>''')

P[1] = re.sub(r'@@PG(\d)@@', lambda m: f'{START[int(m.group(1))]:02d}', P[1])
html = f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>VCCI Hướng dẫn Nhận diện Thương hiệu</title><style>{CSS}</style></head><body style="counter-reset:pg">{"".join(P)}</body></html>'
hp = os.path.join(G, 'guide.html'); open(hp, 'w', encoding='utf-8').write(html)
pdf = os.path.join(OUT_DIR, 'VCCI_Huong-dan-Nhan-dien-Thuong-hieu_v1.1.pdf')
BA.env.run_edge(['--no-pdf-header-footer', '--virtual-time-budget=8000',
                f'--print-to-pdf={pdf}', 'file:///' + hp.replace(os.sep, '/')])
print('pages', len(P), '->', pdf, os.path.getsize(pdf) // 1024, 'KB')
