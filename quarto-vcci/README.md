# quarto-vcci (đang phát triển)

Extension Quarto cho tài liệu VCCI: báo cáo tư vấn (`vcci-report`), working paper (`vcci-wp`), memo (`vcci-memo`). Mỗi định dạng xuất PDF bằng Typst (bản chính) và Word. Kế hoạch: [`docs/PLAN_QUARTO_VCCI.md`](../docs/PLAN_QUARTO_VCCI.md).

Trạng thái: bước 1 (nền dùng chung và bộ kiểm thử) đã xong. `vcci-report` mới là bộ khung; bìa, mở chương và bìa sau làm ở bước 2.

## Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `src/shared/vcci.typ` | Lớp Typst dùng chung: trang, chữ, tiêu đề, bảng, chú thích, logo, gạch vàng, nhãn, đoạn dẫn, hộp nhấn mạnh |
| `src/shared/vcci.lua` | Bộ lọc khối `::: lead`, `::: highlight`, `::: label` cho Typst và Word |
| `src/formats/<định dạng>/` | `_extension.yml`, `template.typ`, `typst-show.typ` của từng định dạng |
| `_extensions/vcci/<định dạng>/` | **Sinh tự động** bằng `build.py`; không sửa tay |
| `tests/fixtures/` | Tài liệu thử; khai báo kiểm tra trong khóa `test:` của YAML |
| `tests/selftest/` | Tài liệu cố tình lỗi, để chứng minh bộ kiểm thử bắt được lỗi |

`build.py` lấy màu, font, logo từ `brand-assets/` và file Word mẫu từ `VCCI_Report.dotx`. Mỗi extension tự chứa đủ (Quarto không cho các extension dùng chung file), nên phần dùng chung được chép vào từng extension. Logo được nhúng thẳng vào mã Typst, nên không chép file nào vào thư mục của người dùng.

## Lệnh

Chạy từ thư mục gốc repo:

```bash
python quarto-vcci/build.py
```

```bash
python quarto-vcci/tests/run_tests.py
```

`build.py --check` báo lỗi nếu `_extensions/` lệch với nguồn. `run_tests.py` dựng mọi tài liệu thử trong thư mục sạch, ở chế độ bỏ qua font hệ thống (giống máy chưa cài font), rồi kiểm tra:

1. Extension khớp nguồn và `brand-tokens.json`.
2. Dựng thành công, không có cảnh báo nào.
3. PDF: chỉ font thương hiệu và đều được nhúng; khổ A4; số trang trong khoảng; đủ câu tiếng Việt yêu cầu; không chữ nào sát mép giấy hay tràn lề hai bên.
4. Word: mọi style đều được định nghĩa; bảng dùng style VCCI Table; không gán font trực tiếp ngoài bộ nhận diện; font được nhúng; đủ câu tiếng Việt yêu cầu.

Sau đó bộ kiểm thử chạy các tài liệu trong `tests/selftest/` và chỉ đạt khi mỗi lỗi cố tình bị đúng kiểm tra tương ứng bắt được. Kết quả nằm ở `tests/out/summary.md` (kèm PDF, DOCX và ảnh từng trang).

Cần: Quarto ≥ 1.6 (có sẵn Typst), Python 3 với PyYAML, Poppler (`pdffonts`, `pdfinfo`, `pdftotext`, `pdftoppm`).
