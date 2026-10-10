// ---------------------------------------------------------------- vcci-report: consulting report (hand-written source)
// Cover (as VCCI_Report.dotx), imprint page, contents, chapters with label and gold rule, running header and
// "Trang X / N" footer, back cover with the logo on a Paper plate. Page geometry in mm, A4.

#let VCCI-CONTACT = [Số 9 Đào Duy Anh, Đống Đa, Hà Nội · T +84 24 3574 2022 · vcci.com.vn]

#let vcci-report(
  title: none,
  subtitle: none,
  label: none,
  client: none,
  date: none,
  version: none,
  status: none,
  hero: none,
  short-title: none,
  authors: none,
  team: none,
  citation: none,
  disclaimer: none,
  contact: none,
  abstract: none,
  abstract-title: none,
  cover: true,
  back-cover: true,
  lang: "vi",
  region: "VN",
  fontsize: 10pt,
  toc: false,
  toc_title: none,
  toc_depth: none,
  doc,
) = {
  set document(title: title)
  set document(author: authors.map(a => content-to-string(a.name)).join(", ")) if authors != none and authors != ()
  let year = if date != none { content-to-string(date).find(regex("\d{4}")) } else { none }
  let running = if short-title != none { short-title } else { title }
  let L = key => vcci-l(lang, key)
  if label == none { label = L("report") }

  // inner pages: logo left, short title right, hairline; footer: web left, "Trang X / N" right
  let header = context {
    set text(font: VCCI-FONT.text, size: 7pt, fill: VCCI.slate, tracking: 0.03em)
    grid(columns: (auto, 1fr), align: (left + horizon, right + horizon),
      vcci-logo(width: 17mm),
      [#running#if year != none [ · #year]])
    v(-1.5mm)
    line(length: 100%, stroke: 0.4pt + VCCI.stone)
  }
  let footer = context {
    set text(font: VCCI-FONT.text, size: 7pt, fill: VCCI.slate, tracking: 0.04em)
    let end = query(<vcci-report-end>)
    let total = if end.len() > 0 { counter(page).at(end.first().location()).first() } else { counter(page).final().first() }
    grid(columns: (1fr, auto), [vcci.com.vn], [#L("page") #counter(page).display("1") / #total])
  }

  show: vcci-base.with(lang: lang, region: region, fontsize: fontsize, margin: (x: 22mm, top: 26mm, bottom: 22mm),
    header: header, footer: footer, status: status)

  // chapters: numbered level-1 headings only; a chapter starts a page with "CHƯƠNG 01", title and gold rule
  set heading(numbering: (..n) => if n.pos().len() == 1 { str(n.pos().first()) })
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(6mm)
    if it.numbering != none {
      let n = counter(heading).get().first()
      vcci-label([#L("chapter") #if n < 10 [0]#n])
    }
    block(above: 3mm, below: 0mm, { set text(font: VCCI-FONT.display, size: 26pt, weight: 500, fill: VCCI.blue); set par(leading: 0.5em); it.body })
    vcci-gold-rule()
  }
  // table of contents
  show outline.entry.where(level: 1): it => block(above: 4mm, text(font: VCCI-FONT.display, size: 11.5pt, fill: VCCI.blue, it))
  set outline.entry(fill: repeat(text(fill: VCCI.stone)[.], gap: 0.4em))

  // ------------------------------------------------ cover
  if cover {
    page(margin: 0mm, header: none, footer: none, background: none, numbering: none, {
      // paper upper part
      place(top + left, rect(width: 100%, height: 100%, fill: VCCI.paper, stroke: none))
      place(top + left, dx: 22mm, dy: 22mm, vcci-lockup(width: 92mm))
      if status != none {
        // not gold: the gold rule on the blue field is the cover's one gold gesture
        place(top + right, dx: -22mm, dy: 24mm, box(stroke: 0.6pt + VCCI.bronze-ink, inset: (x: 3mm, y: 1.6mm),
          text(weight: 700, size: 7.5pt, tracking: 0.18em, fill: VCCI.bronze-ink, upper(status))))
      }
      place(top + left, dx: 22mm, dy: 76mm, block(width: 166mm, {
        let l = if year != none [#label · #year] else [#label]
        vcci-label(l)
        if title != none {
          // leading in em of the title size: Vietnamese stacked diacritics need room (guidelines: line spacing ≥ 1.08)
          block(above: 4mm, below: 0mm, {
            set text(font: VCCI-FONT.display, size: 30pt, weight: 500, fill: VCCI.blue)
            set par(leading: 0.5em)
            title
          })
        }
        if subtitle != none {
          block(above: 5mm, text(font: VCCI-FONT.text, size: 11pt, fill: VCCI.slate, subtitle))
        }
      }))
      // blue lower part with drum-ring line art, gold rule, details and hero icon
      place(top + left, dy: 178mm, block(width: 210mm, height: 119mm, fill: VCCI-COVER-BLUE, clip: true, {
        place(top + left, dx: 105mm, dy: -40mm, vcci-ring(250mm))
        place(top + left, dx: 22mm, dy: 20mm, rect(width: 16mm, height: 0.9mm, fill: VCCI.gold, stroke: none))
        place(top + left, dx: 22mm, dy: 27mm, block(width: 120mm, {
          set text(fill: white, size: 9pt)
          if date != none or version != none {
            text(weight: 600, size: 10pt, [#date#if version != none [ · #L("version") #version]])
          }
          if client != none { block(above: 3mm, text(fill: white.transparentize(18%), [#L("client"): #client])) }
          if authors != none and authors != () {
            block(above: 2mm, text(fill: white.transparentize(18%), authors.map(a => a.name).join(", ")))
          }
        }))
        if hero != none { place(top + left, dx: 22mm, dy: 80mm, vcci-hero(hero, variant: "gold", size: 22mm)) }
      }))
    })
    // imprint page: who the report is for, who made it, how to cite it
    page(header: none, footer: none, numbering: none, {
      set text(size: 8.5pt)
      align(bottom, block(width: 120mm, {
        let row(k, v) = if v != none { block(above: 3.5mm, { vcci-label(k, fill: VCCI.slate); linebreak(); v }) }
        row(L("report"), title)
        row(L("client"), client)
        row(L("team"), if team != none { team } else if authors != none and authors != () {
          authors.map(a => if a.affiliation != [] [#a.name (#a.affiliation)] else [#a.name]).join([; ]) })
        row(L("version"), if version != none or date != none [#if version != none [#version · ]#date])
        row(L("citation"), citation)
        row(L("disclaimer"), disclaimer)
        block(above: 6mm, text(fill: VCCI.slate, [© #if year != none [#year ]#L("org") (VCCI)]))
      }))
    })
    counter(page).update(1)
  }

  if abstract != none { vcci-callout(title: if abstract-title != none { abstract-title } else { L("abstract") }, abstract) }
  if toc {
    outline(title: if toc_title == none { L("contents") } else { toc_title }, depth: toc_depth, indent: 4mm)
  }

  doc

  [#metadata(none) <vcci-report-end>]

  // ------------------------------------------------ back cover
  if back-cover {
    page(margin: 0mm, header: none, footer: none, background: none, numbering: none, fill: VCCI.blue, {
      place(top + left, rect(width: 100%, height: 100%, fill: VCCI-COVER-BLUE, stroke: none))
      place(top + left, dx: -40mm, dy: -60mm, vcci-ring(300mm))
      place(top + left, dx: 22mm, dy: 200mm, block(width: 166mm, height: 70mm, fill: VCCI.paper, radius: 1mm,
        inset: (x: 10mm, y: 10mm), {
          vcci-logo(width: 62mm)
          v(6mm)
          text(weight: 600, size: 9pt, fill: VCCI.blue, L("org"))
          v(1mm)
          text(size: 8pt, fill: VCCI.slate, if contact != none { contact } else { VCCI-CONTACT })
        }))
    })
  }
}
