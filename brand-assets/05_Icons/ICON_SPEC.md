# VCCI Icon System v1

Status: Version 1.0. Direction A and the complete 48 UI / 24 hero icon set approved by the project owner on 2026-10-05.

## Scope and construction

48 UI icons and 24 original hero icons. UI uses the supplied 24 px grid, a 20 × 20 live area, 2 px padding and 1.6 px strokes. Hero uses the supplied 64 px grid, a 56 × 56 live area, 4 px padding and 2 px strokes. Padding includes the painted stroke. All caps and joins are round. Geometry is authored or adapted as explicit SVG paths and basic shapes; no raster tracing. Presentation attributes only; no transforms, text, fonts, CSS or embedded images in icon SVGs. Coordinates use at most two decimal places.

## Color and variants

- UI currentColor masters inherit CSS text color when inlined; standalone consumers should use the explicit color variants. Blue #264896 is for Paper #FBF9F4/light backgrounds. Gold #FFCD00 and White #FFFFFF are for VCCI Blue #264896 or Deep Navy #0B1A4F.
- Hero Blue-Gold: blue line with one flat gold shape behind the linework. Each accent occupies at most 25% of the 56 × 56 live area (a stricter denominator than the full canvas).
- Hero Blue: blue line only. Gold-on-dark: gold line only, no accent. White: white line only, no accent. No Blue Tint accent in v1, per owner agreement.
- No gradients, shadows, opacity effects or additional stroke weights.
- Accent is optional in use: use the line-only variant in dense compositions to avoid multiple competing gold gestures.

## Use and accessibility

UI is designed for 24 px display; hero for 48 px and larger. Hero 24 px is a stress check and is not the recommended use size. Scale uniformly without non-scaling-stroke. Use Blue or Blue-Gold on Paper and Gold or White on dark backgrounds. Do not use Gold or White on Paper, or Blue on VCCI Blue.

Hero icons require a visible label on first use and in navigation unless an adjacent title already conveys the topic. Supply accessible names in the host application; hide decorative duplicates from assistive technology. Do not rely on an icon alone to convey unfamiliar policy concepts or status.

## Meaning boundaries

Local Economic Governance means provincial economic administration and responsiveness to business, not a national/state institution. Green Transition means enterprise environmental transition, not the full ESG agenda. Legislative Input means consultation and contribution to lawmaking, not arbitration. Administrative Reform means reducing procedural complexity. Business Environment Reform refers to enabling business access and removing obstacles. Private Sector Development represents independent businesses and is not a startup-only category.

## Do and do not

Keep proportions, approved colors, clear space and stroke rules. Use labels to distinguish related abstract concepts. Never insert the VCCI logo, drum medallion, flags, state/national emblems or mourning imagery. Never replace geometry with traced image-generation output. Never enclose all icons in a new badge or add ornamental rays. Gold is a controlled accent, not a background flood.

## Exports

UI transparent PNG: 48 and 96 px, Blue/Gold/White. Hero transparent PNG: 256 and 512 px, Blue-Gold/Blue/Gold-on-dark/White. Contact sheets are for review, not icon extraction. Retain SVGs as masters. The approved raster exploration is Sheets/VCCI_Hero_Concepts.png.

## Verification

All icons and explicit color variants are rendered at 24, 48 and 128 px on Paper and VCCI Blue for inspection. Appropriate light/dark pairings are separately assembled into QA sheets. Hero contact sheet additionally uses Deep Navy. Machine checks cover XML validity, allowed elements, stroke consistency, painted live-area bounds, accent count/area, file size, export dimensions and transparent PNG alpha. QA evidence is kept outside the delivery folder.

## Release verification

The approved release contains 288 SVGs and 480 transparent icon PNGs. Automated checks passed with no errors; the largest SVG is 831 bytes and the largest hero accent occupies 8.11% of the live area. Every icon was visually checked at 24, 48 and 128 px on Paper and VCCI Blue. Hero contact sheets also show Deep Navy.
