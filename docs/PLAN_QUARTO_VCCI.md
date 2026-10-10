# Kế hoạch: extension Quarto `quarto-vcci`

Ngày: 10/10/2026. Trạng thái: **chủ dự án đã duyệt (10/10/2026)**, gồm cả scheme Stata.

## 1. Mục tiêu và phạm vi

| Hạng mục | Đã thống nhất |
|---|---|
| Người dùng | Nhóm nghiên cứu (biết Markdown, chạy lệnh). Các phòng ban khác tiếp tục dùng template Word và skill `vcci-brand`. |
| Định dạng | Ba loại tài liệu trong **một** extension: báo cáo tư vấn (`vcci-report`), working paper (`vcci-wp`), memo (`vcci-memo`). |
| Đầu ra | **PDF bằng Typst** là bản chính. **Word (.docx)** để đồng nghiệp sửa, dựa trên template `VCCI_Report.dotx`. |
| Thứ tự | Báo cáo → working paper → memo. Mỗi loại được chủ dự án duyệt rồi mới làm loại tiếp theo. |
| Không làm (giai đoạn này) | Xuất HTML hay website; bản LaTeX; slide (đã có template PowerPoint). |

## 2. Học từ Monash và ANU

Tôi đã đọc cấu trúc các repo [quarto-monash/report](https://github.com/quarto-monash/report), [memo](https://github.com/quarto-monash/memo), [workingpaper](https://github.com/quarto-monash/workingpaper) và [anuopensci/quarto-anu-report](https://github.com/anuopensci/quarto-anu-report).

| Điều quan sát được | Áp dụng cho VCCI |
|---|---|
| Monash: mỗi loại tài liệu là một extension, gồm `_extension.yml`, `typst-template.typ` (bố cục) và `typst-show.typ` (chuyển metadata YAML sang tham số Typst). | Dùng đúng cấu trúc này cho từng định dạng. |
| Monash: font đi kèm extension (`fonts/`, khai báo `font-paths`), nên máy chưa cài font vẫn dựng đúng. | Đóng gói Lora và Be Vietnam Pro (giấy phép OFL cho phép). |
| Monash: khối `common` trong `_extension.yml` chứa thiết lập chung cho PDF và Typst. | Thiết lập chung (khổ A4, ngôn ngữ, đánh số mục, cỡ hình) viết một lần. |
| Monash: README ghi bản Typst "much faster" và "faster and more reliable" so với LaTeX. | Chỉ làm Typst; không duy trì bản LaTeX. |
| Monash và ANU: `template.qmd` ở gốc repo, `.quartoignore` loại `examples/`, có `examples/template.pdf` để xem trước. | Giữ cách này, để lệnh `quarto use template` tạo ngay một file mẫu. |
| ANU: Word xuất bằng `reference-doc` (một file `.docx` mang style ANU). | Sinh `reference-doc` tự động từ `VCCI_Report.dotx`. |
| **Không repo nào có kiểm thử tự động hay CI.** Họ chỉ lưu sẵn một PDF mẫu. | VCCI cần bộ kiểm thử riêng (mục 5). |
| Giấy phép: Monash dùng CC0; ANU không ghi giấy phép. | Chỉ học cấu trúc, tự viết mã, không chép tệp nào (theo `DECISIONS.md`). |

## 3. Đã kiểm chứng trên máy này (10/10/2026)

- Quarto 1.9.38 có sẵn Typst 0.14.2; Python có Jupyter.
- R 4.6.1 (`C:\Program Files\R\R-4.6.1\bin\x64`) đã có knitr, rmarkdown, ggplot2, svglite, nên chạy được khối mã R trong Quarto và kiểm thử `theme_vcci()`.
- Stata MP 19 (`C:\Program Files\StataNow19\StataMP-64.exe`) chạy được ở chế độ batch, nên kiểm thử được scheme Stata.
- Một file `.qmd` tiếng Việt dựng ra PDF bằng Typst với font đóng gói qua `font-paths`:
  - `pdffonts` cho thấy Be Vietnam Pro được nhúng.
  - Văn bản trích từ PDF giữ đủ các chữ ă â đ ê ô ơ ư và các dấu ỹ ỵ ữ ự.
- Bản Word dựng với `reference-doc` sinh từ `VCCI_Report.dotx` (đổi kiểu nội dung từ template sang document):
  - Heading 1 dùng Lora Medium; đủ các style VCCI (VCCI Table, VCCI Callout…).
  - Có 11 font được nhúng; đầu trang của template được giữ.
  - Hạn chế đã biết của Pandoc: bảng chưa tự nhận style "VCCI Table" và không có trang bìa. Cả hai xử lý ở mục 4.4.

## 4. Kiến trúc

### 4.1 Vị trí và phát hành

- **Phát triển** trong repo này, thư mục `quarto-vcci/`. Font, logo, màu và icon lấy trực tiếp từ `brand-assets/`, nên chỉ có một nguồn.
- **Phát hành**: một script xuất ra repo GitHub riêng `quarto-vcci` có `_extensions/` ở gốc, để người dùng chạy được `quarto use template <tài-khoản>/quarto-vcci`. Việc này làm khi đưa repo lên GitHub (việc mở số 1 trong handoff).

### 4.2 Cấu trúc thư mục (dự kiến)

```
quarto-vcci/
  build.py                  sinh các file dùng chung từ brand-assets, chép vào từng extension
  shared/                   nguồn dùng chung (viết tay)
    vcci.typ                màu, cỡ chữ, khoảng cách, hàm vẽ: bìa, nhãn chương, gạch vàng, hộp nhấn mạnh, bảng
    vcci-docx.lua           bộ lọc Pandoc cho Word: style bảng, hộp nhấn mạnh, chú thích hình/bảng tiếng Việt
  _extensions/vcci/
    vcci-report/            _extension.yml, typst-template.typ, typst-show.typ, + bản sao dùng chung (sinh tự động)
    vcci-wp/
    vcci-memo/
  templates/                report.qmd, wp.qmd, memo.qmd (mẫu tiếng Việt) + references.bib
  charts/                   vcci.mplstyle (matplotlib), theme_vcci.R (ggplot2)
  tests/                    fixtures/, baseline/, run_tests.py
  examples/                 PDF và DOCX mẫu đã dựng
```

Cách dùng trong tài liệu: `format: vcci-report-typst` hoặc `format: vcci-report-docx`.

**Cần kiểm chứng ở bước 0:**
- Quarto đặt tên định dạng thế nào khi các extension nằm trong thư mục tổ chức `_extensions/vcci/`.
- Có dùng chung được một file `vcci.typ` giữa các extension hay không. Nếu không, `build.py` sẽ chép bản sao vào từng extension: vẫn một nguồn, chỉ khác ở bản phân phối.

### 4.3 PDF (Typst)

**Phần chung**
- `lang: vi`; nhãn "Hình", "Bảng", "Mục lục", "Tài liệu tham khảo".
- Ngày viết "10 tháng 10 năm 2026"; tắt tách từ (tiếng Việt không tách âm tiết).
- Tiêu đề dùng Lora, nội dung dùng Be Vietnam Pro, đúng thang chữ trong `brand-tokens.json`.
- Màu đọc từ `brand-tokens.json` (gồm cả bảng màu biểu đồ v1.1).

**Báo cáo tư vấn**
- Bìa gồm logo trên ô nền sáng, khối xanh có họa tiết vòng trống, và hero icon chọn bằng YAML (`hero: 06`).
- Thông tin bên đặt hàng, mục lục, mở chương có nhãn và gạch vàng, đoạn dẫn.
- Hộp "Phát hiện chính", bảng theo kiểu VCCI Table, chú thích nguồn dưới hình và bảng.
- Phụ lục, bìa sau có thông tin liên hệ. Tùy chọn hiển thị "BẢN THẢO" hay "MẬT".

**Working paper**
- Số hiệu theo mẫu (mục 7), tóm tắt tiếng Việt và tiếng Anh, từ khóa, mã JEL.
- Gợi ý trích dẫn, lời miễn trừ, trích dẫn BibTeX (CSL APA).
- Trang đầu gọn, không bìa màu; đánh số phương trình.

**Memo**
- Khối Gửi / Từ / Ngày / Về việc, nhãn mức độ (Khẩn, Nội bộ), 1–2 trang, chữ ký tùy chọn.

### 4.4 Word (.docx)

- `build.py` sinh `vcci-reference.docx` từ `VCCI_Report.dotx` (đã thử thành công).
- Bộ lọc `vcci-docx.lua`:
  - Gán style "VCCI Table" cho bảng.
  - Gán style "VCCI Callout" cho hộp nhấn mạnh.
  - Dùng "Hình"/"Bảng" trong chú thích.
- Trang bìa Word: chèn một khối tiêu đề theo style Title và VCCI Label. Pandoc không dựng được bìa màu như PDF; tôi ghi rõ hạn chế này trong README.

### 4.5 Biểu đồ

- `vcci.mplstyle` cho matplotlib: kiểm thử được tại máy này.
- `theme_vcci()` và thang màu cho ggplot2: kiểm thử bằng R 4.6.1 trên máy này.
- Cả hai theo đúng thứ tự màu chuỗi, thang tuần tự và phân kỳ, và quy tắc chữ trong biểu đồ của phần 08.
- **Scheme Stata** `scheme-vcci.scheme` (đã duyệt): màu chuỗi, font, lưới, nền theo phần 08. Kiểm thử bằng Stata batch: vẽ bộ biểu đồ mẫu (cột, đường, cột ngang, phân tán), xuất SVG/PNG, kiểm tra mã màu trong SVG thuộc bảng màu VCCI, và chèn vào tài liệu mẫu.

## 5. Kiểm thử: làm sao để sản phẩm không lỗi

Chạy mọi kiểm thử bằng một lệnh: `python quarto-vcci/tests/run_tests.py`. Kết quả là báo cáo đạt/không đạt kèm ảnh các trang.

### 5.1 Tài liệu thử (fixtures)

Mỗi định dạng có hai file:
- **`template.qmd`**: file mẫu người dùng nhận được.
- **`stress.qmd`**: cố tình khó, gồm:
  - Tiêu đề dài ba dòng; nhiều cấp mục.
  - Đoạn văn tiếng Việt dài có chữ hoa và dấu chồng (Ở, Ỷ, Ữ).
  - Bảng dài qua trang và bảng rộng; hình kèm chú thích.
  - Chú thích cuối trang, trích dẫn, phương trình, tham chiếu chéo, hộp nhấn mạnh.
  - Thiếu metadata tùy chọn (không tác giả, không ngày); tên hai tác giả và đơn vị dài.

### 5.2 Các lớp kiểm tra

| Lớp | Kiểm tra | Tự động |
|---|---|---|
| 1. Tĩnh | `_extension.yml` đọc được; màu và cỡ chữ trong `vcci.typ` khớp `brand-tokens.json` (so sánh bằng script, như cách `build_assets.py colours` đang làm). | Có |
| 2. Dựng | Mọi tổ hợp {3 định dạng} × {PDF, Word} × {template, stress} dựng thành công, **không có dòng cảnh báo** (WARN cũng tính là lỗi). | Có |
| 3. Kiểm PDF | Chỉ có Lora và Be Vietnam Pro, đều được nhúng (`pdffonts`). Khổ A4. Số trang trong khoảng dự kiến. Văn bản trích từ PDF chứa đúng các câu tiếng Việt của nguồn. **Không chữ nào tràn lề** (tọa độ từng chữ, lấy bằng `pdftotext -bbox`, phải nằm trong khung lề). | Có |
| 4. Kiểm Word | Chỉ dùng style trong danh sách cho phép; mọi bảng mang style VCCI Table; font được nhúng. Mở bằng Word, lưu lại và xuất PDF để chắc Word không báo lỗi; chỉ chạy khi Word không mở tài liệu nào của bạn. | Có |
| 5. So ảnh | Mỗi trang PDF được chuyển thành ảnh và so với ảnh chuẩn đã duyệt (`tests/baseline/`). Trang nào lệch quá ngưỡng thì báo kèm ảnh khác biệt. Thay đổi cố ý thì cập nhật ảnh chuẩn sau khi bạn duyệt. | Có |
| 6. Cài mới | Tạo thư mục trống, cài extension như người dùng thật, dựng `template.qmd`. Kiểm tra gói đủ file và `.quartoignore` đúng. Thử thêm chế độ bỏ qua font hệ thống, nếu Quarto cho phép (kiểm chứng ở bước 0). | Có |
| 7. Người xem | Danh sách kiểm tra cho mỗi lần phát hành: bìa, mục lục, ngắt trang, dòng mồ côi, tiêu đề dài, một điểm nhấn vàng mỗi trang. Tôi tự xem ảnh từng trang trước khi gửi; bạn duyệt bản cuối. | Không |

Khi repo lên GitHub, có thể chạy lớp 1–3, 5 và 6 trên GitHub Actions (máy Linux). Lớp 4 cần Microsoft Word nên chỉ chạy trên máy Windows.

## 6. Các bước triển khai

| Bước | Nội dung | Sản phẩm | Điều kiện hoàn thành |
|---|---|---|---|
| 0 ✅ | Thử nghiệm kỹ thuật | Kết quả ở mục 10 | Trả lời các câu hỏi "cần kiểm chứng" ở mục 4.2 và 5.2 |
| 1 ✅ | Nền dùng chung và bộ kiểm thử | `build.py`, `shared/vcci.typ`, `vcci.lua` (bộ lọc chung cho Typst và Word), `tests/run_tests.py` (lớp 1–4, phần Word chưa mở bằng Word) | Lớp 1–3 chạy được trên một tài liệu tối giản |
| 2 ✅ | **Báo cáo tư vấn** | `vcci-report` (PDF và Word), `templates/report.qmd`, PDF mẫu | Mọi lớp kiểm thử đạt; **bạn duyệt PDF và Word** |
| 3 ✅ | Working paper | `vcci-wp`, `templates/wp.qmd`, `references.bib` | Như trên; bạn duyệt số hiệu và lời miễn trừ |
| 4 ✅ | Memo (tờ trình) | `vcci-memo`, `templates/memo.qmd` | Như trên |
| 5 ✅ | Biểu đồ và tài liệu | `vcci.mplstyle`, `theme_vcci.R`, scheme Stata; README; bổ sung skill `vcci-brand` và một trang trong hướng dẫn thương hiệu (phần Ứng dụng) | Biểu đồ mẫu đúng bảng màu; README chạy được từng lệnh |
| 6 ✅ | Phát hành | Repo `quarto-vcci`, phiên bản 1.0.0 | Lớp 6 đạt khi cài từ GitHub |

Mỗi bước kết thúc bằng một lần bạn duyệt. Không chuyển bước khi kiểm thử còn lỗi.

## 7. Đề xuất cho working paper (VCCI chưa có quy định)

Đây là đề xuất để VCCI quyết; template sẽ để các thông tin này thành tham số, đổi được mà không sửa mã.

- **Số hiệu:** "VCCI Working Paper số 2026/01" (năm/số thứ tự), tiếng Anh "VCCI Working Paper No. 2026/01".
- **Lời miễn trừ (bản nháp):** "Quan điểm trong bài là của tác giả, không nhất thiết phản ánh quan điểm của Liên đoàn Thương mại và Công nghiệp Việt Nam."
- **Gợi ý trích dẫn:** sinh tự động từ tác giả, năm, tiêu đề và số hiệu.
- **Chưa đưa vào:** ISSN và quy trình hội đồng duyệt, vì VCCI chưa có.

## 8. Rủi ro và cách xử lý

| Rủi ro | Cách xử lý |
|---|---|
| Quarto nâng cấp kéo theo Typst đổi cú pháp | Ghi `quarto-required` trong `_extension.yml`; lớp 2 và 5 phát hiện ngay khi nâng cấp. |
| Word (Pandoc) không dựng được bìa màu, khối nền màu | Ghi rõ trong README: bản Word để sửa nội dung; bản PDF để phát hành. |
| Font trong biểu đồ Stata | Stata dùng font cài trên máy; README hướng dẫn cài Lora và Be Vietnam Pro, scheme có font dự phòng. |
| Người dùng sửa thẳng file trong extension | `build.py` ghi đè; README chỉ cách tùy biến qua YAML. |

## 9. Cần chủ dự án quyết định

1. ~~Duyệt kế hoạch~~: đã duyệt 10/10/2026.
2. Số hiệu và lời miễn trừ cho working paper (mục 7): quyết khi tới bước 3.
3. ~~Scheme Stata~~: làm, ở bước 5.
4. ~~Tài khoản GitHub~~: `trongtrd`, repo công khai `trongtrd/quarto-vcci` (10/10/2026).

## 10. Kết quả bước 0 và bước 1 (10/10/2026)

**Bước 0: trả lời các câu hỏi cần kiểm chứng**

| Câu hỏi | Kết quả |
|---|---|
| Tên định dạng khi extension nằm trong `_extensions/vcci/` | `_extensions/vcci/vcci-report/` cho định dạng `vcci-report-typst` và `vcci-report-docx`. |
| Dùng chung file giữa các extension | Không cần: `build.py` ghép phần dùng chung vào `typst-template.typ` của từng extension, nên vẫn chỉ có một nguồn. |
| Logo và tài nguyên | `format-resources` chép file vào thư mục của người dùng. Vì vậy logo được **nhúng thẳng vào mã Typst** (SVG 112 KB); thư mục người dùng sạch. |
| Hero icon | Bộ 24 SVG nặng 1,6 MB, quá lớn để nhúng hết. Cách xử lý (rút gọn SVG, hoặc chỉ nhúng icon được chọn) quyết ở bước 2. |
| Bỏ qua font hệ thống | Đặt biến môi trường `TYPST_IGNORE_SYSTEM_FONTS=true`. Thiếu font đóng gói thì Typst báo "unknown font family", nên lớp 2 bắt được. Bộ kiểm thử luôn chạy ở chế độ này. |
| Bảng trong Word | Thay style "Table" (style Pandoc gán cho mọi bảng) bằng bản sao của "VCCI Table" trong file Word mẫu. Không cần bộ lọc. |

**Bước 1: đã có**

- `quarto-vcci/build.py`:
  - Sinh `_extensions/vcci/vcci-report/` (màu từ `brand-tokens.json`, logo, font kèm giấy phép OFL, file Word mẫu).
  - Đồng bộ từng file thay vì xóa thư mục, vì Dropbox hay khóa thư mục.
  - `--check` phát hiện file sinh ra bị sửa tay hoặc đã cũ.
- `src/shared/vcci.typ` (trang, chữ, tiêu đề, bảng, chú thích, logo, gạch vàng, nhãn, đoạn dẫn, hộp nhấn mạnh) và `src/shared/vcci.lua` (khối `::: lead`, `::: highlight`, `::: label` cho cả Typst và Word).
- Nhãn tiếng Việt: Hình, Bảng, Mục lục, Tài liệu tham khảo…; ngày viết "10 tháng 10 năm 2026".
- `tests/run_tests.py`: 19 kiểm tra trên tài liệu thử và 4 kiểm tra tự kiểm. **Lần chạy cuối: 23/23 đạt.**

**Lỗi bộ kiểm thử đã bắt được trong lúc làm**

1. Bản Word dùng 7 style của Pandoc (BodyText, FirstParagraph, Compact, Author, Date, ImageCaption, TOCHeading) mà file Word mẫu không định nghĩa, nên Word sẽ thay bằng Normal. Đã bổ sung 20 style Pandoc, kế thừa từ style VCCI.
2. Phần tự kiểm phát hiện chính bộ kiểm thử bỏ sót hai lỗi. Cảnh báo của Quarto có mã màu ANSI nên không khớp mẫu tìm kiếm. Chữ tràn ra ngoài trang thì bị ghi vào mục "sát mép" thay vì mục "tràn lề". Cả hai đã sửa.

**Chuyển sang bước 2**

- Hộp `callout` mặc định của Quarto trong bản Word được dựng bằng bảng, nên sẽ nhận style VCCI Table (hàng đầu nền xanh). Cần mở bằng Word để xem và xử lý (lớp 4 bằng Word thật).
- Chưa có lớp 5 (so ảnh với ảnh chuẩn) và lớp 6 (cài mới); làm khi bố cục báo cáo đã được duyệt, vì ảnh chuẩn phải là bản bạn đã duyệt.

## 11. Kết quả bước 2 (10/10/2026): `vcci-report`, chủ dự án đã duyệt

**Đã có**
- Bìa theo `VCCI_Report.dotx`: lockup, nhãn, tiêu đề, khối xanh có vòng trống, gạch vàng, ngày và phiên bản, bên đặt hàng, hero icon.
- Trang thông tin (bên đặt hàng, nhóm thực hiện, phiên bản, trích dẫn, lưu ý), mục lục.
- Chương mở trang mới có nhãn "CHƯƠNG 01" và gạch vàng; đầu trang có logo và tên rút gọn; chân trang "Trang X / N".
- Khối `lead`, `figures`, `highlight`, `label`; hộp `callout` của Quarto theo màu trạng thái VCCI; dấu "Bản thảo"/"Mật"; bìa sau.
- Bảng dài ngắt trang và lặp hàng tiêu đề; trích dẫn kiểu APA.
- Bản Word: style VCCI, bảng VCCI Table, chỉ đánh số chương như bản PDF.
- Mẫu: `templates/report.qmd`, kết quả ở `examples/`; hướng dẫn trong `quarto-vcci/README.md`.

**Bộ kiểm thử mở rộng (74/74 đạt)**
- Tài liệu thử `stress`; lớp 4 bằng Word thật; lớp cài đặt `quarto add` (thay cho lớp 6 cũ).
- Kiểm tra mới: chữ phải **nhìn thấy được**; không chữ nào đè lên nhau. Mỗi kiểm tra mới có tài liệu cố tình lỗi trong `tests/selftest/`.

**Lỗi tìm thấy và đã sửa nhờ kiểm thử và xem ảnh**

| Lỗi | Phát hiện bởi |
|---|---|
| Bảng 63 dòng bị cắt sau dòng 41, phần còn lại nằm ngoài trang | Ảnh trang; sau đó kiểm tra "chữ đè" bắt được bảng chạm chân trang. Kiểm tra "đủ chữ" cũ vẫn đạt vì đọc cả chữ ngoài trang, nên đã đổi sang chỉ đọc chữ nhìn thấy |
| Thẻ số liệu gộp thành một thẻ cao hết trang | Ảnh trang |
| Tiêu đề bìa và chương nhiều dòng quá sát (giãn dòng tính theo cỡ chữ 10 pt thay vì cỡ tiêu đề) | Ảnh phóng to |
| Nhãn "Bản thảo" màu vàng thành điểm nhấn vàng thứ hai | Xem theo quy tắc thương hiệu |
| Word đặt ký hiệu đầu dòng bằng Symbol/Arial, phương trình bằng Cambria Math | Lớp 4 (Word thật); cho phép riêng cho các ký hiệu này, chữ thường vẫn phải theo font thương hiệu |
| Template Word và PowerPoint mất hình nền khi dựng lại v1.1 (Edge chạy bất đồng bộ) | Ảnh xem trước của template; đã sửa ở commit `636fde3` |

**Giới hạn đã ghi trong README:** bản Word không có bìa màu; mục lục Word cần F9; danh sách trong `::: highlight` nằm ngoài hộp ở bản Word; tài liệu tham khảo luôn ở cuối.

**Sau khi duyệt**
- Lớp 5 (so ảnh) dùng bản đã duyệt làm ảnh chuẩn. Có phép tự kiểm: nội dung dịch xuống 3 mm phải bị bắt.
- Kiểm tra khổ A4 cho bản Word (kích thước trang trong `.docx` và PDF do Word xuất). Mọi tài liệu VCCI dùng khổ **A4**, không dùng Letter.
- Bìa giữ theo bìa template Word, để báo cáo làm bằng Word và bằng Quarto cùng một nhận diện.
- Kết quả: 87/87 kiểm tra đạt.

## 12. Kết quả bước 3 (10/10/2026): `vcci-wp`, chủ dự án đã duyệt

**Định dạng**
- Trang đầu không bìa màu: logo, "VCCI Working Paper" và số hiệu, tiêu đề, gạch vàng, tác giả (đơn vị, email, \* tác giả liên hệ), ngày.
- Tóm tắt và từ khóa song ngữ, mã JEL; chân trang đầu có trích dẫn đề nghị (tự sinh nếu không khai báo), tác giả liên hệ, lời miễn trừ, ©.
- Thân bài đánh số 1, 1.1; đầu trang có tên bộ và số hiệu; phương trình đánh số; APA.
- Hỗ trợ bài tiếng Anh (`lang: en`): nhãn của template và của Quarto đều chuyển sang tiếng Anh. Nhãn Quarto tiếng Việt khai báo theo ngôn ngữ (`language: vi:`), nên `vcci-report` cũng dùng được cho báo cáo tiếng Anh.
- Đề xuất cho VCCI quyết (đều là tham số): số hiệu dạng "2026/01"; lời miễn trừ "Quan điểm trong bài là của tác giả, không nhất thiết phản ánh quan điểm của Liên đoàn Thương mại và Công nghiệp Việt Nam."

**Kiểm thử: 136/136 đạt**
- Thêm tài liệu thử `wp-en` (bài tiếng Anh) và mẫu `templates/wp.qmd`.
- Phép so ảnh xác nhận việc tái cấu trúc nhãn không làm đổi báo cáo tiếng Việt đã duyệt.
- Sửa nhờ kiểm thử: bản Word không có tiêu đề "Tài liệu tham khảo"; tiêu đề tóm tắt tiếng Việt của Pandoc là "Tóm tắt nội dung"; dòng tên bộ và số hiệu nằm lạc giữa hai bản tóm tắt; kiểm thử cài đặt chưa chép `references.bib`.
- Chỉnh bộ kiểm thử: so chữ không phân biệt hoa thường và bỏ khoảng trắng, vì nhãn in hoa có giãn chữ bị `pdftotext` tách thành "A B ST R ACT".

**Sau khi duyệt**
- Chủ dự án duyệt bố cục, số hiệu dạng "2026/01" và lời miễn trừ mặc định.
- Theo cho phép của chủ dự án, `apa.csl` (APA 7, citation-style-language/styles, CC BY-SA 3.0) được kèm vào extension. Bản Word của báo cáo và working paper giờ trình bày tài liệu tham khảo theo APA như bản PDF.
- Ảnh chuẩn cho `wp` và `wp-en` đã tạo; ảnh chuẩn của báo cáo không đổi.

## 13. Kết quả bước 4 (10/10/2026): `vcci-memo` (tờ trình), chủ dự án đã duyệt

**Định dạng**
- Trang 1: logo, chữ "GHI NHỚ" kèm nhãn mức độ ("Khẩn"); khối Gửi, Từ, Đồng gửi, Ngày, Về việc; gạch vàng.
- Thân memo có tiêu đề mục gọn; chữ ký bên phải; tài liệu kèm theo.
- Từ trang 2, đầu trang nhắc lại "Về việc"; chân trang "Trang X / N"; dấu chìm "Nội bộ"/"Mật".
- Song ngữ (`lang: en`).
- Khóa `recipient`, `sender`, `copy-to`, vì `to` và `from` là khóa riêng của Pandoc (lỗi "cannot produce pdf output from chủ tịch vcci").

**Kiểm thử: 204/204 đạt**
- Thêm tài liệu thử `memo-en` (hai trang) và mẫu `templates/memo.qmd`.
- Kiểm tra mới: không có ký tự hỏng (U+FFFD) trong PDF, Word và PDF do Word xuất; có tự kiểm đi kèm.
- Lỗi tìm thấy:
  - `string.upper` của Lua xử lý theo byte, làm hỏng "GHI NHỚ · KHẨN" trong bản Word thành ký tự lỗi. Kiểm tra chữ trong Word bắt được; đã bỏ, vì style VCCI Label tự viết hoa.
  - Tiêu đề mục memo trong Word to như chương báo cáo; đã hạ một cấp.
  - Nhãn "Tài liệu kèm theo" bị tách khỏi danh sách ở cuối trang; style VCCI Label giờ luôn đi liền đoạn sau (cho cả ba định dạng).

**Quyết định của chủ dự án sau khi xem bản đầu (10/10/2026)**
- Tên tiếng Việt của memo là **"Tờ trình"** (bản tiếng Anh giữ "Memo"), vì định dạng này là văn bản đệ trình nội bộ.
- Kiểu trích dẫn: **báo cáo và tờ trình dùng Chicago chú thích cuối trang** (văn phong chính sách, ứng dụng); **working paper giữ APA**.
- Chicago dùng `vcci-chicago-notes.csl`, bản tùy biến từ `chicago-notes-bibliography.csl` (CSL project, CC BY-SA 3.0; tải theo phép của chủ dự án), dùng cho cả PDF (Typst đọc CSL) lẫn Word. Hai chỗ tùy biến:
  - Không có dấu phẩy trước "và" khi có hai tác giả.
  - Với `@techreport`, khai báo `type = {Báo cáo kỹ thuật}` trong `.bib` để thay "technical report".
- Tên người Việt trong `.bib` viết trong ngoặc nhọn `{Nguyễn Thị Hạnh}` để không bị đảo hay viết tắt.

**Kiểm thử**
- 207/207 đạt khi chạy đầy đủ (trước khi cập nhật ảnh chuẩn, chỉ các trang cố ý thay đổi bị báo).
- Phép so ảnh giờ so theo ô 32 × 32 px; phần tự kiểm xác nhận một từ thay đổi cũng bị bắt.
- Ảnh chuẩn cập nhật cho các trang có trích dẫn; thêm ảnh chuẩn cho `memo` và `memo-en`.

**Bước tiếp theo: bước 5** (theme biểu đồ R, matplotlib, scheme Stata; README; skill `vcci-brand`; một trang trong hướng dẫn thương hiệu), rồi bước 6 (phát hành).


## 14. Kết quả bước 5 (10/10/2026): theme biểu đồ và tài liệu, chủ dự án đã duyệt

**Quyết định của chủ dự án trước khi làm**
- Nguồn theme nằm ở `quarto-vcci/src/charts/`, `build.py` sinh bản dùng vào `quarto-vcci/charts/` và chép một bản cho người không dùng Quarto.
- Theme R là một file dùng bằng `source()`, chưa làm thành gói.
- Mặc định dấu phẩy thập phân; bài tiếng Anh chọn dấu chấm.
- Có mẫu `templates/charts.qmd` với khối mã R. Khối Python chạy được bằng Jupyter nên có thêm tài liệu thử `charts-py`; R và Python không trộn trong một tài liệu (máy chưa có reticulate).

**Đã có**
- `vcci_charts.py` và `vcci.mplstyle` (matplotlib), `theme_vcci.R` (ggplot2), `scheme-vcci.scheme` và `vcci_graph.do` (Stata). Mã màu và tên font được `build.py` điền từ `brand-tokens.json`; `--check` báo khi bản sinh ra lệch nguồn.
- Bản sao nằm ở `brand-assets/06_Templates/Charts/`, không phải `02_Colour/`, vì `build_assets.py` xóa và dựng lại cả thư mục `02_Colour`.
- `charts/README.md` có cách dùng và ví dụ cho từng công cụ.
- Mục "Biểu đồ" và lớp kiểm thử 8 trong `quarto-vcci/README.md`.
- Phần C của skill `vcci-brand` và một dòng trong `AGENTS.md`.
- Trang 34 "Tài liệu và biểu đồ từ mã" trong hướng dẫn thương hiệu (phần 09); hướng dẫn giờ có 37 trang.

**Lớp kiểm thử 8**
- Cùng một bộ số liệu (`tests/charts/data/`) được vẽ bằng cả ba công cụ, gồm sáu biểu đồ: cột có một giá trị nhấn vàng, ba đường, cột ngang chồng, phân tán, sáu chuỗi, bảng nhiệt. Stata không vẽ bảng nhiệt vì không có lệnh sẵn.
- Mỗi SVG phải đạt:
  - chỉ dùng màu VCCI; không trong suốt;
  - chữ giữ dạng chữ, đúng font thương hiệu; có tiêu đề tiếng Việt;
  - dấu phẩy thập phân; không lưới dọc;
  - vàng nhấn tối đa một giá trị; cột bắt đầu từ 0; sáu chuỗi đúng thứ tự màu.
- `charts-tools` chèn 17 biểu đồ vào báo cáo, `charts-py` chạy matplotlib qua Jupyter, `templates/charts.qmd` chạy ggplot2 qua knitr. Cả ba qua các lớp 2–5, kể cả Word thật.
- Mỗi ví dụ mã trong `charts/README.md` được chạy thật.
- Tự kiểm có 11 file lỗi cố ý trong `tests/selftest/charts/`:
  - biểu đồ để mặc định của matplotlib, ggplot2 và Stata;
  - trong suốt; trục không từ 0; chữ chuyển thành nét;
  - lưới dọc; dấu chấm thập phân;
  - vàng làm màu chuỗi; màu trạng thái làm màu chuỗi;
  - README có ví dụ hỏng.

**Lỗi tìm thấy nhờ xem ảnh và kiểm thử**

| Lỗi | Cách sửa |
|---|---|
| matplotlib ghi năm thành "2.020" (dấu chấm hàng nghìn của locale tiếng Việt) | Chỉ đổi dấu thập phân, không nhóm hàng nghìn trên trục; không đổi locale của tiến trình |
| Nét trong ggplot mảnh hơn thiết kế 25% (R tính độ dày nét theo 1/96 inch, không theo pt) | Quy đổi trong `theme_vcci()` |
| Cột ggplot có viền xanh (màu viền mặc định đặt qua `element_geom`) | Chỉ đặt màu nền |
| Tên font "Lora Medium" trong SVG: Typst không nhận, lặng lẽ thay bằng Libertinus | Tiêu đề ggplot dùng "Lora"; lớp 3 bắt được font lạ |
| Stata: tiêu đề căn giữa, còn đường trục dọc, nét mảnh, nhãn trục tung to hơn trục hoành | Sửa trong scheme (vị trí 11, trục `vertical_nolinetick`, độ dày tính theo kích thước biểu đồ, `tick_biglabel`) |
| Stata vẽ cột vàng hai lần (nền và viền rộng 0), bị đếm là hai điểm nhấn | Kiểm tra đếm theo hình, bỏ qua viền rộng 0 |
| Nhãn phần trăm của biểu đồ cột chồng trong mẫu R nằm sai mảng | Thêm `group` trong mẫu |
| Tài liệu thử `charts` trùng tên với mẫu `charts` | Đổi thành `charts-tools` |

**Giới hạn và quan sát**
- Theme matplotlib, ggplot2 và Stata cho cùng nhận diện nhưng không giống hệt điểm ảnh: khoảng cách lề và vị trí chú giải theo mặc định của từng công cụ. Chú giải của Stata nằm giữa, không căn trái.
- Tiêu đề trong biểu đồ ggplot dạng SVG là Lora Regular, không phải Medium (svglite chỉ ghi được độ đậm "bold").
- Poppler (`pdftoppm`) vẽ một vạch mảnh cạnh một số cột và đường trong SVG đã chèn. PDF chỉ chứa hình tô màu (đã kiểm bằng PyMuPDF); MuPDF hiển thị sạch.
- Lớp chữ của PDF do Word xuất làm mất chữ "ứ" trong một số chú thích hình. Trang in vẫn hiển thị đúng.
- Lora và Be Vietnam Pro không có font đơn cách, nên chữ dạng mã từng dùng DejaVu Sans Mono (Typst) và Consolas (Word). Đã xử lý bằng JetBrains Mono, xem phần "Font cho mã" bên dưới.

**Sau khi duyệt**
- Chủ dự án duyệt theme, mẫu biểu đồ, trang 34 của hướng dẫn và lớp kiểm thử 8.
- Ảnh chuẩn (lớp 5) cho `charts-tools`, `charts-py` và mẫu `charts`. Vẽ lại bằng cả ba công cụ và so lại: khớp từng điểm ảnh.
- Lần chạy đầy đủ cuối (có Word thật và Stata): 425/425 đạt.

**Font cho mã (10/10/2026, chủ dự án cho phép tải và duyệt)**
- JetBrains Mono v2.304 (bản phát hành chính thức trên GitHub của JetBrains, SIL OFL 1.1). Chỉ lấy Regular và Bold; đã kiểm đủ dấu tiếng Việt. Font nằm ở `brand-assets/03_Fonts/JetBrainsMono` và được đóng gói vào cả ba định dạng.
- Typst: `show raw` dùng JetBrains Mono, tắt ligature (`<-` không thành mũi tên).
- Word: style Source Code và Verbatim Char dùng JetBrains Mono; font được nhúng (đã làm rối như Word) vào `vcci-reference.docx` với khóa cố định, nên bản dựng lặp lại được.
- `vcci.theme` (sinh từ `brand-tokens.json`) thay theme tô cú pháp mặc định của Quarto (xanh lá, đỏ, tím) bằng màu VCCI, nền Ivory, cho cả PDF lẫn Word.
- Kiểm thử:
  - Thêm tài liệu thử `code` (working paper có mã R và Stata, chữ có dấu).
  - Thêm tự kiểm `foreign-code-font` (mã bị ép sang DejaVu Sans Mono phải bị bắt).
  - Word đổi tên font nhúng thành `___WRD_EMBED_SUB_52` khi xuất PDF. Bộ kiểm thử giờ nhận diện font theo hình nét chữ, có tự kiểm: JetBrains Mono phải được nhận đúng, DejaVu Sans Mono không được nhận nhầm.
  - Đọc chữ trong `.docx` giờ giải mã `&lt;`.
- Chủ dự án duyệt hình thức mã (màu, nền Ivory, không ligature). Ảnh chuẩn cho tài liệu thử `code`. Lần chạy đầy đủ cuối: 459/459 đạt; ảnh chuẩn các tài liệu đã duyệt không đổi.

**Tiếp theo:** bước 6 (phát hành, cần tài khoản GitHub).

## 15. Kết quả bước 6 (10/10/2026): phát hành 1.0.0

**Quyết định của chủ dự án:** duyệt theo khuyến nghị.
- Tài khoản `trongtrd`, repo công khai [trongtrd/quarto-vcci](https://github.com/trongtrd/quarto-vcci).
- README tiếng Việt, có đoạn tiếng Anh ngắn ở đầu.
- Bản Word mẫu đính kèm vào GitHub Release, không để trong repo.
- Repo phát hành đặt ngoài Dropbox: `C:\GitHub Projects\quarto-vcci`.

**Đã có**
- `quarto-vcci/release.py --out <thư mục>` xuất repo phát hành:
  - extension; `template.qmd` (báo cáo); `wp.qmd`, `memo.qmd`, `charts.qmd`, `references.bib`;
  - `charts/`; các PDF mẫu trong `examples/`;
  - README (phần đầu ở `src/release/README-head.md`, phần còn lại lấy từ các mục "Dùng …" và "Biểu đồ" của `quarto-vcci/README.md`), LICENSE, CHANGELOG, `.quartoignore` (trong `src/release/`).
- Script dừng nếu `build.py --check` lệch, nếu ba `_extension.yml` khác phiên bản, nếu CHANGELOG thiếu mục của phiên bản, hoặc nếu một câu cần thay trong README không còn (README phát triển đã đổi). Nó giữ `.git` của thư mục đích và từ chối ghi vào thư mục lạ.
- Phiên bản 1.0.0 cho cả ba định dạng; tag `v1.0.0`; GitHub Release kèm 4 file `.docx`.
- Người dùng cài: `quarto use template trongtrd/quarto-vcci` (cả dự án mẫu) hoặc `quarto add trongtrd/quarto-vcci` (chỉ extension).
- `gh` 2.102.0 cài qua winget; chủ dự án tự đăng nhập (`gh auth login`).

**Lỗi tìm thấy nhờ thử cài trước khi push**

| Lỗi | Cách sửa |
|---|---|
| Với `_extensions/vcci/<định dạng>`, `quarto use template` báo "Extensions installed" nhưng không cài gì. Quarto 1.9 chỉ đọc `_extensions/<tên>` của repo mẫu (`readExtensions` trên thư mục gốc đi xuống hai cấp). | Repo phát hành để extension phẳng ở `_extensions/<định dạng>/`. Khi cài từ GitHub, Quarto tự đặt vào `_extensions/trongtrd/<định dạng>/`; tên định dạng không đổi. |
| Theme R và Python tìm font cố định ở `_extensions/vcci/*/fonts`, nên sau khi cài từ GitHub sẽ không thấy font (máy chưa cài font). | Tìm ở cả `_extensions/*/fonts` và `_extensions/*/*/fonts`. Đã kiểm trên bản cài từ GitHub: R và Python đều thấy 3 thư mục font. |
| `charts.qmd` để trong `charts/` không dựng được: Quarto không tìm `_extensions` ở thư mục cha khi không có project. | `charts.qmd` ở gốc, gọi `source("charts/theme_vcci.R")` (`release.py` sửa dòng này khi xuất). |
| Stata không thấy scheme khi `do charts/vcci_graph.do` từ thư mục gốc. | README phát hành ghi `adopath + "charts"` trước; đã chạy thử bằng Stata thật. |
| `quarto use template` không nhận file zip cục bộ trên Windows ("Url scheme 'c' not supported"). | Thử cục bộ bằng thư mục, không bằng zip. |

**Kiểm thử**
- Lớp 6 mới:
  - Xuất repo phát hành vào thư mục tạm, cài bằng `quarto use template` và `quarto add`.
  - Kiểm: đủ mẫu và theme biểu đồ; extension giống hệt bản dựng (từng font, style, bộ lọc); đúng phiên bản; không có file mà `.quartoignore` loại; mọi mẫu dựng được ở cả PDF và Word, không cảnh báo.
  - `--install-from trongtrd/quarto-vcci@v1.0.0` chạy riêng lớp này với bản trên GitHub.
- Tự kiểm mới: bản xuất thiếu một font, bản có cấu trúc `_extensions/vcci/`, bản để lọt `examples/`; cả ba đều bị bắt.
- Lần chạy đầy đủ (Word thật, R, Stata): **469/469 đạt**.
- Cài từ GitHub (`@v1.0.0` và bản mới nhất): **14/14 đạt** mỗi lần.

**Phát hành bản sau:** quy trình 5 bước ở mục "Phát hành" của `quarto-vcci/README.md`.
