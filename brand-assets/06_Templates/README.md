# Template Word và PowerPoint VCCI — v1.1

| File | Dùng cho | Cấu trúc |
|---|---|---|
| `Word/VCCI_Letterhead.dotx` | Thư, công văn, thư ngỏ | Trang 1 có tiêu đề thương hiệu đầy đủ, khối địa chỉ và hình chìm trống đồng. Từ trang 2 trở đi có tiêu đề rút gọn và số trang. |
| `Word/VCCI_Report.dotx` | Báo cáo, đề xuất, ấn phẩm nghiên cứu | Bìa trước, mục lục, thân bài (chương, bảng, biểu đồ, trích dẫn, hộp nhấn mạnh), bìa sau |
| `Word/VCCI_Invitation.dotx` | Thư mời sự kiện | Một trang: tên sự kiện, khách mời, bảng thông tin có icon, chương trình, chữ ký |

Bản xem trước PDF nằm trong `Word/Previews/`.

## Cách dùng

1. **Nhấp đúp** vào file `.dotx`. Word sẽ mở một **tài liệu mới** dựa trên mẫu, còn file mẫu gốc giữ nguyên.
2. Thay mọi nội dung trong `[ngoặc vuông]`.
3. Chỉ định dạng bằng **Styles** (Home → Styles), không định dạng thủ công:

| Style | Dùng cho |
|---|---|
| Title / Subtitle | Tên và tiêu đề phụ trên bìa |
| VCCI Label | Nhãn nhỏ viết hoa màu nâu đồng (ví dụ "CHƯƠNG 01", "V/V") |
| Heading 1 / 2 / 3 | Ba cấp tiêu đề; tự động đưa vào mục lục |
| VCCI Lead | Đoạn dẫn đầu chương |
| Normal | Thân bài |
| Quote | Trích dẫn (viền trái vàng) |
| VCCI Callout | Hộp nhấn mạnh nền xanh nhạt (tối đa một hộp mỗi trang) |
| Caption | Chú thích bảng và hình |
| VCCI Small | Chữ nhỏ (chức danh, nơi nhận) |

4. **Mục lục:** sau khi sửa tiêu đề, nhấp chuột phải vào mục lục và chọn *Update Field → Update entire table*.
5. **Icon chủ đề trên bìa báo cáo:** nhấp vào icon, chọn *Change Picture*, rồi chọn icon phù hợp trong `05_Icons/Hero/PNG/Gold-on-dark/` (gợi ý ghép cặp có trong `05_Icons/HANDBACK_TO_CLAUDE.md`).
6. **Bảng:** cả ba template có sẵn 3 kiểu bảng. Bảng mới chèn (*Insert → Table*) tự động dùng **VCCI Table**. Để đổi kiểu: nhấp vào bảng, mở tab *Table Design*, chọn kiểu trong gallery (nhóm *Custom*).

| Kiểu bảng | Dùng cho | Tùy chọn nên bật trong *Table Style Options* |
|---|---|---|
| **VCCI Table** | Bảng số liệu: hàng tiêu đề nền xanh chữ trắng, kẻ ngang mảnh, gạch xanh dưới bảng, hàng tổng nền Ivory | Header Row, Total Row (khi có hàng tổng); tắt Banded Rows. Bật Banded Rows nếu bảng dài trên 12 dòng. |
| **VCCI Table Light** | Bảng mô tả, danh mục, chương trình: nhãn tiêu đề chữ in hoa màu nâu đồng, cột đầu chữ đậm màu xanh, không tô nền | Header Row, First Column |
| **VCCI Table Tint** | Khối số liệu nổi bật, ghi chú: ô nền xanh nhạt, ngăn bằng khe trắng | Tắt hết |

Số liệu trong bảng nên căn phải (Ctrl + R). Không tự kẻ thêm viền hay tô màu ô: mọi định dạng đã có trong kiểu bảng.

## Font

Hai font Lora và Be Vietnam Pro đã được **nhúng sẵn** trong template, nên máy chưa cài font vẫn hiển thị đúng. Để soạn thảo thoải mái (nhất là chữ đậm, nghiêng và gõ tiếng Việt), nên cài font từ `03_Fonts/`. Khi lưu tài liệu để gửi đi, giữ tùy chọn *File → Options → Save → Embed fonts in the file*.

## Quy tắc giữ nhất quán

- Không thay logo, không đặt logo trực tiếp lên nền xanh hoặc nền ảnh. Phần đầu trang và bìa sau đã được dựng đúng quy tắc.
- Mỗi trang chỉ có **một điểm nhấn vàng** (gạch vàng dưới tiêu đề chương, một số liệu, hoặc icon).
- Màu chữ chỉ dùng trong bảng màu VCCI. Muốn dùng màu VCCI ở các tài liệu khác, cài bộ theme màu theo hướng dẫn trong `../README.md`.

## PowerPoint: `PowerPoint/VCCI_Presentation.potx`

Khổ 16:9, một file có cả layout nền sáng và nền xanh, font đã nhúng. Nhấp đúp để tạo bài trình bày mới; file mở ra với 17 slide mẫu, mỗi slide minh họa một layout và có ghi chú cách dùng trong phần *Notes*. Xóa các slide không cần, rồi thêm slide mới bằng *Home → New Slide*.

| Nền | Layout | Dùng khi |
|---|---|---|
| Sáng | 01 Bìa sáng | Họp, làm việc với đối tác, bài gửi đọc |
| Sáng | 02 Chương trình | Chương trình sự kiện, mục lục |
| Sáng | 03 Tiêu đề và nội dung · 04 Hai cột · 05 So sánh | Nội dung chính (chữ 18 pt) |
| Sáng | 06 Nội dung dày | Bài gửi qua email để tự đọc (chữ 14 pt); không dùng trên sân khấu |
| Sáng | 07 Biểu đồ và bảng | Biểu đồ hoặc bảng, kèm thông điệp bên phải và dòng nguồn |
| Sáng | 08 Ảnh và chữ · 09 Diễn giả | Ảnh thật; giới thiệu 2–4 diễn giả |
| Sáng | 10 Chỉ có tiêu đề · 11 Trống | Bố cục tự do |
| Xanh | 12 Bìa sự kiện | Sân khấu, màn hình LED (logo trên ô nền sáng) |
| Xanh | 13 Chuyển chương | Mở đầu mỗi phần; có hiệu ứng Fade và vị trí hero icon |
| Xanh | 14 Số liệu nổi bật · 15 Tuyên bố lớn · 16 Trích dẫn | Tạo nhịp, nhấn mạnh thông điệp |
| Xanh | 17 Ảnh toàn khung | Ảnh lớn kèm dải chú thích |
| Xanh | 18 Kết thúc | Lời cảm ơn, logo, thông tin liên hệ |

- **Chân trang:** *Insert → Header & Footer*, nhập tên bài trình bày vào ô *Footer*, đánh dấu *Slide number*, chọn *Apply to All*. Bìa, ảnh toàn khung và slide kết thúc không có chân trang.
- **Hero icon ở slide chuyển chương:** nhấp chuột phải vào icon → *Change Picture* → chọn file trong `05_Icons/Hero/PNG/Gold-on-dark/`.
- **Ảnh:** nhấp vào biểu tượng trong khung ảnh để chèn; ảnh tự cắt vừa khung. Chỉ dùng ảnh thật.
- **Biểu đồ:** biểu đồ tự lấy màu theme theo thứ tự VCCI Blue, Sky, Nâu đồng, Slate, Bronze 20 (chuỗi thứ sáu đổi tay sang Deep Navy). Vàng không phải màu chuỗi: muốn nhấn một giá trị, tô riêng cột đó màu vàng (Accent 6) và giữ nhãn số. Trục cột bắt đầu từ 0. Template Word cũng dùng theme này nên biểu đồ chèn trong Word lấy cùng thứ tự màu.
- **Số liệu nổi bật:** chỉ con số đầu tiên màu vàng (quy tắc một điểm nhấn vàng).
- **Bảng:** kiểu bảng mặc định của PowerPoint đã lấy màu xanh VCCI. Để giống mẫu, tô hàng tiêu đề màu xanh, hàng tổng màu Ivory, và chỉ giữ đường kẻ ngang.
- **Hiệu ứng:** chỉ slide chuyển chương có Fade; không thêm hiệu ứng cho các slide khác.

## Theme biểu đồ (thư mục `Charts/`)

Theme cho matplotlib (`vcci_charts.py`, `vcci.mplstyle`), ggplot2 (`theme_vcci.R`) và Stata (`scheme-vcci.scheme`, `vcci_graph.do`): biểu đồ vẽ bằng mã có cùng màu chuỗi, chữ, lưới và dấu phẩy thập phân như biểu đồ trong Word và PowerPoint. Cách dùng: `Charts/README.md`. Các file này được sinh từ `brand-tokens.json` bằng `python quarto-vcci/build.py`; không sửa tay.

## Dựng lại template

- Word: `python tools/build.py word` (đóng Word trước khi chạy).
- PowerPoint: `python tools/build.py ppt` (đóng PowerPoint trước khi chạy).

Xem thêm `tools/README.md` ở thư mục gốc của repo.
