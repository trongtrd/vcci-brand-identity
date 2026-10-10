# quarto-vcci (đang phát triển)

Extension Quarto cho tài liệu VCCI: báo cáo tư vấn (`vcci-report`), working paper (`vcci-wp`), memo (`vcci-memo`). Mỗi định dạng xuất PDF bằng Typst (bản chính) và Word (để đồng nghiệp sửa). Kế hoạch: [`docs/PLAN_QUARTO_VCCI.md`](../docs/PLAN_QUARTO_VCCI.md).

Trạng thái: `vcci-report` đã xong và được duyệt (bước 2, 10/10/2026). `vcci-wp` và `vcci-memo` làm ở bước 3 và 4.

## Dùng `vcci-report`

Cài extension vào thư mục dự án (khi đã phát hành lên GitHub sẽ dùng `quarto use template`):

```bash
quarto add <đường-dẫn-tới>/quarto-vcci --no-prompt
```

Chép `templates/report.qmd` làm điểm bắt đầu, rồi dựng:

```bash
quarto render report.qmd
```

Bản mẫu đã dựng: [`examples/report.pdf`](examples/report.pdf) và [`examples/report.docx`](examples/report.docx).

### Thông tin trong YAML

| Khóa | Ý nghĩa | Hiện ở |
|---|---|---|
| `title`, `subtitle` | Tiêu đề, phụ đề | Bìa, trang thông tin |
| `report-label` | Nhãn trên tiêu đề, mặc định "Báo cáo" (ví dụ "Báo cáo tư vấn") | Bìa |
| `short-title` | Tên rút gọn | Đầu trang |
| `client` | Bên đặt hàng | Bìa, trang thông tin |
| `author` (kèm `affiliations`), `team` | Tác giả; `team` thay danh sách nhóm thực hiện nếu cần | Bìa, trang thông tin |
| `date`, `version` | Ngày ("10 tháng 10 năm 2026"), phiên bản | Bìa, trang thông tin |
| `status` | Ví dụ "Bản thảo", "Mật": nhãn trên bìa và dấu chìm mọi trang. Bỏ khi phát hành | Bìa, mọi trang |
| `hero` | Hero icon trên bìa, số 1–24 (xem `brand-assets/05_Icons`) | Bìa |
| `citation-text` | Gợi ý trích dẫn (khóa `citation` đã được Quarto dùng) | Trang thông tin |
| `disclaimer` | Lưu ý, miễn trừ | Trang thông tin |
| `contact` | Thay địa chỉ liên hệ mặc định của VCCI | Bìa sau |
| `cover: false`, `back-cover: false` | Bỏ bìa trước (cùng trang thông tin) hoặc bìa sau | |
| `toc: true` | Mục lục | Sau trang thông tin |
| `bibliography` | Tài liệu tham khảo, trích dẫn kiểu tác giả–năm (APA) | Cuối tài liệu |

### Khối nội dung VCCI

```markdown
::: lead
Hai, ba câu nêu thông điệp chính (Lora, màu xanh).
:::

::: figures
64 ngày | Thời gian hoàn tất thủ tục
38% | Doanh nghiệp đi lại từ ba lần trở lên
:::

::: {.highlight title="Ba khuyến nghị ưu tiên"}
Hộp nhấn mạnh nền Blue Tint, gạch xanh bên trái.
:::

::: label
Nhãn chữ in hoa nhỏ
:::
```

Hộp `callout-note`, `-tip`, `-warning`, `-important`, `-caution` của Quarto dùng màu trạng thái VCCI (thông tin, thành công, cảnh báo, lỗi). Mỗi chương (`#`) bắt đầu trang mới với nhãn "CHƯƠNG 01" và gạch vàng; `{.unnumbered}` cho chương không đánh số (Tóm tắt, Phụ lục).

### Lưu ý

- **Bảng rộng:** Pandoc chia độ rộng cột theo số dấu `-` ở dòng phân cách khi bảng có dòng dài. Cột có chữ dài thì cho nhiều dấu `-` hơn, ví dụ `|-----------|--:|--:|`.
- **Tài liệu tham khảo** được Quarto đặt ở cuối tài liệu (sau phụ lục) với tiêu đề "Tài liệu tham khảo"; không tự thêm mục này.
- **Bản Word:**
  - Không có bìa màu như PDF; trang đầu là tiêu đề, tác giả, ngày.
  - Mục lục cần cập nhật một lần: nhấp vào mục lục rồi nhấn F9.
  - Danh sách đặt trong `::: highlight` nằm ngoài hộp, vì Pandoc chỉ áp style cho đoạn văn, không cho mục danh sách.
- **Phương trình** dùng font toán của Typst (PDF) hoặc Cambria Math (Word), vì Lora và Be Vietnam Pro không có ký hiệu toán.

## Phát triển

| Đường dẫn | Nội dung |
|---|---|
| `src/shared/vcci.typ` | Lớp Typst dùng chung: trang, chữ, tiêu đề, bảng, chú thích, logo, hero icon, vòng trống, gạch vàng, nhãn, đoạn dẫn, hộp nhấn mạnh, thẻ số liệu, hộp `callout` theo màu trạng thái, dấu bản thảo |
| `src/shared/vcci.lua` | Bộ lọc khối `lead`, `highlight`, `label`, `figures` cho Typst và Word; cờ `cover`/`back-cover` |
| `src/formats/<định dạng>/` | `_extension.yml`, `template.typ`, `typst-show.typ` của từng định dạng |
| `_extensions/vcci/<định dạng>/` | **Sinh tự động** bằng `build.py`; không sửa tay |
| `templates/` | Tài liệu mẫu cho người dùng |
| `tests/baseline/` | Ảnh chuẩn đã duyệt của từng trang PDF (lớp 5) |
| `tests/fixtures/` | Tài liệu thử: `minimal` (tối giản), `stress` (tiêu đề ba dòng, bảng 63 dòng qua trang, bảng rộng, trích dẫn, phương trình, đủ loại hộp ghi chú) |
| `tests/selftest/` | Tài liệu cố tình lỗi, để chứng minh bộ kiểm thử bắt được lỗi |

`build.py` lấy màu, font, logo, hero icon, họa tiết từ `brand-assets/` và file Word mẫu từ `VCCI_Report.dotx`. Mỗi extension tự chứa đủ (Quarto không cho các extension dùng chung file), nên phần dùng chung được chép vào từng extension. Logo và icon được nhúng thẳng vào mã Typst, nên không có file nào bị chép vào thư mục của người dùng.

Chạy từ thư mục gốc repo:

```bash
python quarto-vcci/build.py
```

```bash
python quarto-vcci/tests/run_tests.py
```

`build.py --check` báo lỗi nếu `_extensions/` lệch với nguồn. `run_tests.py` dựng mọi tài liệu thử và tài liệu mẫu trong thư mục sạch, ở chế độ bỏ qua font hệ thống (giống máy chưa cài font). Các lớp kiểm tra:

1. **Tĩnh:** extension khớp nguồn và `brand-tokens.json`.
2. **Dựng:** dựng thành công, không có cảnh báo nào.
3. **PDF:**
   - Chỉ font thương hiệu, đều được nhúng; khổ **A4**; số trang trong khoảng.
   - Đủ câu yêu cầu và **nhìn thấy được** (chữ bị đẩy ra ngoài trang tính là thiếu).
   - Không chữ nào sát mép giấy hay tràn lề hai bên; không chữ nào đè lên chữ khác.
4. **Word:**
   - Khổ **A4** ở mọi section; mọi style đều được định nghĩa; bảng dùng VCCI Table; font được nhúng.
   - Sau đó Microsoft Word mở file và xuất PDF. PDF đó phải khổ A4, mọi chữ theo font thương hiệu (trừ ký hiệu đầu dòng và phương trình).
   - Lớp này tự bỏ qua khi Word đang mở tài liệu của bạn, hoặc khi chạy với `--no-word`.
5. **So ảnh:** mỗi trang PDF được so với ảnh chuẩn đã duyệt trong `tests/baseline/`. Trang lệch quá ngưỡng thì báo kèm ảnh khác biệt (`diff-*.png`). Thay đổi cố ý đã được duyệt thì chạy lại với `--update-baseline`.
6. **Cài đặt:** `quarto add` vào thư mục trống, rồi dựng tài liệu mẫu ở đó.
7. **Tự kiểm:** các tài liệu trong `tests/selftest/` phải bị đúng kiểm tra tương ứng bắt lỗi.

Kết quả nằm ở `tests/out/summary.md` (kèm PDF, DOCX, PDF do Word xuất và ảnh từng trang).

Cần: Quarto ≥ 1.6 (có sẵn Typst), Python 3 với PyYAML và PyMuPDF, Poppler (`pdffonts`, `pdfinfo`, `pdftotext`, `pdftoppm`); Microsoft Word cho lớp 4.
