// ---------------------------------------------------------------- vcci-wp: VCCI Working Paper (hand-written source)
// Title page: series and number, title, authors, date, abstract(s), keywords, JEL codes, suggested citation and
// disclaimer. Then numbered sections (1, 1.1) on running pages, references at the end. A4, no colour cover.

#let vcci-wp(
  title: none,
  subtitle: none,
  series: "VCCI Working Paper",
  number: none,
  authors: none,
  date: none,
  version: none,
  status: none,
  short-title: none,
  abstract: none,
  abstract-alt: none,          // abstract in the other language (English for a Vietnamese paper, and vice versa)
  keywords: none,
  keywords-alt: none,
  jel: none,
  thanks: none,
  citation: none,
  disclaimer: none,
  lang: "vi",
  region: "VN",
  fontsize: 10pt,
  sectionnumbering: "1.1",
  toc: false,
  toc_title: none,
  toc_depth: none,
  doc,
) = {
  set document(title: title)
  set document(author: authors.map(a => content-to-string(a.name)).join(", ")) if authors != none and authors != ()
  let L = key => vcci-l(lang, key)
  let alt = if lang == "vi" { "en" } else { "vi" }
  let year = if date != none { content-to-string(date).find(regex("\d{4}")) } else { none }
  let series-number = if number != none [#series #L("number") #number] else [#series]
  let running = if short-title != none { short-title } else { title }

  let header = context if counter(page).get().first() > 1 {
    set text(font: VCCI-FONT.text, size: 7pt, fill: VCCI.slate, tracking: 0.03em)
    grid(columns: (auto, 1fr), align: (left + horizon, right + horizon), series-number, running)
    v(-1.5mm)
    line(length: 100%, stroke: 0.4pt + VCCI.stone)
  }
  let footer = context {
    set text(font: VCCI-FONT.text, size: 7pt, fill: VCCI.slate, tracking: 0.04em)
    grid(columns: (1fr, auto), [vcci.com.vn], counter(page).display("1"))
  }
  show: vcci-base.with(lang: lang, region: region, fontsize: fontsize, margin: (x: 25mm, top: 25mm, bottom: 24mm),
    header: header, footer: footer, status: status)

  // academic sections: 1 and 1.1 numbered, smaller than a report's chapters, no page break
  set heading(numbering: (..n) => if n.pos().len() <= 2 { numbering(sectionnumbering, ..n.pos()) })
  show heading.where(level: 1): it => block(above: 8mm, below: 3.5mm, sticky: true, {
    set text(size: 15pt); set par(leading: 0.5em); vcci-heading-text(it) })
  show heading.where(level: 2): it => block(above: 6mm, below: 2.5mm, sticky: true, {
    set text(size: 12pt, weight: 600); set par(leading: 0.5em); vcci-heading-text(it) })
  set math.equation(numbering: "(1)")

  // ------------------------------------------------ title page
  grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
    vcci-logo(width: 30mm),
    align(right, {
      vcci-label(series)
      if number != none { linebreak(); text(font: VCCI-FONT.display, size: 13pt, fill: VCCI.blue, [#L("number-cap") #number]) }
    }))
  v(2mm)
  line(length: 100%, stroke: 0.4pt + VCCI.stone)
  if status != none {
    block(above: 4mm, box(stroke: 0.6pt + VCCI.bronze-ink, inset: (x: 2.5mm, y: 1.3mm),
      text(weight: 700, size: 7pt, tracking: 0.18em, fill: VCCI.bronze-ink, upper(status))))
  }
  if title != none {
    block(above: 9mm, below: 0mm, {
      set text(font: VCCI-FONT.display, size: 22pt, weight: 500, fill: VCCI.blue)
      set par(leading: 0.5em)
      title
      // † for acknowledgements: * marks the corresponding author
      if thanks != none { footnote(numbering: n => "†", thanks) }
    })
  }
  if subtitle != none { block(above: 3.5mm, text(size: 11pt, fill: VCCI.slate, subtitle)) }
  vcci-gold-rule()

  // authors: name, affiliation, e-mail; * marks the corresponding author
  if authors != none and authors != () {
    grid(columns: (1fr,) * calc.min(authors.len(), 3), column-gutter: 6mm, row-gutter: 4mm,
      ..authors.map(a => {
        text(weight: 600, [#a.name#if a.corresponding [\*]])
        if a.affiliation != [] { linebreak(); text(size: 8.5pt, fill: VCCI.slate, a.affiliation) }
        if a.email != [] { linebreak(); text(size: 8.5pt, fill: VCCI.blue, a.email) }
      }))
  }
  if date != none or version != none {
    block(above: 5mm, text(size: 8.5pt, fill: VCCI.slate, [#date#if version != none [ · #L("version") #version]]))
  }

  let abstract-block(lng, body, kw) = block(above: 6mm, width: 100%, {
    vcci-label(vcci-l(lng, "abstract"))
    block(above: 2mm, below: 0mm, text(size: 9.5pt, body))
    if kw != none and kw != () {
      block(above: 2.5mm, text(size: 8.5pt, [#text(weight: 600, vcci-l(lng, "keywords")): #kw.join("; ")]))
    }
  })
  if abstract != none { abstract-block(lang, abstract, keywords) }
  if abstract-alt != none { abstract-block(alt, abstract-alt, keywords-alt) }
  if jel != none and jel != () {
    block(above: 2.5mm, text(size: 8.5pt, [#text(weight: 600, L("jel")): #jel.join(", ")]))
  }
  let corr = if authors != none { authors.filter(a => a.corresponding) } else { () }

  // citation and disclaimer at the foot of the title page
  v(1fr)
  block(width: 100%, inset: (top: 3mm), stroke: (top: 0.4pt + VCCI.stone), {
    set text(size: 7.5pt, fill: VCCI.slate)
    let auto-citation = {
      let names = if authors != none and authors != () { authors.map(a => a.name).join(", ") } else { L("org") }
      [#names (#if year != none { year } else [n.d.]). #title. #series-number. #L("city"): #L("org").]
    }
    block(below: 2mm, [#text(weight: 600, L("suggested-citation")): #if citation != none { citation } else { auto-citation }])
    if corr.len() > 0 {
      block(below: 2mm, [#text(weight: 600, L("correspondence")): #corr.map(a => [#a.name#if a.email != [] [, #a.email]]).join("; ")])
    }
    block(below: 2mm, if disclaimer != none { disclaimer } else { L("wp-disclaimer") })
    [© #if year != none [#year ]#L("org") (VCCI)]
  })
  pagebreak()

  if toc {
    outline(title: if toc_title == none { L("contents") } else { toc_title }, depth: toc_depth, indent: 4mm)
    pagebreak()
  }
  doc
}
