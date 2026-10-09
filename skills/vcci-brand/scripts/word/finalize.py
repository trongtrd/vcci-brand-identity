"""Refresh the table of contents with Microsoft Word, then export a PDF and PNG page previews (Windows only).

    python finalize.py report_VCCI.docx            # updates the .docx in place, writes report_VCCI.pdf
    python finalize.py report_VCCI.docx --png      # also writes report_VCCI_pages/page-01.png ...

Stops without touching Word when the user has a document open in it. Without Word, skip this step: the
report opens fine and Word refreshes the table of contents when the user opens it.
"""
import argparse, os, re, subprocess, sys, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_package, write_package

PS = r'''
param([string]$Mode, [string]$InFile, [string]$OutFile)
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false; $word.DisplayAlerts = 0
try {
  if ($Mode -eq 'update') {
    $doc = $word.Documents.Open($InFile, $false, $false, $false)
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Fields.Update() | Out-Null
    $doc.SaveAs2($OutFile, 16)
  } else {
    $doc = $word.Documents.Open($InFile, $false, $true, $false)
    $doc.ExportAsFixedFormat($OutFile, 17)
  }
  try { $doc.Close($false) } catch {}
} finally {
  try { $word.Quit() } catch {}
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
'''


def word_windows():
    out = subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Process WINWORD -ErrorAction SilentlyContinue | '
                          'ForEach-Object { "$($_.Id)|$($_.MainWindowTitle)" }'], capture_output=True, text=True).stdout
    return {int(l.split('|')[0]): l.split('|', 1)[1] for l in out.splitlines() if '|' in l}


def run_word(mode, src, dst, script):
    before = word_windows()
    if os.path.exists(dst): os.remove(dst)
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script,
                    '-Mode', mode, '-InFile', src, '-OutFile', dst], check=False)
    for pid, title in word_windows().items():   # stop only the hidden Word instance this call started
        if pid not in before and not title.strip():
            subprocess.run(['powershell', '-NoProfile', '-Command', f'Stop-Process -Id {pid} -Force -Confirm:$false'])
    if not os.path.exists(dst): raise SystemExit(f'Word {mode} failed for {src}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('docx')
    ap.add_argument('--png', action='store_true', help='also render page PNGs with pdftoppm (Poppler)')
    ap.add_argument('--dpi', type=int, default=60)
    a = ap.parse_args()
    if sys.platform != 'win32': raise SystemExit('finalize.py needs Microsoft Word on Windows.')
    busy = [t for t in word_windows().values() if t.strip()]
    if busy:
        raise SystemExit('Microsoft Word has documents open (' + '; '.join(busy) + '). Ask the user to close Word, then run again.')

    src = os.path.abspath(a.docx); base = os.path.splitext(src)[0]
    script = base + '_word.ps1'
    open(script, 'w', encoding='utf-8-sig').write(PS)
    try:
        tmp = base + '_updated.docx'
        run_word('update', src, tmp, script)
        files = read_package(tmp)     # TOC is now current: drop the "update fields on open" prompt
        files['word/settings.xml'] = re.sub(rb'<w:updateFields[^>]*/>', b'', files['word/settings.xml'])
        write_package(files, src); os.remove(tmp)
        pdf = base + '.pdf'
        run_word('pdf', src, pdf, script)
        print('Wrote', pdf)
    finally:
        if os.path.exists(script): os.remove(script)

    if a.png:
        exe = os.environ.get('VCCI_PDFTOPPM') or shutil.which('pdftoppm') or next(
            (p for p in (os.path.expandvars(r'%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdftoppm.exe'),
                         os.path.expandvars(r'%ProgramFiles%\MiKTeX\miktex\bin\x64\pdftoppm.exe')) if os.path.exists(p)), None)
        if not exe: raise SystemExit('pdftoppm not found (install Poppler or set VCCI_PDFTOPPM).')
        outdir = base + '_pages'; os.makedirs(outdir, exist_ok=True)
        subprocess.run([exe, '-png', '-r', str(a.dpi), pdf, os.path.join(outdir, 'page')], check=True)
        print('Wrote page previews to', outdir)


if __name__ == '__main__':
    main()
