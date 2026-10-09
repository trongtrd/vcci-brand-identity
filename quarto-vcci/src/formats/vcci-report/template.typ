// ---------------------------------------------------------------- vcci-report: consulting report (hand-written source)
// Step 1 skeleton: title block, table of contents and the shared base layer. The full cover, chapter openers and
// back cover come in step 2 of docs/PLAN_QUARTO_VCCI.md.

#let vcci-report(
  title: none,
  subtitle: none,
  label: "Báo cáo",
  authors: none,
  date: none,
  abstract: none,
  abstract-title: "Tóm tắt",
  lang: "vi",
  region: "VN",
  fontsize: 10pt,
  sectionnumbering: none,
  toc: false,
  toc_title: none,
  toc_depth: none,
  doc,
) = {
  set document(title: title)
  set document(author: authors.map(a => content-to-string(a.name)).join(", ")) if authors != none and authors != ()
  set heading(numbering: sectionnumbering)
  show: vcci-base.with(lang: lang, region: region, fontsize: fontsize)

  // title block
  vcci-logo(width: 38mm)
  v(10mm)
  if label != none { vcci-label(label) }
  if title != none {
    block(above: 3mm, below: 0mm, text(font: VCCI-FONT.display, size: 26pt, weight: 500, fill: VCCI.blue, title))
  }
  if subtitle != none {
    block(above: 3mm, text(font: VCCI-FONT.display, size: 13pt, style: "italic", fill: VCCI.slate, subtitle))
  }
  vcci-gold-rule()
  if authors != none and authors != () {
    for a in authors { block(above: 1mm, below: 1mm, text(weight: 600, a.name)) }
  }
  if date != none { block(above: 2mm, text(fill: VCCI.slate, date)) }
  if abstract != none { vcci-callout(title: abstract-title, abstract) }

  if toc {
    let title = if toc_title == none { [Mục lục] } else { toc_title }
    block(above: 10mm, below: 8mm, outline(title: title, depth: toc_depth, indent: 1.5em))
  }
  doc
}
