// ---------------------------------------------------------------- VCCI shared Typst layer (hand-written source)
// Uses the generated constants above it: VCCI (colours), VCCI-SCALE, VCCI-STATUS, VCCI-SERIES, VCCI-FONT,
// VCCI-LOGO, VCCI-LOGO-PLATE, VCCI-LOCKUP, VCCI-RING, VCCI-HERO.
// Print type scale from the brand guidelines (section 04): H1 Lora Medium 22 pt, H2 Lora SemiBold 14 pt,
// H3 / label Be Vietnam Pro SemiBold 8.5 pt uppercase, body Be Vietnam Pro 10 pt (leading 1.4), caption 7.5 pt.

// Words the templates write themselves, by document language (Quarto's own labels come from _extension.yml)
#let VCCI-LABELS = (
  vi: (org: "Liên đoàn Thương mại và Công nghiệp Việt Nam", contents: "Mục lục", chapter: "Chương", page: "Trang",
       report: "Báo cáo", client: "Thực hiện cho", team: "Nhóm thực hiện", version: "Phiên bản", citation: "Trích dẫn",
       suggested-citation: "Trích dẫn đề nghị", disclaimer: "Lưu ý", abstract: "Tóm tắt", keywords: "Từ khóa",
       jel: "Mã JEL", number: "số", number-cap: "Số", correspondence: "Tác giả liên hệ", city: "Hà Nội", acknowledgements: "Lời cảm ơn",
       memo: "Tờ trình", to: "Gửi", from: "Từ", cc: "Đồng gửi", date: "Ngày", subject: "Về việc", attachments: "Tài liệu kèm theo",
       wp-disclaimer: "Quan điểm trong bài là của tác giả, không nhất thiết phản ánh quan điểm của Liên đoàn Thương mại và Công nghiệp Việt Nam."),
  en: (org: "Vietnam Chamber of Commerce and Industry", contents: "Contents", chapter: "Chapter", page: "Page",
       report: "Report", client: "Prepared for", team: "Team", version: "Version", citation: "Citation",
       suggested-citation: "Suggested citation", disclaimer: "Disclaimer", abstract: "Abstract", keywords: "Keywords",
       jel: "JEL classification", number: "No.", number-cap: "No.", correspondence: "Corresponding author", city: "Hanoi", acknowledgements: "Acknowledgements",
       memo: "Memo", to: "To", from: "From", cc: "Cc", date: "Date", subject: "Subject", attachments: "Attachments",
       wp-disclaimer: "The views expressed are those of the authors and do not necessarily reflect the views of the Vietnam Chamber of Commerce and Industry."),
)
#let vcci-l(lang, key) = VCCI-LABELS.at(if lang in VCCI-LABELS { lang } else { "en" }).at(key)

// The blue used on every VCCI cover and blue page (as in the Word and PowerPoint templates)
#let VCCI-COVER-BLUE = gradient.linear(rgb("#2B4FA0"), rgb("#1E3D86"), angle: 70deg)

#let vcci-svg(s, ..args) = image(bytes(s), format: "svg", ..args)
#let vcci-logo(width: auto, height: auto, plate: false) = vcci-svg(if plate { VCCI-LOGO-PLATE } else { VCCI-LOGO }, width: width, height: height)
#let vcci-lockup(width: auto) = vcci-svg(VCCI-LOCKUP, width: width)
#let vcci-ring(size) = vcci-svg(VCCI-RING, width: size)

// Hero icon by number (1–24 or "01"–"24"); variant "gold" for blue fields, "blue" for light pages
#let vcci-hero(num, variant: "gold", size: 20mm) = {
  let key = str(num).trim()
  if key.len() == 1 { key = "0" + key }
  if key in VCCI-HERO { vcci-svg(VCCI-HERO.at(key).at(variant), width: size) }
}

// One gold gesture: a short gold rule under a chapter title.
#let vcci-gold-rule(width: 14mm) = block(above: 3mm, below: 5mm, rect(width: width, height: 0.8mm, fill: VCCI.gold, stroke: none))

// Small uppercase label above a title ("CHƯƠNG 01", "PHƯƠNG PHÁP").
#let vcci-label(body, fill: VCCI.bronze-ink) = text(
  font: VCCI-FONT.text, weight: 600, size: 7.5pt, tracking: 0.2em, fill: fill, upper(body))

// Lead paragraph: two or three sentences carrying the main message.
#let vcci-lead(body) = block(above: 4mm, below: 5mm,
  text(font: VCCI-FONT.display, size: 12.5pt, fill: VCCI.blue, body))

// Box with a blue left rule on Blue Tint (the "VCCI Callout" Word style).
#let vcci-callout(body, title: none) = block(
  width: 100%, fill: VCCI.blue-tint, inset: (x: 5mm, y: 4mm), stroke: (left: 0.8mm + VCCI.blue), breakable: true,
  {
    if title != none { block(below: 2mm, text(weight: 600, fill: VCCI.blue, title)) }
    body
  })

// Key figures: a row of cards, each a large Lora number and a short label.
#let vcci-figures(items) = block(above: 5mm, below: 6mm, grid(
  columns: (1fr,) * calc.min(items.len(), 4), column-gutter: 3mm, row-gutter: 3mm,
  fill: VCCI.blue-tint, inset: (x: 4mm, y: 3.5mm),
  ..items.map(((value, label)) => stack(spacing: 2.5mm,
    text(font: VCCI-FONT.display, size: 22pt, weight: 500, fill: VCCI.blue, value),
    text(size: 7.5pt, fill: VCCI.slate, label)))))

// Quarto callouts in VCCI status colours. Quarto passes its own icon colour per callout type; map it to VCCI status.
#let callout(body: [], title: "Callout", background_color: none, icon: none, icon_color: black, body_background_color: white) = {
  let kind = (
    "#0758e5": "info", "#00a047": "success", "#eb9113": "warning", "#fc5300": "warning", "#cc1914": "error",
  ).at(lower(icon_color.to-hex()), default: "info")
  let s = VCCI-STATUS.at(kind)
  block(width: 100%, breakable: true, fill: s.background, stroke: (left: 0.8mm + s.strong), inset: (x: 5mm, y: 3.5mm), above: 5mm, below: 5mm, {
    block(below: if body != [] { 2mm } else { 0mm }, text(weight: 600, fill: s.strong, {
      if icon != none { text(fill: s.strong, icon); h(1.5mm) }
      title
    }))
    body
  })
}

// Diagonal "BẢN THẢO" / "MẬT" mark behind the text of every page
#let vcci-status-mark(status) = if status != none {
  place(center + horizon, rotate(-35deg, text(font: VCCI-FONT.text, weight: 700, size: 72pt, tracking: 0.1em,
    fill: VCCI.slate.transparentize(88%), upper(status))))
}

// Heading number (when the numbering gives one) followed by the title
#let vcci-heading-text(it) = {
  let n = if it.numbering != none { numbering(it.numbering, ..counter(heading).at(it.location())) }
  if n != none and n != "" [#n#h(0.7em)]
  it.body
}

// Base page, text, heading, table and caption rules shared by every VCCI format.
#let vcci-base(doc, lang: "vi", region: "VN", margin: (x: 22mm, top: 22mm, bottom: 22mm), fontsize: 10pt,
  header: none, footer: auto, status: none) = {
  set document(keywords: ("VCCI",))
  let default-footer = context {
    set text(font: VCCI-FONT.text, size: 7pt, fill: VCCI.slate, tracking: 0.04em)
    grid(columns: (1fr, auto), vcci-l(lang, "org"), counter(page).display("1"))
  }
  set page(paper: "a4", margin: margin, numbering: "1", header: header,
    footer: if footer == auto { default-footer } else { footer },
    background: vcci-status-mark(status))
  // Vietnamese is not hyphenated by syllable; left-aligned text, no justification
  set text(font: VCCI-FONT.text, size: fontsize, lang: lang, region: region, hyphenate: false, fill: VCCI.ink)
  set par(leading: 0.62em, spacing: 1.1em, justify: false)
  show heading: set text(font: VCCI-FONT.display, fill: VCCI.blue, weight: 500)
  // set the size before the leading, so that em is the heading's size (room for stacked Vietnamese diacritics)
  show heading.where(level: 1): it => block(above: 9mm, below: 4mm, { set text(size: 22pt); set par(leading: 0.5em); vcci-heading-text(it) })
  show heading.where(level: 2): it => block(above: 6mm, below: 3mm, { set text(size: 14pt, weight: 600); set par(leading: 0.5em); vcci-heading-text(it) })
  show heading.where(level: 3): it => block(above: 5mm, below: 2mm,
    text(font: VCCI-FONT.text, size: 8.5pt, weight: 600, tracking: 0.18em, fill: VCCI.bronze-ink, upper(it.body)))
  show heading.where(level: 4): it => block(above: 4mm, below: 2mm, text(font: VCCI-FONT.text, size: fontsize, weight: 600, fill: VCCI.ink, it.body))
  // tables: blue header row, thin horizontal rules (the "VCCI Table" style)
  set table(stroke: (x, y) => (top: if y > 0 { 0.4pt + VCCI.stone }, bottom: 0.6pt + VCCI-SCALE.slate.at("20")),
    fill: (x, y) => if y == 0 { VCCI.blue }, inset: (x: 2.2mm, y: 1.8mm))
  show table.cell.where(y: 0): set text(fill: white, weight: 600)
  show table: set text(size: 0.9 * fontsize)
  // captions above tables, below figures; caption text 8 pt Slate, left-aligned
  show figure.where(kind: table): set figure.caption(position: top)
  show figure.where(kind: "quarto-float-tbl"): set align(left)
  // long tables continue on the next page (header row repeats); figures stay whole
  show figure.where(kind: "quarto-float-tbl"): set block(breakable: true)
  show figure.caption: set text(size: 8pt, fill: VCCI.slate)
  show figure.caption: it => align(left, it)
  show link: set text(fill: VCCI.blue)
  // code: JetBrains Mono (the brand fonts have no monospace), no ligatures (R's "<-" stays two characters);
  // colours and the Ivory ground come from the highlighting theme vcci.theme
  show raw: set text(font: VCCI-FONT.code, size: 0.9em, ligatures: false, features: (calt: 0))
  show footnote.entry: set text(size: 7.5pt)
  set footnote.entry(separator: line(length: 20mm, stroke: 0.5pt + VCCI.gold))
  doc
}
