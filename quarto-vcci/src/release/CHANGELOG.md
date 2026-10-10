# Thay đổi

Đánh số theo [SemVer](https://semver.org/lang/vi/): bản vá (1.0.x) sửa lỗi, không đổi bố cục; bản phụ (1.x.0) thêm tùy chọn hoặc định dạng; bản chính (x.0.0) đổi khóa YAML hoặc bố cục.

## 1.0.0 (10/10/2026)

Bản phát hành đầu tiên.

- Ba định dạng, mỗi định dạng có PDF (Typst) và Word:
  - `vcci-report`: báo cáo tư vấn có bìa, trang thông tin, mục lục và bìa sau;
  - `vcci-wp`: working paper có số hiệu, tóm tắt song ngữ, mã JEL, APA;
  - `vcci-memo`: tờ trình.
- Báo cáo và tờ trình trích dẫn kiểu Chicago chú thích cuối trang; working paper dùng APA.
- Khối `lead`, `figures`, `highlight`, `label`; hộp `callout` theo màu trạng thái VCCI; dấu "Bản thảo"/"Mật".
- Font Lora, Be Vietnam Pro, JetBrains Mono đi kèm; tô cú pháp theo màu VCCI.
- Theme biểu đồ cho matplotlib, ggplot2 và Stata.
- Tiếng Việt mặc định; `lang: en` cho tài liệu tiếng Anh.
