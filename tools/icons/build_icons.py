from pathlib import Path
import json, re, math, shutil, requests, concurrent.futures
import xml.etree.ElementTree as ET
from svgpathtools import parse_path
from heroes import HEROES

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'tools'/'icons'
OUT=ROOT/'build'/'icons'/'review'/'05_Icons'
UI_NAMES='home menu close search filter settings arrow-right arrow-left chevron-down external-link download upload share print calendar clock map-pin phone mail globe user users user-plus lock info alert-triangle check check-circle file file-text file-check folder newspaper presentation video mic image bar-chart line-chart pie-chart briefcase building landmark factory ship handshake scale award'.split()
VN=['Trang chủ','Trình đơn','Đóng','Tìm kiếm','Bộ lọc','Cài đặt','Sang phải','Sang trái','Mở xuống','Liên kết ngoài','Tải xuống','Tải lên','Chia sẻ','In','Lịch','Thời gian','Địa điểm','Điện thoại','Thư điện tử','Toàn cầu','Người dùng','Nhóm người dùng','Thêm người dùng','Khóa','Thông tin','Cảnh báo','Xác nhận','Đã xác nhận','Tệp','Văn bản','Tệp đã duyệt','Thư mục','Tin tức','Thuyết trình','Video','Micro','Hình ảnh','Biểu đồ cột','Biểu đồ đường','Biểu đồ tròn','Công việc','Tòa nhà','Thiết chế','Nhà máy','Tàu hàng','Bắt tay','Cán cân','Giải thưởng']
ALIASES={'home':'house','close':'x','filter':'list-filter','print':'printer','share':'share-2','alert-triangle':'triangle-alert','check-circle':'circle-check','bar-chart':'chart-no-axes-column','line-chart':'chart-line','pie-chart':'chart-pie'}
SOURCE=WORK/'lucide'; SOURCE.mkdir(exist_ok=True)
manifest_file=SOURCE/'source.json'
if manifest_file.exists(): source=json.loads(manifest_file.read_text())
else:
 response=requests.get('https://api.github.com/repos/lucide-icons/lucide/commits/main',timeout=60); response.raise_for_status()
 source={'repository':'https://github.com/lucide-icons/lucide','commit':response.json()['sha']}
 manifest_file.write_text(json.dumps(source,indent=2))
base=f"https://raw.githubusercontent.com/lucide-icons/lucide/{source['commit']}/"
def fetch(name):
 target=SOURCE/name
 if not target.exists():
  response=requests.get(base+('LICENSE' if name=='LICENSE' else 'icons/'+name),timeout=60); response.raise_for_status(); target.write_bytes(response.content)
 return name
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: list(pool.map(fetch,['LICENSE']+[ALIASES.get(s,s)+'.svg' for s in UI_NAMES]))

def number(x): return str(round(float(x),2)).removesuffix('.0')
def clean(s): return re.sub(r'-?\d+(?:\.\d+)?(?:e[+-]?\d+)?',lambda m:number(m.group()),s,flags=re.I)
def bounds(el):
 tag=el.tag.split('}')[-1]; a=el.attrib
 if tag=='path':
  b=parse_path(a['d']).bbox();return b
 if tag=='circle':
  x,y,r=map(float,[a['cx'],a['cy'],a['r']]); return x-r,x+r,y-r,y+r
 if tag=='ellipse':
  x,y,rx,ry=map(float,[a['cx'],a['cy'],a['rx'],a['ry']]);return x-rx,x+rx,y-ry,y+ry
 if tag=='rect':
  x,y,w,h=map(float,[a.get('x',0),a.get('y',0),a['width'],a['height']]);return x,x+w,y,y+h
 if tag=='line':
  x1,y1,x2,y2=map(float,[a['x1'],a['y1'],a['x2'],a['y2']]);return min(x1,x2),max(x1,x2),min(y1,y2),max(y1,y2)
 if tag in ('polyline','polygon'):
  v=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',a['points'])];return min(v[::2]),max(v[::2]),min(v[1::2]),max(v[1::2])
 raise ValueError(tag)
def transform(el,s,dx,dy):
 tag=el.tag.split('}')[-1]; a=dict(el.attrib)
 if tag=='path': a['d']=clean(parse_path(a['d']).scaled(s).translated(complex(dx,dy)).d())
 elif tag in ('polygon','polyline'):
  vals=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',a['points'])];a['points']=' '.join(number(v*s+(dx if i%2==0 else dy)) for i,v in enumerate(vals))
 else:
  for k in ('x','x1','x2','cx'):
   if k in a:a[k]=number(float(a[k])*s+dx)
  for k in ('y','y1','y2','cy'):
   if k in a:a[k]=number(float(a[k])*s+dy)
  for k in ('width','height','r','rx','ry'):
   if k in a:a[k]=number(float(a[k])*s)
 return '<'+tag+' '+ ' '.join(f'{k}="{v}"' for k,v in a.items())+'/>'
def fit(body,size,padding,stroke):
 children=list(ET.fromstring('<svg>'+body+'</svg>')); bb=[bounds(x) for x in children]
 lo,hi,top,bottom=min(b[0] for b in bb),max(b[1] for b in bb),min(b[2] for b in bb),max(b[3] for b in bb)
 # Preserve optical proportions; only reduce shapes crossing the live-area boundary.
 extent=max(size/2-lo,hi-size/2,size/2-top,bottom-size/2)
 s=min(1,(size/2-padding-stroke/2)/extent)
 return ''.join(transform(el,s,size/2*(1-s),size/2*(1-s)) for el in children),s
def svg(body,size,stroke,color):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>\n'
def save(path,text): path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf8')
items=[]; adjustments=[]
for slug,vn in zip(UI_NAMES,VN):
 upstream=ALIASES.get(slug,slug); tree=ET.fromstring((SOURCE/(upstream+'.svg')).read_text())
 body=''.join(ET.tostring(el,encoding='unicode').replace('ns0:','').replace(' xmlns:ns0="http://www.w3.org/2000/svg"','') for el in tree)
 body,s=fit(body,24,2,1.6)
 paths={}
 for variant,color in [('currentColor','currentColor'),('Blue','#264896'),('Gold','#FFCD00'),('White','#FFFFFF')]:
  path=OUT/'UI'/'SVG'/variant/f'VCCI_UI_{slug}.svg';save(path,svg(body,24,1.6,color));paths[variant]=path.relative_to(ROOT).as_posix()
 items.append({'tier':'UI','slug':slug,'vn':vn,'en':slug.replace('-',' ').title(),'paths':paths})
 adjustments.append({'slug':slug,'upstream':upstream,'scale':round(s,6)})
for nn,slug,vn,en,body,accent in HEROES:
 body,s=fit(body,64,4,2)
 paths={}
 for variant,color,acc in [('Blue-Gold','#264896',accent),('Blue','#264896',''),('Gold-on-dark','#FFCD00',''),('White','#FFFFFF','')]:
  path=OUT/'Hero'/'SVG'/variant/f'VCCI_Hero_{nn}_{slug}.svg';save(path,svg(acc+body,64,2,color));paths[variant]=path.relative_to(ROOT).as_posix()
 items.append({'tier':'Hero','nn':nn,'slug':slug,'vn':vn,'en':en,'paths':paths})
(WORK/'catalog.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf8')
(WORK/'ui-adaptations.json').write_text(json.dumps(adjustments,indent=2))
(OUT/'Sheets').mkdir(exist_ok=True);shutil.copy2(ROOT/'docs'/'handoff-icons'/'concepts'/'VCCI_Hero_Concept_A.png',OUT/'Sheets'/'VCCI_Hero_Concepts.png')
license_text=(SOURCE/'LICENSE').read_text()
save(OUT/'LICENSES.md','# Licenses and provenance\n\n## UI icons\n\nBased exclusively on Lucide. Source: '+source['repository']+'\n\nPinned commit: `'+source['commit']+'`. Retrieved 2026-10-05. All 48 icons are modified: stroke changed to 1.6, presentation attributes normalized, colors exported, and geometry fitted within the live area where needed. No icons were copied from another organization’s brand kit.\n\n| VCCI slug | Lucide source | Geometric scale about (12,12) |\n|---|---|---|\n'+''.join(f"| {a['slug']} | {a['upstream']} | {a['scale']} |\n" for a in adjustments)+'\n## Upstream notices (preserved verbatim)\n\n```text\n'+license_text+'\n```\n\n## Hero icons\n\nThe 24 hero icons are original hand-authored SVG compositions created for this VCCI project. GPT Image was used only for raster concept exploration. No raster auto-tracing, embedded raster imagery, third-party brand icons, logo or drum medallion was used. Hero drawings are not derived from Lucide.\n')
save(OUT/'ICON_SPEC.md','''# VCCI Icon System v1 — Review candidate

Status: Direction A approved; icon set awaiting owner review. Not final sign-off.

## Scope and construction

48 UI icons and 24 original hero icons. UI uses the supplied 24 px grid, a 20 × 20 live area, 2 px padding and 1.6 px strokes. Hero uses the supplied 64 px grid, a 56 × 56 live area, 4 px padding and 2 px strokes. Padding includes the painted stroke. All caps and joins are round. Geometry is authored or adapted as explicit SVG paths and basic shapes; no raster tracing. Presentation attributes only; no transforms, text, fonts, CSS or embedded images in icon SVGs. Coordinates use at most two decimal places.

## Color and variants

- UI currentColor masters inherit CSS text color when inlined; standalone consumers should use the explicit color variants. Blue #264896 is for Paper #FBF9F4/light backgrounds. Gold #FFCD00 and White #FFFFFF are for VCCI Blue #264896 or Deep Navy #0B1A4F.
- Hero Blue-Gold: blue line with one flat gold shape behind the linework. Each accent occupies at most 25% of the 56 × 56 live area (a stricter denominator than the full canvas).
- Hero Blue: blue line only. Gold-on-dark: gold line only, no accent. White: white line only, no accent. No Blue Tint accent in v1, per owner agreement.
- No gradients, shadows, opacity effects or additional stroke weights.
- Accent is optional in use: use the line-only variant in dense compositions to avoid multiple competing gold gestures.

## Use and accessibility

UI is designed for 24 px display; hero for 48 px and larger. Hero 24 px is a stress check and is not the recommended use size. Scale uniformly without non-scaling-stroke. Use Blue or Blue-Gold on Paper and Gold or White on dark backgrounds. Do not use Gold or White on Paper, or Blue on VCCI Blue.

Hero icons require a visible label on first use and in navigation unless an adjacent title already conveys the topic. Supply accessible names in the host application; hide decorative duplicates from assistive technology. Do not rely on an icon alone to convey unfamiliar policy concepts or status.

## Meaning boundaries

Local Economic Governance means provincial economic administration and responsiveness to business, not a national/state institution. Green Transition means enterprise environmental transition, not the full ESG agenda. Legislative Input means consultation and contribution to lawmaking, not arbitration. Administrative Reform means reducing procedural complexity. Business Environment Reform refers to enabling business access and removing obstacles. Private Sector Development represents independent businesses and is not a startup-only category.

## Do and do not

Keep proportions, approved colors, clear space and stroke rules. Use labels to distinguish related abstract concepts. Never insert the VCCI logo, drum medallion, flags, state/national emblems or mourning imagery. Never replace geometry with traced image-generation output. Never enclose all icons in a new badge or add ornamental rays. Gold is a controlled accent, not a background flood.

## Exports

UI transparent PNG: 48 and 96 px, Blue/Gold/White. Hero transparent PNG: 256 and 512 px, Blue-Gold/Blue/Gold-on-dark/White. Contact sheets are for review, not icon extraction. Retain SVGs as masters. The approved raster exploration is Sheets/VCCI_Hero_Concepts.png.

## Verification

All icons and explicit color variants are rendered at 24, 48 and 128 px on Paper and VCCI Blue for inspection. Appropriate light/dark pairings are separately assembled into QA sheets. Hero contact sheet additionally uses Deep Navy. Machine checks cover XML validity, allowed elements, stroke consistency, painted live-area bounds, accent count/area, file size, export dimensions and transparent PNG alpha. QA evidence is kept outside the delivery folder.
''')
save(OUT/'HANDBACK_TO_CLAUDE.md','# Handback to Claude — Review candidate\n\n## Status\n\nThe owner approved Direction A (Geometric Clarity). The vector set awaits review and final sign-off; no final ZIP has been issued.\n\n## Approved direction\n\nA restrained, frontal geometric line system with spacious compositions and one small gold accent behind blue linework. The approved raster sheet is `Sheets/VCCI_Hero_Concepts.png`. Final geometry is constructed manually rather than tracing the raster; ambiguous concepts are clarified for the policy and enterprise priorities.\n\n## Approved deviations\n\nHero scope increased from 20 to 24, with 12 priority themes first. Numbering and slugs follow the revised catalog below. Startup is no longer a standalone v1 icon; law reform, policy dialogue and sustainability are refined into more specific themes. UI remains 48. Gold-on-dark has no accent. First-use labels are required unless supplied by an adjacent title. Primary use is Word, PowerPoint, reports and events, with common UI uses supported.\n\n## Catalog\n\n| Tier / ID | Slug | Vietnamese | English |\n|---|---|---|---|\n'+''.join(f"| {i['tier']} {i.get('nn','')} | {i['slug']} | {i['vn']} | {i['en']} |\n" for i in items)+'''\n## Suggested template pairings

- Legislative submissions and consultation papers: 01 Legislative Input.
- Provincial economic governance / PCI reports: 02 Local Economic Governance with 21 Research and Surveys.
- Business environment recommendations: 03 Business Environment Reform.
- Procedure simplification and service guidance: 04 Administrative Reform.
- FTA and international cooperation materials: 05 International Integration.
- Public-private consultation agendas: 06 Public-Private Dialogue.
- C/O service guidance: 07 Certificate of Origin.
- SME support programs: 08 SME and 24 Business Advisory.
- Private sector strategy and productivity reports: 09 and 10 respectively.
- Enterprise green/digital transition programs: 11 and 12 respectively.
- Membership materials: 13; fairs: 15; training decks: 18; event agendas: 20.

## Review points and limitations

Owner review is still required, particularly for the abstract meanings of 02, 03 and 04 and the distinction between 09 and 10. Labels remain necessary. Hero 24 px is a stress-test size; 48 px is the minimum recommended display. The concept sheet is a raster reference and not a source of production geometry. Final sign-off and final ZIP packaging remain pending.
''')
print(json.dumps({'icons':len(items),'ui':len(UI_NAMES),'hero':len(HEROES),'source':source,'output':str(OUT)}))
