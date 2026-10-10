---
name: vcci-brand
description: Áp dụng Bộ nhận diện thương hiệu VCCI (Liên đoàn Thương mại và Công nghiệp Việt Nam) cho tài liệu. Dùng khi người dùng muốn định dạng một file Word thô thành báo cáo VCCI, chuyển một file PowerPoint thô (hoặc dàn ý, báo cáo) thành bài trình bày VCCI, soạn báo cáo, working paper, tờ trình VCCI bằng Quarto, vẽ biểu đồ theo màu VCCI bằng Python (matplotlib), R (ggplot2) hay Stata, hoặc hỏi về logo, màu, font, quy tắc thương hiệu VCCI. Use for any request to turn a raw .docx into a VCCI-branded report, a raw .pptx or outline into a VCCI-branded presentation, to write a VCCI report, working paper or memo in Quarto, to style charts in matplotlib, ggplot2 or Stata with the VCCI theme, or to apply VCCI brand colours, fonts and logo rules.
---

# VCCI Brand: báo cáo Word, bài trình bày PowerPoint, tài liệu Quarto và biểu đồ

Skill này đưa nội dung thô vào template VCCI: báo cáo theo `VCCI_Report.dotx`, bài trình bày theo `VCCI_Presentation.potx`. Màu, font và bố cục do template và script quyết định. Agent chỉ phải xác định **cấu trúc** của nội dung và giữ nguyên câu chữ, số liệu.

Script nằm trong `scripts/word/` và `scripts/ppt/` (đường dẫn tính từ thư mục skill này), cần Python 3.9+ với `lxml`, `Pillow` và (cho PowerPoint) `python-pptx`. Script tự tìm `brand-assets/` ở các thư mục cha; nếu skill được chép ra khỏi repo, đặt biến môi trường `VCCI_BRAND_ROOT` trỏ tới bản clone của repo `vcci-brand-identity`.

Bước hoàn thiện (`finalize.py`) cần Microsoft Word hoặc PowerPoint trên Windows. Script tự dừng nếu người dùng đang mở tài liệu trong ứng dụng đó: khi ấy nhờ người dùng đóng ứng dụng, **không bao giờ tắt Word hay PowerPoint của người dùng**. Không có Office thì bỏ qua bước này và nói rõ là chưa tự kiểm tra bằng hình.

## A. Báo cáo Word

1. **Trích xuất** file thô sang Markdown nháp (ảnh tách vào `media/` cạnh file `.md`):
   ```bash
   python scripts/word/extract_docx.py "<file thô>.docx" -o "<thư mục làm việc>/report.md"
   ```
   Nếu đầu vào là PDF hoặc định dạng khác, tự chuyển sang Markdown theo cùng cú pháp.

2. **Biên tập cấu trúc** trong `report.md`, theo [references/word-markdown.md](references/word-markdown.md):
   - Điền front matter: `title`, `subtitle`, `date`, `author`, `unit`, `header`, `label`, `contact`, `icon` (hero icon trên bìa, chọn theo chủ đề trong bảng ở cuối file tham chiếu). Lấy thông tin từ bản thô; dòng nào không có thì xóa (không đoán ngày, đầu mối liên hệ). Dòng `<!-- title: … -->` nếu có là tên tài liệu gốc; xóa dòng tác giả, đơn vị ở đầu bài sau khi đưa lên bìa.
   - Bản gốc tự đánh số mục ("1. …"): bỏ số khỏi tiêu đề và dùng `{label="Mục 1"}`; mục không đánh số như Tóm tắt, Tài liệu tham khảo dùng `{.nolabel}`.
   - `#` là chương, `##` và `###` là mục con. Nếu bản thô dùng chữ in đậm thay cho heading, chuyển thành heading.
   - Đoạn mở đầu quan trọng nhất của chương đặt trong `::: lead`, chỉ khi đoạn đó ngắn (tối đa khoảng 70 từ). Khuyến nghị hoặc định nghĩa then chốt đặt trong `::: callout` (tối đa một hộp mỗi trang). Ba đến bốn con số chủ chốt đặt trong `::: figures`.
   - Thay `Bảng: [tên bảng]` bằng tên thật. Chuyển các dòng `<!-- caption: … -->` thành chú thích của ảnh `![…](…)`, hoặc thành `Hình: …` trên bảng nếu bản gốc gọi bảng đó là hình. Dòng "Nguồn/Ghi chú" dưới bảng, hình đặt trong `::: note`; danh mục tài liệu tham khảo đặt trong `::: references`. Bảng mô tả hoặc danh mục thêm `{.light}`, bảng có hàng tổng thêm `{.total}`.

3. **Dựng báo cáo** và đọc các dòng `WARNING`:
   ```bash
   python scripts/word/render_report.py "<thư mục làm việc>/report.md" -o "<tên>_VCCI.docx"
   ```

4. **Hoàn thiện và tự kiểm tra:**
   ```bash
   python scripts/word/finalize.py "<tên>_VCCI.docx" --png
   ```
   Script cập nhật mục lục, xuất PDF và ảnh từng trang. **Xem các ảnh trang**: bìa, mục lục, bảng có tràn lề không, hình có rõ không, hộp nhấn mạnh có quá nhiều không. Không có Word thì Word sẽ hỏi cập nhật mục lục khi người dùng mở file.

Ví dụ: [examples/sample-report.md](examples/sample-report.md) → [examples/sample-report_VCCI.pdf](examples/sample-report_VCCI.pdf) (số liệu giả lập).

## B. Bài trình bày PowerPoint

1. **Trích xuất và xem bản gốc:**
   ```bash
   python scripts/ppt/extract_pptx.py "<file thô>.pptx" -o "<thư mục làm việc>/deck.md"
   python scripts/ppt/finalize.py "<bản sao của file thô>.pptx" --png --no-save
   ```
   Bước 1 lấy chữ theo thứ tự đọc, số liệu của biểu đồ thật, bảng, ảnh và ghi chú. Bước 2 xuất ảnh từng slide của bản gốc (chạy trên **bản sao**, không chạy trên file của người dùng). **Xem các ảnh này**: chữ trích xuất không cho biết đâu là thẻ số liệu, biểu đồ vẽ bằng hình hay chuỗi bước. Đầu vào là dàn ý hoặc báo cáo Word thì viết thẳng `deck.md`.

2. **Biên tập cấu trúc** trong `deck.md`, theo [references/ppt-markdown.md](references/ppt-markdown.md):
   - Front matter: `title`, `subtitle`, `presenter`, `footer`, `cover` (`light` cho họp và bài gửi đọc, `event` cho hội nghị, sân khấu), `end_title`, `contact`. Không đưa bìa và slide cảm ơn của bản gốc vào phần thân: script tự dựng.
   - Bản gốc có phần lớn (01, 02, 03…) thì thêm slide chuyển chương `# Tên phần {icon=…}`.
   - Mỗi slide `## Tiêu đề {label="…"}`: nhãn nhỏ phía trên tiêu đề của bản gốc (ví dụ "GIAI ĐOẠN 1 · …") đưa vào `label`; câu dẫn dưới tiêu đề vào `::: lead`; dòng nguồn vào `::: source`.
   - Thẻ số liệu → `::: figures`; biểu đồ (kể cả biểu đồ vẽ bằng hình, đọc số từ nhãn) → `::: chart`; hộp chữ có tiêu đề → `::: cards`; chuỗi mũi tên → `::: steps`; hộp ghi chú, hàm ý → `::: note`; danh sách có nhiều cột thông tin → bảng.
   - Giữ nguyên câu chữ. Slide quá nhiều chữ thì tách slide; chỉ rút gọn khi người dùng yêu cầu.

3. **Dựng bài trình bày** và đọc các dòng `WARNING` (tràn chỗ, tiêu đề quá dài):
   ```bash
   python scripts/ppt/render_deck.py "<thư mục làm việc>/deck.md" -o "<tên>_VCCI.pptx"
   ```

4. **Hoàn thiện và tự kiểm tra:**
   ```bash
   python scripts/ppt/finalize.py "<tên>_VCCI.pptx" --png
   ```
   PowerPoint lưu lại file (nhúng font), xuất PDF và ảnh từng slide. **Xem từng ảnh**: tiêu đề có đè gạch vàng không, chữ có tràn khỏi thẻ, hộp hay chạm chân trang không, nhãn số trên biểu đồ có đúng bản gốc không. Sửa `deck.md` rồi dựng lại cho đến khi đạt.

Ví dụ: [examples/sample-deck.md](examples/sample-deck.md) → [examples/sample-deck_VCCI.pdf](examples/sample-deck_VCCI.pdf) (số liệu giả lập).

## C. Tài liệu Quarto và biểu đồ bằng mã

Dùng khi người dùng viết bằng Markdown hoặc Quarto (nhóm nghiên cứu), cần working paper hay tờ trình, hoặc vẽ biểu đồ bằng Python, R, Stata. Extension nằm trong `quarto-vcci/` của repo; hướng dẫn đầy đủ ở `quarto-vcci/README.md`.

1. **Chọn định dạng** và chép mẫu tương ứng từ `quarto-vcci/templates/`:

   | Định dạng | Mẫu | Dùng cho |
   |---|---|---|
   | `vcci-report` | `report.qmd` | Báo cáo tư vấn: bìa, mục lục, chương, bìa sau; trích dẫn Chicago chú thích cuối trang |
   | `vcci-wp` | `wp.qmd`, `references.bib` | Working paper: số hiệu, tóm tắt song ngữ, mã JEL; trích dẫn APA |
   | `vcci-memo` | `memo.qmd` | Tờ trình: Gửi, Từ, Về việc, chữ ký; trích dẫn Chicago |
   | biểu đồ R | `charts.qmd` | Báo cáo có biểu đồ ggplot2 chạy trong tài liệu |

2. **Cài extension và dựng** trong thư mục làm việc:
   ```bash
   quarto add "<repo>/quarto-vcci" --no-prompt
   quarto render report.qmd
   ```
   Mỗi định dạng ra PDF (Typst, bản phát hành) và Word (`--to vcci-report-docx`, để đồng nghiệp sửa). Khóa YAML của từng định dạng ở `quarto-vcci/README.md`. Gửi, Từ của tờ trình là `recipient`, `sender` (không dùng `to`, `from`). Tên người Việt trong `.bib` viết trong ngoặc nhọn: `{Nguyễn Thị Hạnh}`.

3. **Biểu đồ:** chép file theme từ `quarto-vcci/charts/` (hoặc `brand-assets/06_Templates/Charts/`) cạnh file mã; cách dùng đầy đủ ở `charts/README.md`.
   - Python: `import vcci_charts as vcci; vcci.use()`, rồi `vcci.highlight()`, `vcci.title()`, `vcci.source()`.
   - R: `source("theme_vcci.R"); vcci_setup()`, rồi `vcci_highlight()`, `scale_fill_vcci()`, `label_vcci()`.
   - Stata: `do vcci_graph.do`, rồi `graph export ten.svg`.
   - Trong tài liệu Quarto, chú thích hình (`fig-cap`) nêu thông điệp; nguồn ghi dưới biểu đồ. Bài tiếng Anh: `vcci.use("en")`, `vcci_setup("en")`, `do vcci_graph.do en`.

4. **Tự kiểm tra:** xem ảnh từng trang PDF (bìa, bảng dài, biểu đồ, chú thích cuối trang). Không viết chữ trong định dạng mã (`` `...` ``) vì Lora và Be Vietnam Pro không có font đơn cách; tên hàm viết như chữ thường.

## Báo cáo lại cho người dùng

Đường dẫn file kết quả (`.docx`/`.pptx` và `.pdf`), những gì đã đổi về cấu trúc (slide tách, biểu đồ dựng lại, chương thêm), những gì giữ nguyên dạng ảnh, và những chỗ `[cần bổ sung]`. **Không bịa nội dung**: thiếu thông tin thì ghi `[cần bổ sung]`.

## Quy tắc thương hiệu bắt buộc

- Logo chỉ có một phiên bản màu: chữ VCCI Blue #264896, trống đồng giữ màu gốc, trên nền sáng. **Không** dùng logo chữ trắng (kiêng kị văn hóa), logo chữ vàng, hay trống đồng đứng riêng. Trên nền tối, logo đặt trên ô nền sáng Paper #FBF9F4. Template đã đặt sẵn logo; không thêm hay sửa logo.
- Font: Lora cho tiêu đề, Be Vietnam Pro cho nội dung. Không định dạng thủ công.
- Màu chỉ lấy từ bảng màu VCCI (`brand-assets/brand-tokens.json`). Mỗi trang, mỗi slide chỉ **một điểm nhấn vàng** #FFCD00.
- Biểu đồ: màu chuỗi theo thứ tự trong `dataviz` của `brand-tokens.json` (VCCI Blue, Sky, Drum Bronze, Slate, Bronze 20, Deep Navy); vàng chỉ nhấn một giá trị; trục cột bắt đầu từ 0; màu trạng thái (lỗi, cảnh báo, thành công) không dùng làm màu chuỗi.
- Thông số đầy đủ ở `brand-assets/07_Guidelines/VCCI_Huong-dan-Nhan-dien-Thuong-hieu_v1.1.pdf`.

## Phạm vi hiện tại

Có script cho **báo cáo Word** và **bài trình bày PowerPoint**; extension Quarto cho **báo cáo, working paper, tờ trình**; theme biểu đồ cho **matplotlib, ggplot2, Stata**. Thư, công văn (`VCCI_Letterhead.dotx`) và thư mời (`VCCI_Invitation.dotx`) có trong `brand-assets/06_Templates/` để dùng thủ công.
