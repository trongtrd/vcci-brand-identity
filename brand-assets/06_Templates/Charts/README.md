# Theme biểu đồ VCCI: matplotlib, ggplot2, Stata

Biểu đồ vẽ bằng Python, R hay Stata có cùng màu, chữ và đường nét theo phần 08 "Dữ liệu và biểu đồ" của hướng dẫn thương hiệu. Các file trong thư mục này được `quarto-vcci/build.py` sinh từ `brand-assets/brand-tokens.json`; muốn sửa thì sửa nguồn trong `quarto-vcci/src/charts/`, đừng sửa bản sinh ra.

| File | Công cụ | Cần |
|---|---|---|
| `vcci_charts.py`, `vcci.mplstyle` | Python | matplotlib ≥ 3.6 |
| `theme_vcci.R` | R | ggplot2 ≥ 3.5 (bản 4.0 tự đặt màu mặc định cho mọi biểu đồ), scales, systemfonts; svglite hoặc ragg để xuất file |
| `scheme-vcci.scheme`, `vcci_graph.do` | Stata | Stata 18 trở lên |

**Font.** Cài Lora và Be Vietnam Pro từ `brand-assets/03_Fonts`. Nếu chưa cài, Python và R tự tìm font trong extension Quarto (thư mục `fonts` trong `_extensions/`) hoặc trong `brand-assets/03_Fonts`, ở thư mục làm việc và tối đa bốn cấp phía trên. Stata chỉ dùng font đã cài.

**Cách dùng chung.** Chép các file của công cụ mình dùng vào cạnh file mã hoặc tài liệu Quarto. Mặc định số viết theo tiếng Việt: 2,5 và 12.500. Bài tiếng Anh chọn `"en"`.

## Python (matplotlib)

```python
import matplotlib.pyplot as plt
import vcci_charts as vcci

vcci.use()                                   # vcci.use("en") cho bài tiếng Anh
fig, ax = plt.subplots()
bars = ax.bar(["2023", "2024", "2025"], [64.8, 66.0, 67.4], width=0.62)
vcci.highlight(bars, -1)                     # một cột vàng, kèm nhãn số
ax.set_ylim(0, 80)
vcci.title(ax, "Năm 2025 đạt điểm cao nhất")
vcci.source(fig, "Nguồn: VCCI, Khảo sát PCI 2025")
fig.savefig("diem-pci.svg")
```

Các hàm khác: `vcci.label(ax, bars)` (nhãn số Lora màu xanh), `vcci.line_labels(ax)` (ghi tên ở cuối mỗi đường thay chú giải), `vcci.legend(ax)` (chú giải một hàng dưới tiêu đề), `vcci.number(x)` (viết số kiểu Việt Nam). Bảng màu: `cmap="vcci_seq"` (bảy lớp) hoặc `"vcci_seq_c"` cho giá trị có thứ tự; `"vcci_div"`, `"vcci_div_c"` cho giá trị quanh một mốc.

## R (ggplot2)

```r
library(ggplot2)
source("theme_vcci.R", encoding = "UTF-8")
vcci_setup()                                 # vcci_setup("en") cho bài tiếng Anh
d <- data.frame(year = 2023:2025, score = c(64.8, 66.0, 67.4))
p <- ggplot(d, aes(factor(year), score, fill = vcci_highlight(year == 2025))) +
  geom_col(width = 0.62) + scale_fill_identity() +
  geom_text(data = subset(d, year == 2025), aes(label = label_vcci(accuracy = 0.1)(score)), vjust = -0.6) +
  scale_y_continuous(limits = c(0, 80), expand = c(0, 0)) +
  labs(x = NULL, y = NULL, title = "Năm 2025 đạt điểm cao nhất", caption = "Nguồn: VCCI, Khảo sát PCI 2025")
ggsave("diem-pci.svg", p, width = 6.5, height = 3.6)
```

`vcci_setup()` đặt `theme_vcci()` làm mặc định. Thang màu: `scale_colour_vcci()`, `scale_fill_vcci()` (chuỗi), `scale_fill_vcci_seq()` và `_seq_c()` (có thứ tự), `scale_fill_vcci_div()` và `_div_c()` (quanh một mốc). Số: `label_vcci()`, `label_vcci_percent()`. Trong Quarto, `vcci_setup()` tự chọn SVG cho bản PDF và PNG 300 dpi cho bản Word; xem mẫu `quarto-vcci/templates/charts.qmd`.

Tiêu đề trong biểu đồ ggplot dùng Lora Regular, vì SVG của svglite không ghi được độ đậm Medium. Trong báo cáo, chú thích hình (`fig-cap`) thường thay cho tiêu đề này.

## Stata

```stata
do vcci_graph.do                             // do vcci_graph.do en  cho bài tiếng Anh
sysuse auto, clear
graph bar mpg, over(foreign) blabel(bar, format(%4,1f)) ///
    title(`"{fontface "$VCCI_DISPLAY":Xe nhập khẩu tiết kiệm nhiên liệu hơn}"') ///
    note("Nguồn: Stata, bộ số liệu auto")
graph export "mpg.svg", replace
```

`vcci_graph.do` chọn scheme `vcci`, đặt font Be Vietnam Pro (scheme của Stata không chọn được font) và dấu phẩy thập phân (`set dp comma`). Màu dùng riêng: `$VCCI_GOLD` (nhấn một giá trị), `$VCCI_BLUE`, `$VCCI_MUTED`, `$VCCI_S1`…`$VCCI_S6` (màu chuỗi), `$VCCI_SEQ1`…`7`, `$VCCI_DIV1`…`7`. Tiêu đề dùng Lora nhờ `{fontface "$VCCI_DISPLAY":…}`. Định dạng số kiểu Việt Nam: `%4,1f`.

## Quy tắc (phần 08 của hướng dẫn)

- Tối đa sáu chuỗi, theo thứ tự VCCI Blue, Sky, Drum Bronze, Slate, Bronze 20, Deep Navy. Nhiều hơn thì gộp nhóm nhỏ hoặc tách thành nhiều biểu đồ nhỏ.
- Vàng không phải màu chuỗi: chỉ nhấn một giá trị, luôn kèm nhãn số.
- Trục cột bắt đầu từ 0. Không 3D, không bóng đổ, không trong suốt, không chuyển màu.
- Ghi tên chuỗi trực tiếp khi được; ghi nguồn dưới mỗi biểu đồ.
- Không dùng màu trạng thái (đỏ, xanh lá) làm màu chuỗi.
