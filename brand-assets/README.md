# Bộ tài sản thương hiệu VCCI — v1.0

Liên đoàn Thương mại và Công nghiệp Việt Nam · Vietnam Chamber of Commerce and Industry
Cập nhật: 05/10/2026 · Nguồn gốc logo: `Logo_VCCI.cdr` (CorelDRAW X3), giải mã sang vector SVG.

Thông số máy đọc được (màu, tỉ lệ, kiểu chữ, quy tắc): xem [`brand-tokens.json`](brand-tokens.json).

## Quy tắc bắt buộc về logo

1. **Chỉ một phiên bản màu:** chữ VCCI Blue, trống đồng giữ màu gốc, đặt trên **nền sáng**.
2. Trên nền xanh, nền tối, ảnh hoặc nền nhiều chi tiết: dùng bản **trên ô nền sáng** (`*_Plate`).
3. **Không** dùng logo chữ trắng (kiêng kị văn hóa), **không** chữ vàng, **không** dùng trống đồng đứng riêng để thay logo.
4. Không kéo giãn, xoay, đổi màu, thêm hiệu ứng hay vẽ lại logo.
5. Khoảng trống bảo vệ **x = bán kính trống đồng** (≈ 0,26 chiều cao chữ) ở mọi phía. Ô nền sáng có lề trong bằng x.
6. Cỡ tối thiểu: 25 mm khi in, 96 px trên màn hình.

## Nội dung

| Thư mục | Nội dung | Dùng khi |
|---|---|---|
| `01_Logo/SVG` | Logo chính, bản trên ô nền sáng, lockup ngang song ngữ, lockup đứng tiếng Việt và tiếng Anh | Web, thiết kế, mọi cỡ |
| `01_Logo/PNG` | Như trên, nền trong suốt, rộng 600 / 1200 / 2400 / 4800 px | Word, PowerPoint, mạng xã hội |
| `01_Logo/PDF` | Như trên, vector, khổ rộng 100 mm | Gửi nhà in, chèn vào tài liệu |
| `01_Logo/Source` | File gốc CorelDRAW (CMYK) | **Bản gốc khi in ấn** |
| `01_Logo/_Construction-only` | Trống đồng tách riêng | Chỉ để dựng hình và thiết kế họa tiết; không dùng thay logo |
| `02_Colour` | Bảng màu dạng JSON, CSS, ASE (Adobe), Office theme | Thiết kế, web, Word/PowerPoint |
| `03_Fonts` | Lora, Be Vietnam Pro (giấy phép SIL OFL 1.1, dùng thương mại miễn phí) | Cài vào máy |
| `04_Graphics` | Họa tiết vòng trống, sao 14 cánh, pattern cung chữ C, trường chấm | Bìa, sân khấu, nền trang |
| `05_Icons` | 48 icon nhỏ (UI) và 24 hero icon theo nghiệp vụ VCCI; SVG và PNG; quy cách trong `ICON_SPEC.md` | Tài liệu, slide, web, sự kiện |
| `06_Templates` | Template Word (letterhead, báo cáo, thư mời) và PowerPoint 16:9 (18 layout); đã nhúng font; xem `06_Templates/README.md` | Soạn văn bản, trình chiếu |
| `07_Guidelines` | Hướng dẫn Nhận diện Thương hiệu VCCI v1.0 (PDF, 30 trang, tiếng Việt) | Tham chiếu cho mọi người làm ấn phẩm |

## Màu

| Tên | HEX | CMYK | Vai trò |
|---|---|---|---|
| VCCI Blue | #264896 | 100 · 80 · 0 · 0 | Chính (theo .CDR) |
| Drum Gold | #FFCD00 | 0 · 20 · 100 · 0 | Phụ (theo .CDR) |
| Drum Bronze | #CC713C | 0 · 60 · 80 · 20 | Phụ (theo .CDR), chỉ cho đồ họa và chữ lớn |
| Deep Navy | #0B1A4F | 100 · 90 · 30 · 40 | Nền tối |
| Blue Tint | #E7ECF6 | 8 · 4 · 0 · 0 | Bề mặt giao diện |
| Bronze Ink | #9C570C | 20 · 65 · 100 · 15 | Chữ nhãn cỡ nhỏ |
| Ink / Slate | #161A26 / #5C6478 | | Chữ thân bài / chữ phụ |
| Stone / Ivory / Paper | #E6E1D5 / #F4F0E6 / #FBF9F4 | | Nền trung tính |

Mã HEX được quy đổi từ CMYK gốc theo hồ sơ màu FOGRA39. Khi in, luôn dùng giá trị CMYK. File .CDR không ghi mã Pantone; nếu cần in màu pha, nhờ nhà in đề xuất mã từ CMYK.

## Cài đặt nhanh

- **Font:** mở từng file `.ttf` trong `03_Fonts` rồi chọn *Install for all users*.
- **Màu cho Word/PowerPoint:** chép `02_Colour/VCCI_Office_Theme_Colours.xml` vào `%APPDATA%\Microsoft\Templates\Document Themes\Theme Colors\`, rồi chọn *Design → Colors → VCCI*.
- **Màu cho Adobe:** mở Swatches, chọn *Import Swatches…*, rồi chọn `02_Colour/VCCI_Colours.ase`.

## Ghi chú kỹ thuật

- Vòng ngăn giữa chữ C và trống đồng là **trong suốt**, nên sẽ mang màu nền. Vì logo luôn đặt trên nền sáng hoặc ô nền sáng, vòng này luôn hiện thành một viền sáng.
- Chữ trong các lockup đã được chuyển thành đường vector, nên mở trên máy chưa cài font vẫn hiển thị đúng.
- Toàn bộ gói được tạo lại bằng `python tools/build.py logo assets` (chạy từ thư mục gốc của repo; xem `tools/README.md`).
