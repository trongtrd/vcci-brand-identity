from pathlib import Path
import json, math, sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]; WORK=ROOT/'tools'/'icons'; OUT=ROOT/'build'/'icons'/'review'/'05_Icons'
FINAL='--final' in sys.argv
if FINAL: OUT=ROOT/'build'/'icons'/'final'/'05_Icons'
items=json.loads((WORK/'catalog.json').read_text(encoding='utf8'))
PAPER='#FBF9F4'; BLUE='#264896'; NAVY='#0B1A4F'; GOLD='#FFCD00'
def font(size,bold=False):return ImageFont.truetype(str(ROOT/'brand-assets'/'03_Fonts'/'BeVietnamPro'/('BeVietnamPro-SemiBold.ttf' if bold else 'BeVietnamPro-Regular.ttf')),size)
def lines(text,f,width):
 words=text.split(); result=[]; current=''
 for w in words:
  test=(current+' '+w).strip()
  if f.getlength(test)>width and current:result.append(current);current=w
  else:current=test
 if current:result.append(current)
 return result
def center(draw,text,x,y,width,f,color):
 for line in lines(text,f,width):
  draw.text((x+(width-f.getlength(line))/2,y),line,font=f,fill=color);y+=int(f.size*1.4)
 return y
def icon(item,variant,size):
 file=Path(item['paths'][variant]);alpha=WORK/'qa'/'alpha'/item['tier']/(variant+'_'+item['slug']+'.png')
 return Image.open(alpha).convert('RGBA').resize((size,size),Image.Resampling.LANCZOS)
for tier in ['UI','Hero']:
 subset=[i for i in items if i['tier']==tier];cols=4 if tier=='Hero' else 6; cellw=320 if tier=='Hero' else 210;cellh=270 if tier=='Hero' else 174
 panelw=cols*cellw; rows=math.ceil(len(subset)/cols);w=panelw*2;h=rows*cellh+195
 sheet=Image.new('RGB',(w,h),PAPER);d=ImageDraw.Draw(sheet);dark=NAVY if tier=='Hero' else BLUE
 d.rectangle((panelw,0,w,h),fill=dark)
 for side,color in [(0,BLUE),(1,'#FFFFFF')]:
  x=side*panelw;d.text((x+32,25),f'VCCI / {tier.upper()} ICON SYSTEM',font=font(26,True),fill=color)
  d.text((x+32,70),('PAPER / BLUE + GOLD' if tier=='Hero' else 'PAPER / BLUE') if side==0 else ('DEEP NAVY / GOLD' if tier=='Hero' else 'VCCI BLUE / GOLD'),font=font(14),fill=color)
  d.text((x+32,h-40),'VERSION 1.0 / DIRECTION A / OWNER APPROVED' if FINAL else 'REVIEW 01 / DIRECTION A / OWNER SIGN-OFF PENDING',font=font(13),fill=color)
 for idx,item in enumerate(subset):
  for side in [0,1]:
   x=side*panelw+(idx%cols)*cellw;y=125+(idx//cols)*cellh;size=120 if tier=='Hero' else 64
   variant=('Blue-Gold' if tier=='Hero' else 'Blue') if side==0 else ('Gold-on-dark' if tier=='Hero' else 'Gold')
   im=icon(item,variant,size);sheet.paste(im,(x+(cellw-size)//2,y),im)
   color=BLUE if side==0 else '#FFFFFF'
   yy=center(d,(item.get('nn','')+' '+item['vn']).strip(),x+15,y+size+15,cellw-30,font(17 if tier=='Hero' else 14,True),color)
   center(d,item['en'],x+15,yy+4,cellw-30,font(14 if tier=='Hero' else 12),color)
 sheet.save(OUT/'Sheets'/f'VCCI_{tier}_ContactSheet.png')
 # Review pages preserve actual 24, 48 and 128 pixel render sizes.
 for start in range(0,len(subset),6):
  group=subset[start:start+6];qa=Image.new('RGB',(1000,1080),PAPER);d=ImageDraw.Draw(qa)
  d.text((20,12),f'{tier} / {start+1:02d}–{start+len(group):02d} / 24 · 48 · 128 px',font=font(21,True),fill=BLUE)
  d.text((290,52),'PAPER',font=font(14),fill=BLUE);d.text((650,52),'VCCI BLUE',font=font(14),fill=BLUE)
  for row,item in enumerate(group):
   y=85+row*163;d.text((12,y+10),item.get('nn',str(start+row+1)),font=font(16,True),fill=BLUE)
   center(d,item['en'],10,y+42,215,font(15),BLUE)
   for side,bg in enumerate(['Paper','Blue']):
    x=245+side*365;d.rectangle((x,y,x+350,y+154),fill=PAPER if side==0 else BLUE)
    variant=('Blue-Gold' if tier=='Hero' else 'Blue') if side==0 else ('Gold-on-dark' if tier=='Hero' else 'Gold')
    for size,offset in [(24,16),(48,78),(128,177)]:
     im=Image.open(WORK/'qa'/'renders'/tier/variant/bg/f"{item['slug']}_{size}.png")
     qa.paste(im,(x+offset,y+(154-size)//2))
  qa.save(WORK/'qa'/f'{tier}_{start//6+1:02d}.png')
 # Compact preview, still generated from actual vectors.
 sheet.thumbnail((1600,1600),Image.Resampling.LANCZOS);sheet.save(WORK/'qa'/f'{tier}_overview.png')
print('Contact sheets and 12 size-check pages created.')
