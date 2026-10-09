# Markdown cho báo cáo VCCI (`render_report.py`)

Mỗi cú pháp dưới đây ánh xạ vào một style có sẵn trong `VCCI_Report.dotx`. Không có cú pháp cho màu, font hay cỡ chữ: template quyết định toàn bộ.

## Phần đầu file (front matter)

```yaml
---
title: Báo cáo thường niên Môi trường kinh doanh 2026     # bìa: tên báo cáo (tối đa ba dòng)
subtitle: Đánh giá của 12.500 doanh nghiệp ...           # bìa: tiêu đề phụ (bỏ dòng nếu không có)
date: Tháng 10 / 2026                                    # bìa: thời gian; năm cũng dùng cho nhãn bìa và đầu trang
author: Trương Đức Trọng                                 # bìa: tác giả (bỏ dòng nếu không có)
unit: Ban Pháp chế                                       # bìa: đơn vị thực hiện (bỏ dòng nếu không có)
contact: "Đầu mối: Nguyễn Văn A · a@vcci.com.vn"         # bìa sau: đầu mối liên hệ (bỏ dòng = không in)
icon: 21                                                 # bìa: hero icon, số 1–24 hoặc tên (research-index); none = bỏ icon
header: Môi trường kinh doanh 2026                       # đầu trang thân bài (mặc định = title)
label: Báo cáo  ·  Report  ·  2026                       # tùy chọn: nhãn nhỏ trên bìa (ví dụ "Tham luận hội thảo")
toc: true                                                # false = bỏ trang mục lục
chapter_break: true                                      # false = chương mới không sang trang
---
```

## Khối nội dung

| Markdown | Kết quả trong Word |
|---|---|
| `# Tên chương` | Nhãn "CHƯƠNG 01" + Heading 1 + gạch vàng; mỗi chương bắt đầu trang mới |
| `# Phụ lục {label="Phụ lục A"}` | Đổi nhãn chương; `{.nolabel}` để bỏ nhãn |
| `## …`, `### …` | Heading 2, Heading 3 (vào mục lục) |
| đoạn văn thường | Normal (Be Vietnam Pro 10 pt) |
| `::: lead` … `:::` | VCCI Lead: đoạn dẫn ngay sau tên chương, 2–3 câu, **tối đa khoảng 70 từ**; đoạn dài hơn để làm thân bài |
| `::: callout` … `:::` | VCCI Callout: hộp nền xanh nhạt; **tối đa một hộp mỗi trang** |
| `::: small` … `:::` | VCCI Small: ghi chú, chức danh, nơi nhận |
| `::: figures` + dòng `giá trị \| nhãn` + `:::` | Khối số liệu nổi bật (VCCI Table Tint), tối đa 4 ô |
| `> Trích dẫn` rồi dòng `— Họ tên, chức danh` | Quote (viền trái vàng) + dòng ghi nguồn |
| `- ý` / `1. bước` (thụt 2 dấu cách = cấp 2) | Danh sách VCCI; mỗi danh sách số bắt đầu lại từ 1 |
| `Bảng: Tên bảng` ngay trên bảng | Chú thích "Bảng N." tự đánh số |
| `Hình: Tên hình` ngay trên bảng | Bảng được đánh số như hình ("Hình N."), khi bản gốc gọi bảng đó là hình |
| `::: note` … `:::` ngay dưới bảng hoặc hình | Dòng "Nguồn: …" hoặc "Ghi chú: …" cỡ nhỏ |
| `::: references` … `:::` | Danh mục tài liệu tham khảo: mỗi đoạn một mục, thụt treo |
| bảng `\| … \|` | VCCI Table; số tự căn phải; hàng đầu là tiêu đề |
| `{.light}` cuối dòng `Bảng:` | VCCI Table Light (bảng mô tả, danh mục) |
| `{.total}` | Hàng cuối là hàng tổng (nền Ivory) |
| `{.banded}` | Bật sọc xen kẽ (bảng dài trên 12 dòng) |
| `{widths=3,1,1}` | Tỉ lệ độ rộng cột |
| `![Tên hình  ·  Nguồn: …](media/a.png)` | Ảnh rộng bằng khối chữ + chú thích "Hình N." |
| `![…](a.png){width=60%}` hoặc `{.natural}` | Ảnh hẹp hơn / giữ kích thước gốc |
| `**đậm**`, `*nghiêng*`, `[chữ](https://…)` | Đậm, nghiêng, liên kết |
| `[^1]` và dòng `[^1]: nội dung` | Chú thích cuối trang thật của Word |
| `\pagebreak` | Ngắt trang |

Trong ô bảng, dùng `<br>` để xuống dòng. Ô chỉ chứa `<<` được gộp vào ô bên trái (ô gộp ngang); `extract_docx.py` tự sinh ký hiệu này.
Chú thích hình, bảng được đánh số lại theo thứ tự xuất hiện: giữ thứ tự như bản gốc để các tham chiếu "Hình 2", "Bảng 1" trong văn bản vẫn đúng.

## Quy tắc biên tập

- Chỉ **một điểm nhấn vàng** mỗi trang: gạch vàng dưới tên chương đã là điểm nhấn, nên không thêm màu vàng ở chỗ khác.
- Không bịa số liệu, nguồn hay trích dẫn. Nếu bản thô thiếu tên bảng, nguồn hay chú thích hình, để `[cần bổ sung]` và báo lại người dùng.
- Giữ nguyên nội dung và thứ tự của bản thô. Chỉ đổi cấu trúc (chia chương, đoạn dẫn, hộp nhấn mạnh) và chỉ sửa câu chữ khi người dùng yêu cầu.
- Biểu đồ: nếu cần vẽ lại, dùng màu chuỗi theo đúng thứ tự VCCI Blue #264896, Sky #8FA6D6, Drum Bronze #CC713C, Slate #5C6478, Bronze 20 #F2B18E, Deep Navy #0B1A4F (tối đa 6 chuỗi). Vàng #FFCD00 chỉ để nhấn **một** giá trị, kèm nhãn số. Số liệu theo tỉnh, vùng dùng thang tuần tự xanh; tăng/giảm quanh một mốc dùng thang phân kỳ đồng–xanh. Trục cột bắt đầu từ 0, ghi nguồn dưới biểu đồ. Mã màu đầy đủ ở mục `dataviz` của `brand-assets/brand-tokens.json`; quy tắc ở phần 08 của hướng dẫn thương hiệu.

## Hero icon trên bìa

| Số | Tên | Số | Tên |
|---|---|---|---|
| 1 | legislative-input | 13 | membership |
| 2 | local-economic-governance | 14 | trade-promotion |
| 3 | business-environment-reform | 15 | trade-fair |
| 4 | administrative-reform | 16 | investment |
| 5 | international-integration | 17 | arbitration |
| 6 | public-private-dialogue | 18 | training |
| 7 | certificate-of-origin | 19 | export-logistics |
| 8 | sme | 20 | forum-events |
| 9 | private-sector-development | 21 | research-index |
| 10 | enterprise-productivity | 22 | employers-labour |
| 11 | enterprise-green-transition | 23 | networking-partnership |
| 12 | enterprise-digital-transition | 24 | business-advisory |

Chọn icon gần nhất với chủ đề chính của tài liệu. Hình vẽ: `brand-assets/05_Icons/Sheets/`.

