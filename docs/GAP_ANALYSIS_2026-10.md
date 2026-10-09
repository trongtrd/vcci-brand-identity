# Đối chiếu bộ nhận diện VCCI với các hệ thống tham chiếu

Ngày: 10/10/2026. Phạm vi: bộ VCCI v1.0 (hướng dẫn PDF 30 trang, `brand-tokens.json`, bảng màu, template, skill `vcci-brand`).

Ba hệ thống tham chiếu:

| Hệ thống | Lý do chọn | Nguồn |
|---|---|---|
| GOV.UK Brand (2025) | Cơ quan công quyền đổi nhận diện gần đây, hướng dẫn dạng website | [brand.design-system.service.gov.uk](https://brand.design-system.service.gov.uk), [alphagov/govuk-brand-assets](https://github.com/alphagov/govuk-brand-assets) |
| IBM Carbon | Chuẩn mực về màu biểu đồ, pictogram, token | [carbondesignsystem.com](https://carbondesignsystem.com/data-visualization/color-palettes/), [carbon-design-system/carbon](https://github.com/carbon-design-system/carbon) |
| USWDS (Mỹ) | Hệ sắc độ màu gắn với độ tương phản, màu trạng thái | [uswds/uswds](https://github.com/uswds/uswds) |

## Những gì VCCI đã ngang tầm

Không cần làm lại các phần sau:

- Logo: dựng hình, khoảng trống bảo vệ, cỡ tối thiểu, các phiên bản, nền, danh sách điều không được làm. Phần này đầy đủ như GOV.UK.
- Quy tắc văn hóa (không dùng logo chữ trắng) được ghi kèm lý do. Đây là cách làm tốt mà nhiều brand book bỏ qua.
- Bảng tương phản WCAG cho các cặp màu chính.
- Giọng điệu: có thang định vị và bảng nên/không nên.
- Icon hai cấp, cùng quy tắc dùng đúng và sai, nhãn chữ, alt text. Cách tổ chức tương tự icon và pictogram của IBM.
- Song ngữ, template thật, skill tự động hóa. Phần này vượt mức thông thường.

## Danh sách còn thiếu, theo mức ưu tiên

> **Cập nhật 10/10/2026:** đã làm xong mục 1, 2 và 3 (bộ nhận diện v1.1). Xem `docs/DECISIONS.md`, phần 03 và 08 của hướng dẫn PDF v1.1. Theme màu Office (Word, Excel, PowerPoint) đã xếp theo thứ tự màu biểu đồ, biểu đồ mẫu trong template đã có trục từ 0. Chủ dự án duyệt ngày 10/10/2026.

### Ưu tiên 1: giá trị cao, làm được ngay, không cần VCCI quyết định thêm

**1. Chương "Dữ liệu và biểu đồ"**
- Tham chiếu: GOV.UK có hẳn mục *Data* (biểu đồ, dashboard, bản đồ). IBM Carbon tách bốn loại bảng màu: phân loại (thứ tự cố định), tuần tự, phân kỳ, trạng thái.
- Hiện trạng VCCI: hướng dẫn chưa có chương này. Thứ tự màu chuỗi chỉ nằm trong code (`render_deck.py`: Blue, Sky, Bronze, Slate; vàng để nhấn một giá trị) và trong ghi chú của skill.
- Vì sao quan trọng: VCCI ra nhiều báo cáo số liệu (PCI, khảo sát doanh nghiệp). Bản đồ 63 tỉnh cần dải màu tuần tự; tăng/giảm cần dải màu phân kỳ. Hiện chưa có cả hai.
- Đề xuất: bổ sung 2–3 trang vào hướng dẫn và thêm vào tokens:
  - Bảng màu phân loại: thứ tự cố định, tối đa 5–6 màu, vàng chỉ dùng để nhấn.
  - Dải màu tuần tự xanh khoảng 7 bậc.
  - Dải màu phân kỳ xanh ↔ đồng, có màu trung tính ở giữa.
  - Quy tắc: không truyền tải thông tin chỉ bằng màu, ghi nguồn, trục cột bắt đầu từ 0, chữ trong biểu đồ dùng Be Vietnam Pro.
  - Bảng "loại quan hệ dữ liệu → loại biểu đồ" (theo GOV.UK).
  - Template biểu đồ cho Excel và PowerPoint.
- Việc này cũng giải quyết việc mở số 5 trong `HANDOFF_NEXT_SESSION.md` (vẽ lại biểu đồ trong báo cáo).

**2. Màu #8FA6D6 chưa được khai báo**
- Hiện trạng: `#8FA6D6` là accent5 trong theme Office (`02_Colour/VCCI_Office_Theme_Colours.xml`) và là màu chuỗi thứ hai của biểu đồ (`SKY` trong `render_deck.py`). Màu này **không có** trong `brand-tokens.json`, CSS, ASE hay hướng dẫn PDF.
- Hệ quả: người làm ấn phẩm chọn được màu này trong Office nhưng không biết nó dùng vào việc gì.
- Đề xuất: đặt tên chính thức (ví dụ "Sky"), ghi vai trò ("chuỗi thứ hai trong biểu đồ, mảng nhạt") và đưa vào mọi định dạng màu. Một việc nhỏ nhưng là lỗi nhất quán.

**3. Thang sắc độ và màu trạng thái**
- Tham chiếu: USWDS đánh số mỗi sắc độ theo độ sáng (0–100). Hai màu chênh nhau từ 50 điểm trở lên thì đạt chuẩn AA cho chữ thường, nên chỉ cần nhìn mã là biết cặp nào dùng được. Cả USWDS và Carbon đều có bộ màu trạng thái (lỗi, cảnh báo, thành công, thông tin).
- Hiện trạng VCCI: mỗi màu chỉ có một sắc độ (riêng xanh có thêm Blue Tint). Chưa có màu trạng thái.
- Hệ quả: website, ứng dụng hội viên, biểu mẫu và báo cáo đánh giá (đạt/không đạt, tăng/giảm) mỗi nơi sẽ tự chọn màu.
- Đề xuất: làm thang 5–7 bậc cho VCCI Blue, Gold và Bronze, đánh số theo độ sáng; thêm 4 màu trạng thái hài hòa với bảng màu; cập nhật bảng tương phản.

### Ưu tiên 2: quan trọng, nhưng cần VCCI quyết định trước

**4. Kiến trúc thương hiệu: chi nhánh, trung tâm, chương trình**
- Tham chiếu: NL Design System (Hà Lan) dùng một khung chung, mỗi tổ chức có bộ token riêng. GOV.UK có "Logo system" cho các đơn vị.
- Hiện trạng VCCI: hướng dẫn chỉ có logo của Liên đoàn. Chưa quy định lockup cho các chi nhánh và văn phòng khu vực, các trung tâm trực thuộc, hay chương trình và sản phẩm mang tên riêng (ví dụ PCI).
- Nếu bỏ trống, mỗi đơn vị sẽ tự ghép tên dưới logo theo cách riêng. Đây là nguồn gây lệch nhận diện lớn nhất ở các tổ chức nhiều đơn vị.
- Cần VCCI quyết định:
  - Danh sách đơn vị.
  - Có cho chương trình dùng logo riêng hay không.
  - Tên đơn vị đặt dưới hay bên phải logo.

**5. Đồng thương hiệu với đối tác**
- Hiện trạng: hướng dẫn mới cấm ghép logo với khẩu hiệu. Chưa có quy tắc khi đặt logo VCCI cạnh logo bộ ngành, nhà tài trợ hay tổ chức quốc tế, dù trường hợp này xảy ra ở hầu hết hội thảo và báo cáo hợp tác.
- Ghi chú: trang GOV.UK không có mục riêng về phần này. Đề xuất dựa trên thông lệ chung của các brand book.
- Đề xuất nội dung:
  - Căn logo theo chiều cao chữ.
  - Có vạch ngăn và khoảng cách bằng x.
  - Thứ tự logo khi VCCI chủ trì và khi VCCI là đối tác.
  - Dải logo đối tác ở chân trang hoặc phông sân khấu.
  - Khi logo đối tác có nền tối: dùng ô nền sáng, giống logo VCCI.

**6. Hướng dẫn dạng website**
- Tham chiếu: GOV.UK công bố hướng dẫn thành website, mỗi mục một trang, có link tải asset và mục "Need help?".
- Hiện trạng VCCI: chỉ có PDF. Riêng bảng nhận diện đã là HTML (`board/`).
- Lợi ích: dễ cập nhật, có link tới từng quy tắc, có thể dẫn thẳng tới file trong `brand-assets/`. PDF vẫn giữ để in và gửi đối tác.
- Cần VCCI quyết định: lưu trữ ở đâu (GitHub Pages, website VCCI hay nội bộ).

### Ưu tiên 3: nâng mức chuyên nghiệp, làm dần

**7. Token theo vai trò và một nguồn duy nhất**
- Hiện trạng: token đang đặt tên theo màu ("VCCI Blue", "Paper"), không theo vai trò ("nền mặc định", "chữ phụ", "nhấn"). Theme Office được viết tay ở hai nơi: `tools/assets/build_assets.py` và `tools/ppt/finalize.py`.
- Đề xuất: chuyển `brand-tokens.json` sang định dạng W3C Design Tokens, thêm lớp token theo vai trò, rồi dùng [Style Dictionary](https://github.com/style-dictionary/style-dictionary) hoặc mở rộng `build.py` để sinh CSS, ASE, Office theme và hằng số Python từ một file.

**8. Ảnh chụp**
- Hiện trạng: hướng dẫn chỉ có một đoạn văn (trang 24).
- Đề xuất: 1–2 trang ảnh mẫu đúng và sai, quy tắc cắt khung, xử lý màu, cách đặt chữ trên ảnh. Cần VCCI cung cấp ảnh có quyền sử dụng.

**9. Quản trị thương hiệu**
- Hiện trạng: hướng dẫn ghi "bộ phận phụ trách thương hiệu" nhưng chưa nêu đầu mối cụ thể. Chưa có nhật ký phiên bản cho người dùng.
- Đề xuất:
  - Ghi tên đơn vị và email đầu mối.
  - Thêm quy trình xin duyệt và xin file.
  - Thêm trang "Thay đổi theo phiên bản" (bắt đầu từ v1.0).

**10. Chuyển động và kênh số**
- Đề xuất: đoạn mở và kết video, thanh tên trên livestream, nền Zoom và Teams, avatar mạng xã hội. Các mục này đã nằm trong việc mở số 6 của `HANDOFF_NEXT_SESSION.md`.

## Trình tự đề xuất

1. Làm mục 2 trước (sửa nhanh), sau đó mục 1 và mục 3. Hai mục này dùng chung thang màu nên nên làm cùng nhau.
2. Hỏi VCCI về mục 4 và 5, rồi bổ sung vào hướng dẫn trong phiên bản 1.1.
3. Mục 6–10 làm theo nhu cầu.
