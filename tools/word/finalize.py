"""Turn the generated .docx files into branded .dotx templates with embedded fonts, then export PDF previews.

Pipeline per template:  docx-js output -> Word (refresh TOC, re-save) -> embed obfuscated fonts + template content type
-> brand-assets/06_Templates/Word/*.dotx -> Word PDF export -> PNG previews (build/word/preview).
Run from the repository root:  python tools/word/finalize.py
"""
import os, re, shutil, subprocess, sys, uuid, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import table_styles

ROOT = os.getcwd()
W = os.path.join(ROOT, 'build', 'word')
SRC, STAGE, PREV = os.path.join(W, 'out'), os.path.join(W, 'stage'), os.path.join(W, 'preview')
DEST = os.path.join(ROOT, 'brand-assets', '06_Templates', 'Word')
FONTDIR = os.path.join(ROOT, 'brand-assets', '03_Fonts')
from env import PDFTOPPM
for d in (STAGE, PREV, DEST): os.makedirs(d, exist_ok=True)

EMBED = {  # family name (nameID 1) -> {slot: file}
    'Lora':                    {'Regular': 'Lora/Lora-Regular.ttf', 'Bold': 'Lora/Lora-Bold.ttf', 'Italic': 'Lora/Lora-Italic.ttf'},
    'Lora Medium':             {'Regular': 'Lora/Lora-Medium.ttf', 'Italic': 'Lora/Lora-MediumItalic.ttf'},
    'Lora SemiBold':           {'Regular': 'Lora/Lora-SemiBold.ttf', 'Italic': 'Lora/Lora-SemiBoldItalic.ttf'},
    'Be Vietnam Pro':          {'Regular': 'BeVietnamPro/BeVietnamPro-Regular.ttf', 'Bold': 'BeVietnamPro/BeVietnamPro-Bold.ttf'},
    'Be Vietnam Pro Medium':   {'Regular': 'BeVietnamPro/BeVietnamPro-Medium.ttf'},
    'Be Vietnam Pro SemiBold': {'Regular': 'BeVietnamPro/BeVietnamPro-SemiBold.ttf'},
}
SLOT_ORDER = ['Regular', 'Bold', 'Italic', 'BoldItalic']
TEMPLATE_CT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml'
DOC_CT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'
FONT_REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/font'

def word_pids():
    out = subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Process WINWORD -ErrorAction SilentlyContinue | '
                          'ForEach-Object { "$($_.Id)|$($_.MainWindowTitle)" }'], capture_output=True, text=True).stdout
    return {int(l.split('|')[0]): l.split('|', 1)[1] for l in out.splitlines() if '|' in l}

def ps(mode, src, dst):
    before = word_pids()
    if os.path.exists(dst): os.remove(dst)
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'word_com.ps1'),
                    '-Mode', mode, '-InFile', src, '-OutFile', dst], check=False)
    for pid, title in word_pids().items():   # stop only headless Word instances started by this call
        if pid not in before and not title.strip():
            subprocess.run(['powershell', '-NoProfile', '-Command', f'Stop-Process -Id {pid} -Force -Confirm:$false'])
    if not os.path.exists(dst): raise RuntimeError(f'Word {mode} failed for {src}')

def obfuscate(data, guid):
    """ECMA-376 Part 1 §17.8.1: XOR the first 32 bytes with the GUID key (bytes read from the end of the GUID string)."""
    h = guid.strip('{}').replace('-', '')
    key = [int(h[i:i + 2], 16) for i in range(30, -1, -2)]
    b = bytearray(data)
    for i in range(32): b[i] ^= key[i % 16]
    return bytes(b)

def embed_and_templatise(src_docx, dst_dotx):
    zin = zipfile.ZipFile(src_docx)
    files = {n: zin.read(n) for n in zin.namelist()}
    ft = files['word/fontTable.xml'].decode('utf-8')
    if 'xmlns:r=' not in ft[:600]:
        ft = ft.replace('<w:fonts ', '<w:fonts xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
    rels_name = 'word/_rels/fontTable.xml.rels'
    rels = files.get(rels_name, b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                     b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>').decode('utf-8')
    rels = re.sub(r'<Relationship [^>]*relationships/font"[^>]*/>', '', rels)
    for n in [n for n in files if n.startswith('word/fonts/')]: del files[n]
    k = 0
    for fam, slots in EMBED.items():
        embeds = ''
        for slot in SLOT_ORDER:
            if slot not in slots: continue
            k += 1; rid = f'rIdVcciFont{k}'; guid = '{' + str(uuid.uuid4()).upper() + '}'
            files[f'word/fonts/font{k}.odttf'] = obfuscate(open(os.path.join(FONTDIR, slots[slot]), 'rb').read(), guid)
            rels = rels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="{FONT_REL}" Target="fonts/font{k}.odttf"/></Relationships>')
            embeds += f'<w:embed{slot} r:id="{rid}" w:fontKey="{guid}"/>'
        pat = re.compile(r'(<w:font w:name="' + re.escape(fam) + r'"[^>]*?)(/>|>(.*?)</w:font>)', re.S)
        m = pat.search(ft)
        if m:
            inner = re.sub(r'<w:embed(Regular|Bold|Italic|BoldItalic)[^>]*/>', '', m.group(3) or '')
            ft = ft[:m.start()] + f'{m.group(1)}>{inner}{embeds}</w:font>' + ft[m.end():]
        else:
            ft = ft.replace('</w:fonts>', f'<w:font w:name="{fam}"><w:charset w:val="00"/><w:family w:val="auto"/>'
                                          f'<w:pitch w:val="variable"/>{embeds}</w:font></w:fonts>')
    files['word/fontTable.xml'] = ft.encode('utf-8'); files[rels_name] = rels.encode('utf-8')

    st = files['word/settings.xml'].decode('utf-8')
    st = re.sub(r'<w:(embedTrueTypeFonts|saveSubsetFonts)[^>]*/>', '', st)
    # embedTrueTypeFonts follows view/zoom/removePersonalInformation/.../printFormsData in CT_Settings
    m = None
    for m in re.finditer(r'<w:(?:view|zoom|removePersonalInformation|removeDateAndTime|doNotDisplayPageBoundaries|displayBackgroundShape|printPostScriptOverText|printFractionalCharacterWidth|printFormsData)[^>]*/>', st): pass
    ins = '<w:embedTrueTypeFonts/>'
    st = st[:m.end()] + ins + st[m.end():] if m else re.sub(r'(<w:settings[^>]*>)', r'\1' + ins, st, 1)
    files['word/settings.xml'] = st.encode('utf-8')

    table_styles.inject(files)
    ct = files['[Content_Types].xml'].decode('utf-8')
    if 'Extension="odttf"' not in ct:
        ct = ct.replace('<Default ', '<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/><Default ', 1)
    if dst_dotx.endswith('.dotx'): ct = ct.replace(DOC_CT, TEMPLATE_CT)
    files['[Content_Types].xml'] = ct.encode('utf-8')

    with zipfile.ZipFile(dst_dotx, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in ['[Content_Types].xml'] + [n for n in files if n != '[Content_Types].xml']:
            z.writestr(n, files[n])

def main():
    busy = [t for t in word_pids().values() if t.strip()]
    if busy:   # never automate Word while the user has documents open in it
        raise SystemExit('Close Microsoft Word before running this script (open: ' + '; '.join(busy) + ')')
    for f in sorted(os.listdir(SRC)):
        if not f.endswith('.docx') or f.startswith('~$'): continue
        base = f[:-5]
        staged = os.path.join(STAGE, f)
        pre = os.path.join(STAGE, 'pre_' + f)        # table styles must exist before Word opens the file
        zin = zipfile.ZipFile(os.path.join(SRC, f)); parts = {n: zin.read(n) for n in zin.namelist()}; zin.close()
        table_styles.inject(parts)
        with zipfile.ZipFile(pre, 'w', zipfile.ZIP_DEFLATED) as z:
            for n in ['[Content_Types].xml'] + [n for n in parts if n != '[Content_Types].xml']: z.writestr(n, parts[n])
        ps('update', pre, staged)
        dotx = os.path.join(DEST, base + '.dotx')
        embed_and_templatise(staged, dotx)
        pdf = os.path.join(PREV, base + '.pdf')
        ps('pdf', dotx, pdf)
        for old in [p for p in os.listdir(PREV) if p.startswith(base + '-') and p.endswith('.png')]: os.remove(os.path.join(PREV, old))
        subprocess.run([PDFTOPPM, '-png', '-r', '70', pdf, os.path.join(PREV, base)], check=True)
        print('ok', base, f'{os.path.getsize(dotx)/1024:.0f} KB')

if __name__ == '__main__':
    main()
