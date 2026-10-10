// ---------------------------------------------------------------- vcci-memo: internal memo (hand-written source)
// One or two A4 pages: logo and "TỜ TRÌNH" ("MEMO" in English), routing block (to, from, cc, date, subject) closed by the gold rule,
// body, signature, attachments. From page 2 a running header repeats the subject. No cover.

#let vcci-memo(
  title: none,
  label: none,
  to: none,
  from: none,
  cc: none,
  date: none,
  priority: none,
  status: none,
  signature-name: none,
  signature-title: none,
  attachments: none,
  authors: none,
  lang: "vi",
  region: "VN",
  fontsize: 10pt,
  doc,
) = {
  set document(title: title)
  let L = key => vcci-l(lang, key)
  let sender = if from != none { from } else if authors != none and authors != () { authors.map(a => a.name).join(", ") }

  let header = context if counter(page).get().first() > 1 {
    set text(font: VCCI-FONT.text, size: 7pt, fill: VCCI.slate, tracking: 0.03em)
    grid(columns: (auto, 1fr), align: (left + horizon, right + horizon),
      [#if label != none { label } else { L("memo") }], title)
    v(-1.5mm)
    line(length: 100%, stroke: 0.4pt + VCCI.stone)
  }
  let footer = context {
    set text(font: VCCI-FONT.text, size: 7pt, fill: VCCI.slate, tracking: 0.04em)
    grid(columns: (1fr, auto), L("org"), [#L("page") #counter(page).display("1") / #counter(page).final().first()])
  }
  show: vcci-base.with(lang: lang, region: region, fontsize: fontsize, margin: (x: 22mm, top: 22mm, bottom: 22mm),
    header: header, footer: footer, status: status)
  set heading(numbering: none)
  show heading.where(level: 1): it => block(above: 6mm, below: 2.5mm, sticky: true, {
    set text(size: 13pt, weight: 600); set par(leading: 0.5em); it.body })
  show heading.where(level: 2): it => block(above: 5mm, below: 2mm, sticky: true, {
    set text(size: 11pt, weight: 600); set par(leading: 0.5em); it.body })

  // ------------------------------------------------ masthead and routing block
  grid(columns: (1fr, auto), align: (left + horizon, right + horizon),
    vcci-logo(width: 34mm),
    {
      if priority != none {
        box(stroke: 0.6pt + VCCI.bronze-ink, inset: (x: 2.5mm, y: 1.3mm),
          text(weight: 700, size: 7pt, tracking: 0.18em, fill: VCCI.bronze-ink, upper(priority)))
        h(4mm)
      }
      text(font: VCCI-FONT.display, size: 20pt, weight: 500, fill: VCCI.blue, upper(if label != none { label } else { L("memo") }))
    })
  v(3mm)
  line(length: 100%, stroke: 0.4pt + VCCI.stone)
  let rows = (
    (L("to"), to), (L("from"), sender), (L("cc"), cc), (L("date"), date),
  ).filter(r => r.at(1) != none)
  block(above: 5mm, grid(columns: (26mm, 1fr), row-gutter: 3mm, column-gutter: 3mm,
    ..rows.map(((k, v)) => (vcci-label(k, fill: VCCI.slate), v)).flatten(),
    ..(if title != none { (vcci-label(L("subject"), fill: VCCI.slate),
      { set text(font: VCCI-FONT.display, size: 13pt, weight: 600, fill: VCCI.blue); set par(leading: 0.5em); title }) } else { () })))
  vcci-gold-rule(width: 14mm)

  doc

  // ------------------------------------------------ signature and attachments
  if signature-name != none {
    // signature on the right half of the page
    block(above: 10mm, breakable: false, grid(columns: (1fr, 70mm), [], {
      text(weight: 600, signature-name)
      if signature-title != none { linebreak(); text(size: 8.5pt, fill: VCCI.slate, signature-title) }
    }))
  }
  if attachments != none and attachments != () {
    block(above: 8mm, breakable: false, {
      vcci-label(L("attachments"), fill: VCCI.slate)
      set text(size: 9pt)
      enum(..attachments)
    })
  }
}
