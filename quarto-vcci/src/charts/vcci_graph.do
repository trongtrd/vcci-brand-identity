* VCCI charts for Stata: brand scheme, fonts and the Vietnamese decimal comma.
*
*   do vcci_graph.do          Vietnamese: 2,5 (decimal comma)
*   do vcci_graph.do en       English: 2.5
*
* Needs scheme-vcci.scheme in the same folder (or anywhere on the adopath) and the fonts Lora and Be Vietnam Pro
* installed (brand-assets/03_Fonts). A scheme cannot choose fonts, so this file does.
* Brand guide, section 08: at most six series, in the scheme's order; Drum Gold ($VCCI_GOLD) only marks one value
* and always carries its label; bar and column axes start at zero; label series directly; cite the source under every
* chart:  note("Nguồn: VCCI, Khảo sát PCI 2025").
* Titles in Lora:  title("{fontface \"$VCCI_DISPLAY\":Năm 2025 đạt điểm cao nhất}")
* Value labels in Lora:  graph bar ..., blabel(bar, format(%4,1f))   (the scheme sets their colour)

args lang

set scheme vcci
graph set window fontface "{{TEXT-FONT}}"
graph set svg fontface "{{TEXT-FONT}}"
graph set ps fontface "{{TEXT-FONT}}"
graph set eps fontface "{{TEXT-FONT}}"

* decimal comma in tables and in graph labels that use a default (%g) format
if "`lang'" == "en" set dp period
else set dp comma

{{STATA-GLOBALS}}
