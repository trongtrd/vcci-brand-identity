# quarto-vcci (đang phát triển)

Extension Quarto cho tài liệu VCCI: báo cáo tư vấn (`vcci-report`), working paper (`vcci-wp`), tờ trình (`vcci-memo`). Mỗi định dạng xuất PDF bằng Typst (bản chính) và Word (để đồng nghiệp sửa). Kế hoạch: [`docs/PLAN_QUARTO_VCCI.md`](../docs/PLAN_QUARTO_VCCI.md).

Trạng thái: `vcci-report`, `vcci-wp` và `vcci-memo` (tờ trình) đã được duyệt (bước 2–4, 10/10/2026). Tiếp theo: bước 5 (theme biểu đồ, tài liệu).

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
| `bibliography` | Tài liệu tham khảo; trích dẫn kiểu Chicago chú thích cuối trang | Chú thích, cuối tài liệu |

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
- **Trích dẫn:** báo cáo và tờ trình dùng Chicago chú thích cuối trang (lần đầu đầy đủ, các lần sau rút gọn); luôn viết trong ngoặc vuông, `[@khoa]` hay `[@khoa, tr. 12]`, vì `@khoa` đứng trần sẽ in cả nguồn giữa câu. Working paper dùng APA (tác giả–năm), nơi `@khoa` cho "Tác giả (năm)" trong câu. Kiểu Chicago là bản tùy biến `vcci-chicago-notes.csl`: không đặt dấu phẩy trước "và" khi có hai tác giả. Với `@techreport`, thêm `type = {Báo cáo kỹ thuật}` để không hiện "technical report". Trong file `.bib`, viết tên người Việt trong ngoặc nhọn, `author = {{Nguyễn Thị Hạnh} and {Trần Đức Long}}`, để tên không bị đảo thành "Thị Hạnh Nguyễn" hay viết tắt thành "Nguyễn, T. H.".
- **Tài liệu tham khảo** được Quarto đặt ở cuối tài liệu (sau phụ lục) với tiêu đề "Tài liệu tham khảo"; không tự thêm mục này.
- **Bản Word:**
  - Không có bìa màu như PDF; trang đầu là tiêu đề, tác giả, ngày.
  - Mục lục cần cập nhật một lần: nhấp vào mục lục rồi nhấn F9.
  - Danh sách đặt trong `::: highlight` nằm ngoài hộp, vì Pandoc chỉ áp style cho đoạn văn, không cho mục danh sách.
- **Phương trình** dùng font toán của Typst (PDF) hoặc Cambria Math (Word), vì Lora và Be Vietnam Pro không có ký hiệu toán.

## Dùng `vcci-wp` (working paper)

Chép `templates/wp.qmd` (kèm `templates/references.bib`) làm điểm bắt đầu. Bản mẫu: [`examples/wp.pdf`](examples/wp.pdf), [`examples/wp.docx`](examples/wp.docx), bản tiếng Anh [`examples/wp-en.pdf`](examples/wp-en.pdf).

Trang đầu gồm: tên bộ và số hiệu, tiêu đề, tác giả (đơn vị, email), ngày, tóm tắt kèm từ khóa (một hoặc hai ngôn ngữ), mã JEL. Chân trang đầu có trích dẫn đề nghị, tác giả liên hệ, lời miễn trừ. Thân bài đánh số mục 1, 1.1; phương trình đánh số; tài liệu tham khảo kiểu APA ở cuối.

| Khóa | Ý nghĩa |
|---|---|
| `wp-number` | Số hiệu, ví dụ `"2026/01"`: hiện "VCCI Working Paper số 2026/01" (tiếng Anh: "No. 2026/01") |
| `wp-series` | Tên bộ, mặc định "VCCI Working Paper" |
| `lang` | `vi` (mặc định) hoặc `en`. Bản tiếng Anh nên thêm `date-format: "D MMMM YYYY"` |
| `author` | `name`, `email`, `affiliations`; `attributes: {corresponding: true}` đánh dấu \* tác giả liên hệ |
| `abstract`, `keywords` | Tóm tắt và từ khóa theo ngôn ngữ của bài |
| `abstract-en`, `keywords-en` | Tóm tắt tiếng Anh cho bài tiếng Việt (bài tiếng Anh dùng `abstract-vi`, `keywords-vi`) |
| `jel` | Mã JEL, ví dụ `[D22, K23]` |
| `thanks` | Lời cảm ơn: chú thích † ở tiêu đề |
| `citation-text` | Thay gợi ý trích dẫn tự sinh ("Tác giả (năm). Tiêu đề. VCCI Working Paper số …. Hà Nội: VCCI.") |
| `disclaimer` | Thay lời miễn trừ mặc định |
| `status`, `short-title`, `version`, `toc` | Như `vcci-report` |

Trong bản Word, tên bộ và số hiệu nằm trên dòng ngày; từ khóa, tóm tắt thứ hai, mã JEL, trích dẫn và lời miễn trừ nằm ở đầu thân bài.

## Dùng `vcci-memo` (tờ trình)

Chép `templates/memo.qmd`. Bản mẫu: [`examples/memo.pdf`](examples/memo.pdf), [`examples/memo.docx`](examples/memo.docx), bản tiếng Anh hai trang [`examples/memo-en.pdf`](examples/memo-en.pdf).

| Khóa | Ý nghĩa |
|---|---|
| `title` | Nội dung "Về việc" |
| `recipient`, `sender`, `copy-to` | Gửi, Từ, Đồng gửi (`to` và `from` là khóa riêng của Pandoc nên không dùng được); không có `sender` thì lấy `author` |
| `date` | Ngày |
| `priority` | Ví dụ "Khẩn": nhãn cạnh chữ "TỜ TRÌNH" |
| `status` | Ví dụ "Nội bộ", "Mật": dấu chìm mọi trang |
| `signature` | `name` và `title` (chức vụ), đặt bên phải cuối memo |
| `attachments` | Danh sách tài liệu kèm theo |
| `memo-label` | Thay chữ "Tờ trình" (tiếng Anh: "Memo") |
| `lang: en` | Memo tiếng Anh ("MEMO", To, From, Subject…); thêm `date-format: "D MMMM YYYY"` |

Tiêu đề mục (`#`) của memo nhỏ hơn chương của báo cáo và không đánh số. Từ trang 2, đầu trang nhắc lại "Về việc".

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
5. **So ảnh:** mỗi trang PDF được so với ảnh chuẩn đã duyệt trong `tests/baseline/`, theo từng ô 32 × 32 điểm ảnh (khoảng 16 mm), nên chỉ một từ thay đổi cũng bị phát hiện. Trang lệch thì báo kèm ảnh khác biệt (`diff-*.png`). Thay đổi cố ý đã được duyệt thì chạy lại với `--update-baseline`.
6. **Cài đặt:** `quarto add` vào thư mục trống, rồi dựng tài liệu mẫu ở đó.
7. **Tự kiểm:** các tài liệu trong `tests/selftest/` phải bị đúng kiểm tra tương ứng bắt lỗi.

Kết quả nằm ở `tests/out/summary.md` (kèm PDF, DOCX, PDF do Word xuất và ảnh từng trang).

Cần: Quarto ≥ 1.6 (có sẵn Typst), Python 3 với PyYAML và PyMuPDF, Poppler (`pdffonts`, `pdfinfo`, `pdftotext`, `pdftoppm`); Microsoft Word cho lớp 4.
