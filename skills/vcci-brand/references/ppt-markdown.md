# Markdown cho bài trình bày VCCI (`render_deck.py`)

Một file Markdown là một bài trình bày. Bìa và slide kết thúc được dựng từ phần đầu file; `#` là slide chuyển chương; `##` là một slide. Không có cú pháp cho màu, font hay vị trí: template và script quyết định.

## Phần đầu file

```yaml
---
title: Chất lượng điều hành kinh tế tỉnh Lạng Sơn       # bìa
subtitle: Góc nhìn từ PCI 2025                          # bìa (bỏ dòng nếu không có)
presenter: Họ tên · chức danh · sự kiện · ngày           # dòng nhỏ cuối bìa
footer: Tên ngắn · PCI 2025                              # chân mọi slide nội dung (kèm số trang)
cover: light                                             # light = "01 Bìa sáng" (họp, gửi đọc); event = "12 Bìa sự kiện" (sân khấu); none = không bìa
end_title: Cảm ơn                                        # slide kết thúc (mặc định "Cảm ơn")
end_subtitle: Thank you                                  # (mặc định "Thank you")
contact: Họ tên · email                                  # thêm vào khối liên hệ; nhiều dòng ngăn bằng |
end: true                                                # false = không có slide kết thúc
---
```

## Slide chuyển chương

```markdown
# Kết quả tổng quan {icon=21}

Dòng phụ đề (tùy chọn), ví dụ tiếng Anh hoặc câu hỏi của phần này.
```

Số chương tự đánh 01, 02… (`{number=A}` để đổi). `icon` là hero icon 1–24 (bảng trong [word-markdown.md](word-markdown.md)). Slide chuyển chương có hiệu ứng Fade.

## Slide nội dung

```markdown
## Tiêu đề slide: một thông điệp, tối đa hai dòng {label="Giai đoạn 1 · Gia nhập thị trường"}
```

`label` là nhãn nhỏ chữ in hoa màu nâu đồng phía trên tiêu đề. Các thuộc tính khác: `{layout=…}` để chọn layout, `{.statement}` cho slide tuyên bố lớn, `{.dense}` cho slide nhiều chữ.

Script tự chọn layout theo nội dung:

| Nội dung slide | Layout |
|---|---|
| chỉ đoạn văn, gạch đầu dòng | 03 Tiêu đề và nội dung (18 pt); trên ~90 từ: 06 Nội dung dày (14 pt, hai cột) |
| hai khối `::: col` | 04 Hai cột |
| `::: left {title="TRƯỚC"}` + `::: right {title="SAU"}` | 05 So sánh |
| `::: agenda` | 02 Chương trình |
| một `::: chart` + chữ (đoạn, gạch đầu dòng, `::: figures`) | 07 Biểu đồ và bảng: biểu đồ bên trái, chữ bên phải |
| `{.statement}` | 15 Tuyên bố lớn (nền xanh): tiêu đề là câu tuyên bố, đoạn văn là dòng phụ |
| chỉ một trích dẫn `>` | 16 Trích dẫn (nền xanh) |
| `::: figures` + `{.dark}` | 14 Số liệu nổi bật (nền xanh, tối đa 3 số, số đầu màu vàng) |
| ảnh `{.full}` | 17 Ảnh toàn khung; ảnh `{.photo}` + chữ: 08 Ảnh và chữ |
| mọi trường hợp khác | 10 Chỉ có tiêu đề, các khối xếp từ trên xuống |

`{layout=content|dense|two|compare|agenda|chart|title|statement|quote|figures-dark|image|fullimage}` để chọn tay.

## Các khối

| Markdown | Kết quả |
|---|---|
| `::: lead` | Một câu dẫn dưới tiêu đề (15 pt, màu slate) |
| `::: figures` + dòng `giá trị \| nhãn \| so sánh` | 2–4 thẻ số liệu (số Lora màu xanh, dòng so sánh cỡ nhỏ) |
| `::: chart {type=column}` + bảng | Biểu đồ thật, sửa được số liệu trong PowerPoint (xem dưới) |
| `::: cards` + `### Tiêu đề thẻ` + nội dung | 2–4 thẻ nội dung cạnh nhau |
| `::: steps {title="…"}` + dòng `bước \| mô tả` | Chuỗi bước nối bằng mũi tên |
| `::: note` | Hộp ghi chú nền xanh nhạt, viền trái xanh |
| `::: source` | Dòng nguồn cuối slide |
| `::: notes` | Ghi chú cho người trình bày (Notes) |
| bảng `\| … \|` (dòng `{.total}` ngay dưới bảng: hàng cuối là hàng tổng) | Bảng VCCI: hàng tiêu đề nền xanh, kẻ ngang mảnh, số căn phải |
| `![](media/a.png)` | Ảnh, giữ tỉ lệ, vừa khoảng trống |
| đoạn văn, `- gạch đầu dòng` (thụt 2 dấu cách = cấp 2) | Chữ 16–18 pt |
| `**đậm**`, `*nghiêng*` | Đậm, nghiêng |

### Biểu đồ

```markdown
::: chart {type=barh highlight="Lạng Sơn" title="So sánh với trung vị cả nước"}
| | Tỷ lệ |
|---|---|
| Lạng Sơn | 63,6% |
| Trung vị cả nước | 38,0% |
:::
```

- `type`: `column` (cột), `barh` (thanh ngang), `line`, `stacked`, `pie` (vành khuyên).
- Cột đầu là nhãn; mỗi cột sau là một chuỗi số liệu (nhiều chuỗi thì có chú giải).
- Nhãn số trên biểu đồ giữ đúng cách viết trong bảng (dấu phẩy thập phân, dấu +, %). `unit=%` thêm % khi bảng chỉ ghi số.
- Màu: một chuỗi màu xanh VCCI. Nhiều chuỗi: chuỗi **cuối cùng** (thường là năm mới nhất) màu xanh đậm, các chuỗi trước lần lượt Xanh nhạt, Nâu đồng, Slate. Đặt cột theo thứ tự thời gian để năm mới nhất nổi bật nhất.
- `highlight="nhãn"`: tô **một** giá trị màu vàng (quy tắc một điểm nhấn vàng).
- `.signed`: giá trị âm màu nâu đồng, dương màu xanh (biểu đồ chênh lệch so với trung vị).

## Quy tắc biên tập

- Mỗi slide một thông điệp; tiêu đề là câu nói lên thông điệp đó, tối đa hai dòng.
- Giữ nguyên câu chữ và số liệu của bản gốc. Slide quá nhiều chữ thì tách thành hai slide hoặc dùng `{.dense}`; chỉ rút gọn câu chữ khi người dùng yêu cầu, và khi rút gọn thì đưa bản đầy đủ vào `::: notes`.
- Biểu đồ trong bản gốc vẽ bằng hình (thanh, cột tự vẽ): dựng lại bằng `::: chart` với số liệu đọc từ nhãn trên slide. Biểu đồ dạng ảnh: giữ ảnh và báo lại người dùng.
- Không bịa số liệu, nguồn hay chú thích. Thiếu thì ghi `[cần bổ sung]` và báo lại.
- Chỉ một điểm nhấn vàng mỗi slide: gạch vàng dưới tiêu đề đã có sẵn, nên chỉ dùng `highlight` khi thật cần.
