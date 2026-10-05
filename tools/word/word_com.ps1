param(
  [Parameter(Mandatory = $true)][ValidateSet('update', 'pdf')][string]$Mode,
  [Parameter(Mandatory = $true)][string]$InFile,
  [Parameter(Mandatory = $true)][string]$OutFile
)
# update: refresh TOC/fields and save as .docx (wdFormatXMLDocument = 16)
# pdf:    open (read-only) and export as PDF (wdExportFormatPDF = 17)
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
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
  # Word occasionally crashes while closing a document after PDF export (seen with populated TOCs);
  # the PDF is already written at that point, so close/quit failures are ignored here.
  try { $doc.Close($false) } catch {}
} finally {
  try { $word.Quit() } catch {}
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
