"""Export a presentation to PDF and PNG slide previews with Microsoft PowerPoint (Windows only).

    python finalize.py deck_VCCI.pptx            # writes deck_VCCI.pdf
    python finalize.py deck_VCCI.pptx --png      # also writes deck_VCCI_pages/page-01.png ...

PowerPoint also re-saves the file, which embeds the VCCI fonts. Stops without touching PowerPoint when the user
has a presentation open in it. Without PowerPoint, skip this step.
"""
import argparse, os, shutil, subprocess, sys

PS = r'''
param([string]$InFile, [string]$PdfFile, [string]$Resave)
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
try {
  $pres = $app.Presentations.Open($InFile, $false, $false, $false)
  if ($Resave -eq '1') { $pres.Save() }
  $pres.SaveAs($PdfFile, 32)
  try { $pres.Close() } catch {}
} finally {
  try { $app.Quit() } catch {}
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
'''


def ppt_windows():
    out = subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Process POWERPNT -ErrorAction SilentlyContinue | '
                          'ForEach-Object { "$($_.Id)|$($_.MainWindowTitle)" }'], capture_output=True, text=True).stdout
    return {int(l.split('|')[0]): l.split('|', 1)[1] for l in out.splitlines() if '|' in l}


def find_pdftoppm():
    return os.environ.get('VCCI_PDFTOPPM') or shutil.which('pdftoppm') or next(
        (p for p in (os.path.expandvars(r'%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdftoppm.exe'),
                     os.path.expandvars(r'%ProgramFiles%\MiKTeX\miktex\bin\x64\pdftoppm.exe')) if os.path.exists(p)), None)


def export(pptx, png=False, dpi=50, resave=True):
    if sys.platform != 'win32': raise SystemExit('finalize.py needs Microsoft PowerPoint on Windows.')
    busy = [t for t in ppt_windows().values() if t.strip()]
    if busy:
        raise SystemExit('PowerPoint has presentations open (' + '; '.join(busy) + '). Ask the user to close PowerPoint, then run again.')
    src = os.path.abspath(pptx); base = os.path.splitext(src)[0]; pdf = base + '.pdf'
    script = base + '_ppt.ps1'
    open(script, 'w', encoding='utf-8-sig').write(PS)
    before = ppt_windows()
    try:
        if os.path.exists(pdf): os.remove(pdf)
        subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script,
                        '-InFile', src, '-PdfFile', pdf, '-Resave', '1' if resave else '0'], check=False)
    finally:
        os.remove(script)
        for pid, title in ppt_windows().items():   # stop only a windowless PowerPoint this call started
            if pid not in before and not title.strip():
                subprocess.run(['powershell', '-NoProfile', '-Command', f'Stop-Process -Id {pid} -Force -Confirm:$false'])
    if not os.path.exists(pdf): raise SystemExit(f'PowerPoint PDF export failed for {src}')
    print('Wrote', pdf)
    if png:
        exe = find_pdftoppm()
        if not exe: raise SystemExit('pdftoppm not found (install Poppler or set VCCI_PDFTOPPM).')
        outdir = base + '_pages'
        shutil.rmtree(outdir, ignore_errors=True); os.makedirs(outdir)
        subprocess.run([exe, '-png', '-r', str(dpi), pdf, os.path.join(outdir, 'page')], check=True)
        print('Wrote slide previews to', outdir)
    return pdf


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('pptx')
    ap.add_argument('--png', action='store_true', help='also render slide PNGs with pdftoppm (Poppler)')
    ap.add_argument('--dpi', type=int, default=50)
    ap.add_argument('--no-save', action='store_true', help='export only; do not re-save the presentation')
    a = ap.parse_args()
    export(a.pptx, a.png, a.dpi, not a.no_save)


if __name__ == '__main__':
    main()
