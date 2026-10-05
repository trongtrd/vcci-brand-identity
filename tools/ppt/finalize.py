"""Post-process the pptxgenjs output into the VCCI PowerPoint template.

1. VCCI theme colours and fonts      2. drop the empty DEFAULT layout
3. real footer placeholders (Insert > Header & Footer) on layouts and sample slides
4. Fade transition on the section-divider layout and its slides
5. PowerPoint saves the result as .potx with embedded fonts, and exports a PDF preview
Run from the repository root:  python tools/ppt/finalize.py
"""
import json, os, re, subprocess, zipfile

ROOT = os.getcwd()
P = os.path.join(ROOT, 'build', 'ppt')
SRC = os.path.join(P, 'out', 'VCCI_Presentation.pptx')
STAGE = os.path.join(P, 'out', 'VCCI_Presentation_processed.pptx')
DEST_DIR = os.path.join(ROOT, 'brand-assets', '06_Templates', 'PowerPoint')
os.makedirs(os.path.join(DEST_DIR, 'Previews'), exist_ok=True)
POTX = os.path.join(DEST_DIR, 'VCCI_Presentation.potx')
PDF = os.path.join(DEST_DIR, 'Previews', 'VCCI_Presentation.pdf')

CLR = '''<a:clrScheme name="VCCI"><a:dk1><a:srgbClr val="161A26"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
<a:dk2><a:srgbClr val="0B1A4F"/></a:dk2><a:lt2><a:srgbClr val="F4F0E6"/></a:lt2><a:accent1><a:srgbClr val="264896"/></a:accent1>
<a:accent2><a:srgbClr val="FFCD00"/></a:accent2><a:accent3><a:srgbClr val="CC713C"/></a:accent3><a:accent4><a:srgbClr val="5C6478"/></a:accent4>
<a:accent5><a:srgbClr val="8FA6D6"/></a:accent5><a:accent6><a:srgbClr val="9C570C"/></a:accent6><a:hlink><a:srgbClr val="264896"/></a:hlink>
<a:folHlink><a:srgbClr val="9C570C"/></a:folHlink></a:clrScheme>'''.replace('\n', '')
NO_FOOTER = {'01 Bìa sáng', '12 Bìa sự kiện', '17 Ảnh toàn khung', '18 Kết thúc', 'DEFAULT'}
BLUE = {'12 Bìa sự kiện', '13 Chuyển chương', '14 Số liệu nổi bật', '15 Tuyên bố lớn', '16 Trích dẫn', '17 Ảnh toàn khung', '18 Kết thúc'}
SECTION = '13 Chuyển chương'
FOOTER_TEXT = 'Diễn đàn Doanh nghiệp Việt Nam 2026'
EMU = 914400
FTR_IDX = '4001'
TRANSITION = '<p:transition spd="med"><p:fade/></p:transition>'

def footer_sp(sid, color, text=None):
    x, y, w, h = int(0.8 * EMU), int(6.93 * EMU), int(8.0 * EMU), int(0.3 * EMU)
    body = (f'<a:p><a:r><a:rPr lang="vi-VN" dirty="0"/><a:t>{text}</a:t></a:r></a:p>' if text else '<a:p><a:endParaRPr lang="vi-VN"/></a:p>')
    sppr = '<p:spPr/>' if text else f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm></p:spPr>'
    lst = '' if text else (f'<a:lstStyle><a:lvl1pPr algn="l"><a:defRPr sz="1000"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
                           f'<a:latin typeface="Be Vietnam Pro"/><a:cs typeface="Be Vietnam Pro"/></a:defRPr></a:lvl1pPr></a:lstStyle>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Footer Placeholder {sid}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr><p:ph type="ftr" sz="quarter" idx="{FTR_IDX}"/></p:nvPr></p:nvSpPr>{sppr}'
            f'<p:txBody><a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/>{lst}{body}</p:txBody></p:sp>')

def add_to_tree(xml, sp):
    return xml.replace('</p:spTree>', sp + '</p:spTree>', 1)

def process():
    z = zipfile.ZipFile(SRC); f = {n: z.read(n) for n in z.namelist()}; z.close()
    s = lambda n: f[n].decode('utf-8')

    # 1. theme
    th = s('ppt/theme/theme1.xml')
    th = re.sub(r'<a:clrScheme name="[^"]*">.*?</a:clrScheme>', CLR, th, flags=re.S)
    th = re.sub(r'(<a:theme [^>]*name=")[^"]*"', r'\1VCCI"', th, count=1)
    th = re.sub(r'(<a:minorFont><a:latin typeface=")[^"]*"', r'\1Be Vietnam Pro"', th, count=1)
    th = re.sub(r'(<a:majorFont><a:latin typeface=")[^"]*"', r'\1Lora Medium"', th, count=1)
    th = re.sub(r'<a:fontScheme name="[^"]*"', '<a:fontScheme name="VCCI"', th, count=1)
    f['ppt/theme/theme1.xml'] = th.encode('utf-8')

    # layout names: pptxgenjs builds media file names from master titles, so masters use ASCII codes (L01…)
    # and get their Vietnamese display names here
    vn = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'layout_names.json'), encoding='utf-8'))
    names = {}
    for n in [n for n in f if re.match(r'ppt/slideLayouts/slideLayout\d+\.xml$', n)]:
        code = re.search(r'<p:cSld name="([^"]*)"', s(n)).group(1)
        names[n] = vn.get(code, code)
        f[n] = s(n).replace(f'<p:cSld name="{code}"', f'<p:cSld name="{names[n]}"', 1).encode('utf-8')

    # 2. drop DEFAULT layout
    for n, nm in list(names.items()):
        if nm != 'DEFAULT': continue
        base = os.path.basename(n)
        mrels = s('ppt/slideMasters/_rels/slideMaster1.xml.rels')
        rid = re.search(r'Id="(rId\d+)"[^>]*Target="\.\./slideLayouts/' + re.escape(base) + '"', mrels).group(1)
        f['ppt/slideMasters/_rels/slideMaster1.xml.rels'] = re.sub(r'<Relationship Id="' + rid + r'"[^>]*/>', '', mrels).encode('utf-8')
        f['ppt/slideMasters/slideMaster1.xml'] = re.sub(r'<p:sldLayoutId id="\d+" r:id="' + rid + r'"/>', '', s('ppt/slideMasters/slideMaster1.xml')).encode('utf-8')
        ct = s('[Content_Types].xml')
        f['[Content_Types].xml'] = re.sub(r'<Override PartName="/ppt/slideLayouts/' + re.escape(base) + r'"[^>]*/>', '', ct).encode('utf-8')
        del f[n]; f.pop(f'ppt/slideLayouts/_rels/{base}.rels', None); del names[n]

    # 3a. footer placeholder on the master and on layouts; 4a. transition on the section layout
    f['ppt/slideMasters/slideMaster1.xml'] = add_to_tree(s('ppt/slideMasters/slideMaster1.xml'), footer_sp(9001, '5C6478')).encode('utf-8')
    for n, nm in names.items():
        x = s(n)
        if nm not in NO_FOOTER: x = add_to_tree(x, footer_sp(9001, 'B9C6E4' if nm in BLUE else '5C6478'))
        if nm == SECTION: x = x.replace('</p:clrMapOvr>', '</p:clrMapOvr>' + TRANSITION, 1)
        f[n] = x.encode('utf-8')

    # 3b/4b. sample slides
    for n in [n for n in f if re.match(r'ppt/slides/slide\d+\.xml$', n)]:
        rel = s(f'ppt/slides/_rels/{os.path.basename(n)}.rels')
        lay = 'ppt/slideLayouts/' + re.search(r'slideLayouts/(slideLayout\d+\.xml)', rel).group(1)
        nm = names[lay]; x = s(n)
        if nm not in NO_FOOTER: x = add_to_tree(x, footer_sp(9001, None, FOOTER_TEXT))
        if nm == SECTION: x = x.replace('</p:clrMapOvr>', '</p:clrMapOvr>' + TRANSITION, 1)
        f[n] = x.encode('utf-8')

    with zipfile.ZipFile(STAGE, 'w', zipfile.ZIP_DEFLATED) as o:
        for n in ['[Content_Types].xml'] + [n for n in f if n != '[Content_Types].xml']: o.writestr(n, f[n])

PS = r'''
param([string]$In, [string]$Potx, [string]$Pdf)
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
try {
  $p = $app.Presentations.Open($In, -1, 0, 0)
  $p.SaveAs($Potx, 26, -1)          # ppSaveAsOpenXMLTemplate, EmbedTrueTypeFonts
  $p.Close()
  $p = $app.Presentations.Open($Potx, -1, 0, 0)
  $p.SaveAs($Pdf, 32)               # ppSaveAsPDF
  $p.Close()
} finally { $app.Quit() }
'''

def powerpoint():
    out = subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Process POWERPNT -ErrorAction SilentlyContinue | '
                          'Where-Object { $_.MainWindowTitle } | ForEach-Object { $_.MainWindowTitle }'], capture_output=True, text=True).stdout.strip()
    if out: raise SystemExit('Close PowerPoint before running this script (open: ' + out + ')')
    ps1 = os.path.join(P, '_ppt.ps1'); open(ps1, 'w', encoding='utf-8-sig').write(PS)
    for p in (POTX, PDF):
        if os.path.exists(p): os.remove(p)
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps1, '-In', STAGE, '-Potx', POTX, '-Pdf', PDF], check=True)
    print('potx', os.path.getsize(POTX) // 1024, 'KB; pdf', os.path.getsize(PDF) // 1024, 'KB')

if __name__ == '__main__':
    process(); powerpoint()
