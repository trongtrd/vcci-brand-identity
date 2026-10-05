from pathlib import Path
import json, math, xml.etree.ElementTree as ET
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];WORK=ROOT/'tools'/'icons';OUT=ROOT/'build'/'icons'/'review'/'05_Icons'
items=json.loads((WORK/'catalog.json').read_text(encoding='utf8'));errors=[];stats={'icons':len(items),'svg':0,'png':0,'max_svg_bytes':0,'max_accent_area_percent':0}
for item in items:
 size=24 if item['tier']=='UI' else 64;pad=2 if size==24 else 4;weight='1.6' if size==24 else '2'
 for variant,file in item['paths'].items():
  f=Path(file);root=ET.parse(f).getroot();stats['svg']+=1;stats['max_svg_bytes']=max(stats['max_svg_bytes'],f.stat().st_size)
  def fail(msg):errors.append(str(f.relative_to(OUT))+': '+msg)
  if root.attrib.get('viewBox')!=f'0 0 {size} {size}':fail('viewBox')
  if root.attrib.get('stroke-width')!=weight:fail('stroke width')
  if root.attrib.get('stroke-linecap')!='round' or root.attrib.get('stroke-linejoin')!='round':fail('caps/joins')
  accents=[]
  for el in root.iter():
   tag=el.tag.split('}')[-1]
   if tag not in ['svg','path','circle','rect','line','polyline','polygon','ellipse']:fail('element '+tag)
   if any(k in el.attrib for k in ['transform','style','class']):fail('forbidden attribute')
   if el is not root and 'stroke-width' in el.attrib:fail('child stroke override')
   if el.attrib.get('fill','none')!='none':accents.append(el)
  if item['tier']=='UI' and accents:fail('UI fill')
  if len(accents)>1:fail('multiple accent shapes')
  for a in accents:
   if a.attrib['fill'] not in ['#FFCD00','#CC713C']:fail('accent color')
   if a.tag.endswith('circle'):area=math.pi*float(a.attrib['r'])**2
   elif a.tag.endswith('rect'):area=float(a.attrib['width'])*float(a.attrib['height'])
   else:fail('unmeasured accent');continue
   pc=100*area/(size-2*pad)**2;stats['max_accent_area_percent']=max(stats['max_accent_area_percent'],pc)
   if pc>25:fail('accent area')
  if f.stat().st_size>=4096:fail('over 4KB')
  if variant=='currentColor':continue
  alpha=Image.open(WORK/'qa'/'alpha'/item['tier']/(variant+'_'+item['slug']+'.png')).getchannel('A')
  # Ignore antialias fringes below 50% coverage; allow 0.1-unit rounding tolerance.
  box=alpha.point(lambda v:255 if v>=128 else 0).getbbox();scale=alpha.width/size
  if not box:fail('empty render')
  elif min(box[0]/scale,box[1]/scale,size-box[2]/scale,size-box[3]/scale)<pad-.1:fail('painted live-area bounds '+str(box))
  for px in ([48,96] if size==24 else [256,512]):
   dest=Path(str(f).replace('\\SVG\\','\\PNG\\').replace('.svg',f'_{px}px.png'));im=Image.open(dest);stats['png']+=1
   if im.size!=(px,px) or im.mode!='RGBA':fail('PNG dimensions/alpha')
   elif im.getchannel('A').getextrema()!=(0,255):fail('PNG transparency range')
stats['max_accent_area_percent']=round(stats['max_accent_area_percent'],2)
stats['errors']=errors
(WORK/'qa'/'validation.json').write_text(json.dumps(stats,indent=2),encoding='utf8')
print(json.dumps(stats,indent=2));raise SystemExit(bool(errors))
