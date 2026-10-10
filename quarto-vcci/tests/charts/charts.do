* Sample charts with the VCCI Stata scheme:  StataMP-64.exe /e do charts.do OUTDIR CHARTS_DIR DATA_DIR
* Writes stata-<chart>.svg for the chart checks in run_tests.py (layer 8). The same charts are drawn in Python and R
* (no heat map: Stata has no built-in one).
args outdir chartsdir datadir
version 18
cd "`outdir'"
adopath ++ "`chartsdir'"
do "`chartsdir'/vcci_graph.do"
local src "Nguồn: VCCI · Số liệu minh họa"
local T `"{fontface "$VCCI_DISPLAY":"'

* column chart, one value highlighted in gold with its label
import delimited using "`datadir'/bar.csv", encoding(utf-8) clear
gen lbl = "{fontface " + char(34) + "$VCCI_DISPLAY" + char(34) + ":" + string(score, "%4,1f") + "}"
twoway (bar score year if year < 2025, barwidth(0.62) color("$VCCI_BLUE")) ///
       (bar score year if year == 2025, barwidth(0.62) color("$VCCI_GOLD")) ///
       (scatter score year if year == 2025, msymbol(none) mlabel(lbl) mlabposition(12) mlabcolor("$VCCI_BLUE") mlabsize(medsmall)), ///
       ylabel(0(10)80) yscale(range(0 80)) xlabel(2020(1)2025) xtitle("") ytitle("") legend(off) ///
       title(`"`T'Năm 2025 đạt điểm cao nhất trong sáu năm}"') note("`src'")
graph export "stata-bar.svg", replace

* three lines, named at their ends
import delimited using "`datadir'/line.csv", encoding(utf-8) clear
gen k = 1 if city == "Hà Nội"
replace k = 2 if city == "TP.HCM"
replace k = 3 if city == "Đà Nẵng"
separate score, by(k)
twoway (line score1 score2 score3 year) ///
       (scatter score year if year == 2025 & k == 1, msymbol(none) mlabel(city) mlabcolor("$VCCI_S1") mlabsize(small)) ///
       (scatter score year if year == 2025 & k == 2, msymbol(none) mlabel(city) mlabcolor("$VCCI_SEQ5") mlabsize(small)) ///
       (scatter score year if year == 2025 & k == 3, msymbol(none) mlabel(city) mlabcolor("$VCCI_S3") mlabsize(small)), ///
       ylabel(55(2.5)75, format(%4,1f)) xlabel(2020(1)2025) xscale(range(2020 2025.8)) xtitle("") ytitle("") legend(off) ///
       title(`"`T'Hà Nội vượt TP.HCM và Đà Nẵng từ năm 2024}"') note("`src'")
graph export "stata-line.svg", replace

* stacked horizontal bars (shares), values on the segments
import delimited using "`datadir'/stack.csv", encoding(utf-8) clear
gen g = 1 if group == "Doanh nghiệp nhỏ"
replace g = 2 if group == "Doanh nghiệp vừa"
replace g = 3 if group == "Doanh nghiệp lớn"
graph hbar share, over(order, relabel(1 "Tốt" 2 "Khá" 3 "Trung bình" 4 "Kém")) over(group, sort(g)) asyvars stack ///
      bar(1, color("$VCCI_S1")) bar(2, color("$VCCI_S2")) bar(3, color("$VCCI_S3")) bar(4, color("$VCCI_S4")) ///
      blabel(bar, position(center) color(white) format(%2.0f) size(small)) ytitle("") yscale(off) ylabel(, nogrid) ///
      title(`"`T'Doanh nghiệp nhỏ đánh giá tích cực hơn (%)}"') note("`src'")
graph export "stata-stack.svg", replace

* scatter, two groups
import delimited using "`datadir'/scatter.csv", encoding(utf-8) clear
twoway (scatter cost employees if sector == "Sản xuất") (scatter cost employees if sector == "Dịch vụ"), ///
       legend(order(1 "Sản xuất" 2 "Dịch vụ")) ylabel(0(1)5) xtitle("Số lao động") ytitle("Chi phí không chính thức (% doanh thu)") ///
       title(`"`T'Chi phí không chính thức tăng theo quy mô}"') note("`src'")
graph export "stata-scatter.svg", replace

* six series: the full series order
import delimited using "`datadir'/series6.csv", encoding(utf-8) clear
separate value, by(order)
local labels
forvalues i = 1/6 {
    local labels `labels' (scatter value year if year == 2025 & order == `i', msymbol(none) mlabel(sector) mlabcolor("${VCCI_S`i'}") mlabsize(small))
}
twoway (line value1-value6 year) `labels', xlabel(2020(1)2025) xscale(range(2020 2025.9)) xtitle("") ytitle("") legend(off) ///
       title(`"`T'Sáu ngành theo thứ tự màu chuỗi}"') note("`src'")
graph export "stata-series6.svg", replace
