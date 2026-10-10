# quarto-vcci

Extension Quarto cho tài liệu của Liên đoàn Thương mại và Công nghiệp Việt Nam (VCCI). Có ba định dạng: báo cáo tư vấn (`vcci-report`), working paper (`vcci-wp`) và tờ trình (`vcci-memo`). Mỗi định dạng xuất PDF bằng Typst (bản chính, khổ A4) và Word (để đồng nghiệp sửa), theo Bộ nhận diện thương hiệu VCCI. Kèm theo là theme biểu đồ cho Python (matplotlib), R (ggplot2) và Stata.

*English: Quarto formats for VCCI (Vietnam Chamber of Commerce and Industry) consulting reports, working papers and memos, rendered to PDF (Typst, A4) and Word, with chart themes for matplotlib, ggplot2 and Stata. Documentation is in Vietnamese; every format also supports `lang: en`.*

Phiên bản {{VERSION}}. Cần Quarto ≥ 1.6 (đã có sẵn Typst). Font Lora, Be Vietnam Pro và JetBrains Mono đi kèm extension, nên không cần cài font.

## Cài đặt

Tạo dự án mới từ mẫu, gồm extension, tài liệu mẫu và theme biểu đồ:

```bash
quarto use template trongtrd/quarto-vcci
```

Lệnh trên tạo các file sau:

| File | Nội dung |
|---|---|
| `<tên-thư-mục>.qmd` | Báo cáo tư vấn mẫu (`vcci-report`) |
| `wp.qmd`, `references.bib` | Working paper mẫu (`vcci-wp`) |
| `memo.qmd` | Tờ trình mẫu (`vcci-memo`) |
| `charts.qmd` | Báo cáo có biểu đồ ggplot2 (cần R) |
| `charts/` | Theme biểu đồ cho matplotlib, ggplot2, Stata |
| `_extensions/trongtrd/` | Extension (ba định dạng) |

Chỉ thêm extension vào một dự án đã có:

```bash
quarto add trongtrd/quarto-vcci
```

Ghim một phiên bản: `quarto use template trongtrd/quarto-vcci@v{{VERSION}}`. Cập nhật extension: chạy lại `quarto add trongtrd/quarto-vcci`.

Dựng tài liệu:

```bash
quarto render ten-tai-lieu.qmd
```

Mỗi mẫu khai báo cả hai đầu ra (`vcci-report-typst` cho PDF, `vcci-report-docx` cho Word). Chỉ dựng một đầu ra: `quarto render ten-tai-lieu.qmd --to vcci-report-typst`.

