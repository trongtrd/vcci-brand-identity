// ---------------------------------------------------------------- VCCI shared Typst layer (hand-written source)
// Uses the generated tokens above it: VCCI (colours), VCCI-SCALE, VCCI-SERIES, VCCI-STATUS, VCCI-FONT, VCCI-LOGO, VCCI-LOGO-PLATE.
// Print type scale from the brand guidelines (section 04): H1 Lora Medium 22 pt, H2 Lora SemiBold 14 pt,
// H3 / label Be Vietnam Pro SemiBold 8.5 pt uppercase, body Be Vietnam Pro 10 pt (leading 1.4), caption 7.5 pt.

#let vcci-logo(width: auto, height: auto, plate: false) = image(
  bytes(if plate { VCCI-LOGO-PLATE } else { VCCI-LOGO }), format: "svg", width: width, height: height)

// One gold gesture: a short gold rule under a chapter title.
#let vcci-gold-rule(width: 14mm) = block(above: 3mm, below: 5mm, rect(width: width, height: 0.8mm, fill: VCCI.gold, stroke: none))

// Small uppercase label above a title ("CHƯƠNG 01", "PHƯƠNG PHÁP").
#let vcci-label(body, fill: VCCI.bronze-ink) = text(
  font: VCCI-FONT.text, weight: 600, size: 7.5pt, tracking: 0.2em, fill: fill, upper(body))

// Lead paragraph: two or three sentences carrying the main message.
#let vcci-lead(body) = block(above: 4mm, below: 5mm,
  text(font: VCCI-FONT.display, size: 12.5pt, fill: VCCI.blue, body))

// Callout with a blue left rule on Blue Tint (the "VCCI Callout" Word style).
#let vcci-callout(body, title: none) = block(
  width: 100%, fill: VCCI.blue-tint, inset: (x: 5mm, y: 4mm), stroke: (left: 0.8mm + VCCI.blue), breakable: true,
  {
    if title != none { block(below: 2mm, text(weight: 600, fill: VCCI.blue, title)) }
    body
  })

// Base page, text, heading, table and caption rules shared by every VCCI format.
#let vcci-base(doc, lang: "vi", region: "VN", margin: (x: 22mm, top: 22mm, bottom: 22mm), fontsize: 10pt, footer-text: none) = {
  set document(keywords: ("VCCI",))
  set page(paper: "a4", margin: margin, numbering: "1",
    footer: context {
      set text(font: VCCI-FONT.text, size: 7pt, fill: VCCI.slate, tracking: 0.04em)
      grid(columns: (1fr, auto),
        if footer-text != none { footer-text } else { [Liên đoàn Thương mại và Công nghiệp Việt Nam] },
        counter(page).display("1"))
    })
  // Vietnamese is not hyphenated by syllable; left-aligned text, no justification
  set text(font: VCCI-FONT.text, size: fontsize, lang: lang, region: region, hyphenate: false, fill: VCCI.ink)
  set par(leading: 0.62em, spacing: 1.1em, justify: false)
  show heading: set text(font: VCCI-FONT.display, fill: VCCI.blue, weight: 500)
  show heading.where(level: 1): it => block(above: 9mm, below: 4mm, text(size: 22pt, it))
  show heading.where(level: 2): it => block(above: 6mm, below: 3mm, text(size: 14pt, weight: 600, it))
  show heading.where(level: 3): it => block(above: 5mm, below: 2mm,
    text(font: VCCI-FONT.text, size: 8.5pt, weight: 600, tracking: 0.18em, fill: VCCI.bronze-ink, upper(it.body)))
  show heading.where(level: 4): it => block(above: 4mm, below: 2mm, text(font: VCCI-FONT.text, size: fontsize, weight: 600, fill: VCCI.ink, it.body))
  // tables: blue header row, thin horizontal rules (the "VCCI Table" style)
  set table(stroke: (x, y) => (top: if y > 0 { 0.4pt + VCCI.stone }, bottom: 0.6pt + VCCI-SCALE.slate.at("20")),
    fill: (x, y) => if y == 0 { VCCI.blue }, inset: (x: 2.2mm, y: 1.8mm))
  show table.cell.where(y: 0): set text(fill: white, weight: 600)
  show table: set text(size: 0.9 * fontsize)
  // captions above tables, below figures; caption text 7.5 pt Slate
  show figure.where(kind: table): set figure.caption(position: top)
  show figure.caption: set text(size: 8pt, fill: VCCI.slate)
  show figure.caption: it => align(left, it)
  show link: set text(fill: VCCI.blue)
  show footnote.entry: set text(size: 7.5pt)
  set footnote.entry(separator: line(length: 20mm, stroke: 0.5pt + VCCI.gold))
  doc
}
