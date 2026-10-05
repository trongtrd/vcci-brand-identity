# HANDOFF — Step 2: VCCI Icon System v1

**From:** Claude (brand system lead, steps 1, 3, 4) · **To:** ChatGPT agent (step 2) · **Date:** 2026-10-05
**Client:** VCCI — Liên đoàn Thương mại và Công nghiệp Việt Nam / Vietnam Chamber of Commerce and Industry
**Project owner:** the person who sends you this pack. They make the final decisions.

---

## 1. Why this matters

We are building a brand identity system for VCCI that will be applied to all of its future documents, reports, events and digital channels. VCCI is Vietnam's national chamber of commerce (founded in Hà Nội in 1963). It represents and advocates for Vietnamese enterprises, issues Certificates of Origin, promotes trade and investment, runs business forums, and publishes research such as the PCI index.

The brand must read as **authoritative, trusted, enduring and proud, but a partner rather than a bureaucracy.** Think premium institutional, editorial and calm. It must not look like a startup, a tech company or a Canva template.

Your job is the **icon system**. The next steps depend on it: Claude will build MS Word and PowerPoint templates (step 3) and the full brand guidelines document (step 4) using your icons.

## 2. What is already done (do not change)

| Area | Status | Where |
|---|---|---|
| Logo | Vector master decoded from the client's CorelDRAW file. Lockups, logo on a light plate, PNG/PDF/SVG exports. | `reference/VCCI_Logo_Primary.svg` |
| Colour | Locked (see below). | `reference/VCCI_Colours.json` |
| Typography | Lora (display serif) + Be Vietnam Pro (text sans). | `reference/brand-tokens.json` |
| Graphic motifs | Drum-ring line art, 14-ray "Radiance" star, C-arc pattern, drum-dot field. | `reference/*.svg` |
| Brand board | One-page summary of the whole system. | `reference/VCCI_Brand_Board_preview.jpg` |
| Interim icons | 12 placeholder line icons. Use them as a style starting point, not as the final set. | `reference/interim-icons/` |

### Locked colours

| Name | HEX | Use in icons |
|---|---|---|
| VCCI Blue | `#264896` | Default stroke on light backgrounds |
| Drum Gold | `#FFCD00` | Stroke on blue/dark backgrounds; optional single accent fill in hero icons |
| Drum Bronze | `#CC713C` | Hero accent only (sparingly) |
| Deep Navy | `#0B1A4F` | Dark background for testing |
| Paper | `#FBF9F4` | Default light background for testing |
| White | `#FFFFFF` | Stroke variant for blue/dark backgrounds |

### Non-negotiable brand rules that affect icons

1. **Never use the VCCI logo, or the bronze-drum medallion from the logo, as an icon or inside an icon.** The client has explicitly rejected "symbol-only" use of the drum.
2. **Cultural rule:** the client rejected any all-white version of the logo (in Vietnamese culture, all-white has mourning connotations in this context). White icon *variants* for dark backgrounds are fine, because they are not the logo. Do not design anything that looks like a white logo.
3. Avoid imagery with funeral or mourning connotations: incense, white chrysanthemums, mourning headbands, altars. Also avoid political or state symbols that VCCI does not own: the national emblem, the flag, the star-on-red, the hammer and sickle.
4. One gold gesture per composition. Gold is a signature, not a flood.

## 3. Scope: two tiers (structure inspired by a leading university's system)

### Tier A — UI icons (small, functional): about 48 icons

- **Base:** use **Lucide** (https://lucide.dev, ISC licence, commercial use allowed). Select and, where necessary, lightly adapt icons so the set is consistent. Do **not** copy icons from any other organisation's brand kit.
- **Grid:** `viewBox="0 0 24 24"`, 2 px live-area padding (template: `templates/VCCI_UI-Icon_Grid_24.svg`).
- **Stroke:** `stroke-width="1.6"`, `stroke-linecap="round"`, `stroke-linejoin="round"`, `fill="none"`. Strokes only.
- **Colour:** the master files use `stroke="currentColor"`. Coloured exports are listed in section 4.
- **Suggested list** (adjust if needed, keep it at about 48):
  home, menu, close, search, filter, settings, arrow-right, arrow-left, chevron-down, external-link, download, upload, share, print, calendar, clock, map-pin, phone, mail, globe, user, users, user-plus, lock, info, alert-triangle, check, check-circle, file, file-text, file-check, folder, newspaper, presentation, video, mic, image, bar-chart, line-chart, pie-chart, briefcase, building, landmark, factory, ship, handshake, scale, award.

### Tier B — Hero icons (illustrative, distinctively VCCI): 20 icons

These carry the brand. They are **original designs** in a **single-weight line style** that matches the interim icons and the drum-ring motifs.

- **Grid:** `viewBox="0 0 64 64"`, 4 px padding (template: `templates/VCCI_Hero-Icon_Grid_64.svg`).
- **Stroke:** `stroke-width="2"`, round caps and joins, one weight only throughout.
- **Accent (optional):** at most **one** flat fill shape per icon, in Drum Gold (or Drum Bronze on a light background), covering **≤ 25 %** of the icon area. The accent sits *behind* the linework, for example an offset circle or tile. No gradients.
- **Motif DNA (subtle, optional):** the 14-ray star, concentric rings or the C-arc (a ring cut at +0.35R with inner radius 0.6R) may appear as a quiet structural element in a few icons, for example a sun motif in "Sustainability". **Never the drum medallion itself.**
- **Themes** (Vietnamese label / English slug):

| # | Theme | Slug |
|---|---|---|
| 01 | Hội viên | membership |
| 02 | Chứng nhận xuất xứ (C/O) | certificate-of-origin |
| 03 | Xúc tiến thương mại | trade-promotion |
| 04 | Hội chợ, triển lãm | trade-fair |
| 05 | Thu hút đầu tư | investment |
| 06 | Đối thoại chính sách | policy-dialogue |
| 07 | Pháp lý và cải cách thể chế | law-reform |
| 08 | Trọng tài thương mại | arbitration |
| 09 | Đào tạo, nâng cao năng lực | training |
| 10 | Phát triển bền vững (ESG) | sustainability |
| 11 | Chuyển đổi số | digital-transformation |
| 12 | Doanh nghiệp nhỏ và vừa | sme |
| 13 | Hội nhập quốc tế / FTA | international-integration |
| 14 | Xuất khẩu và logistics | export-logistics |
| 15 | Diễn đàn, sự kiện | forum-events |
| 16 | Nghiên cứu, khảo sát (PCI) | research-index |
| 17 | Doanh nhân, khởi nghiệp | entrepreneurship |
| 18 | Người sử dụng lao động, quan hệ lao động | employers-labour |
| 19 | Kết nối, đối tác | networking-partnership |
| 20 | Tư vấn, hỗ trợ doanh nghiệp | business-advisory |

## 4. How to use image generation (important)

GPT Image produces **raster** images. The deliverable must be **clean, hand-authored vector SVG.** Please work like this:

1. **Explore:** use image generation for concept sheets and moodboards of the 20 hero icons (two or three directions). Show these to the project owner and let them pick a direction before you finalise.
2. **Build:** author the final icons as SVG geometry (`path`, `circle`, `line`, `rect`) on the grid templates. **Do not auto-trace raster images**: tracing produces uneven, multi-weight, noisy paths that fail the criteria below.
3. **Verify:** render each SVG at 24 px, 48 px and 128 px on Paper (`#FBF9F4`) and on VCCI Blue (`#264896`), and visually check every icon. Fix anything that is illegible at its target size.

## 5. Deliverables

Return **one zip**, `VCCI_Icons_v1.zip`, structured like this:

```
05_Icons/
  UI/
    SVG/currentColor/VCCI_UI_<slug>.svg      ← masters
    SVG/Blue/  SVG/Gold/  SVG/White/          ← stroke set to #264896 / #FFCD00 / #FFFFFF
    PNG/Blue|Gold|White/VCCI_UI_<slug>_48px.png and _96px.png (transparent)
  Hero/
    SVG/Blue-Gold/VCCI_Hero_<nn>_<slug>.svg   ← master: Blue line + Gold accent (for light backgrounds)
    SVG/Blue/                                  ← line only, no accent
    SVG/Gold-on-dark/                          ← Gold line, accent in Blue Tint #E7ECF6 or omitted (for blue/dark backgrounds)
    SVG/White/                                 ← White line, no accent (for blue/dark backgrounds)
    PNG/<same variants>/VCCI_Hero_<nn>_<slug>_256px.png and _512px.png (transparent)
  Sheets/
    VCCI_UI_ContactSheet.png        ← all UI icons, labelled, on Paper and on Blue
    VCCI_Hero_ContactSheet.png      ← all hero icons, labelled VN + EN, on Paper and on Deep Navy
    VCCI_Hero_Concepts.png          ← the image-gen exploration the owner approved
  ICON_SPEC.md                      ← grid, stroke, padding, colour, accent rules, do/don't (feeds step 4)
  LICENSES.md                       ← Lucide ISC attribution and list of modified icons; statement that hero icons are original
  HANDBACK_TO_CLAUDE.md             ← see section 7
```

## 6. Acceptance criteria (Claude will check these on intake)

- [ ] Valid standalone SVG; correct `viewBox` (24 or 64); no `<image>`, no raster data, no `<text>`, no embedded fonts.
- [ ] No `transform` attributes left on paths (flatten them). No inline styles or classes; presentation attributes only.
- [ ] Single stroke weight per tier (UI 1.6, Hero 2), round caps and joins; strokes do not visually merge into heavier blobs.
- [ ] Geometry stays inside the live area; optical sizes are balanced across the set (a circle icon does not look smaller than a square one).
- [ ] Hero accent: at most one shape, ≤ 25 % of the area, Gold or Bronze only.
- [ ] Legible at 24 px (UI) and 48 px (hero), on both Paper and VCCI Blue.
- [ ] No logo, no drum medallion, no national or state symbols, no mourning imagery, no copied third-party brand icons.
- [ ] File names exactly as specified (lowercase kebab-case slugs).
- [ ] Each SVG under 4 KB where possible (optimised, e.g. SVGO-style precision of 2 decimals).

## 7. Handing back to Claude

Include `HANDBACK_TO_CLAUDE.md` with:
1. The final icon lists (UI and hero) with VN and EN names.
2. Any deviations from this brief and why.
3. The direction the project owner approved (one paragraph and a reference to the concepts sheet).
4. Known issues or icons the owner wants to revisit.
5. Suggested pairings for templates, for example which hero icon fits which report type.

## 8. Reference files in this pack

- `reference/VCCI_Brand_Board_preview.jpg`: the whole brand on one board. **Look at this first.**
- `reference/VCCI_Logo_Primary.svg` and `_1200px.png`: logo, for visual context only.
- `reference/VCCI_Colours.json`, `reference/brand-tokens.json`: the exact system values.
- `reference/VCCI_Drum-Ring_Line_Transparent_Blue.svg`, `reference/VCCI_Radiance-14_Blue.svg`: the motif DNA.
- `reference/interim-icons/`: the current 12-icon style (24 px, stroke 1.6).
- `templates/`: 24 px and 64 px keyline grids.

If anything in this brief conflicts with what the project owner tells you, **the project owner wins.** Note the change in `HANDBACK_TO_CLAUDE.md`.
