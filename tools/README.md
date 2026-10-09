# Công cụ dựng

Mọi lệnh chạy từ **thư mục gốc của repo**. File trung gian được ghi vào `build/` (không đưa lên git); sản phẩm được ghi vào `brand-assets/` và `board/export/`.

```bash
python tools/build.py all            # toàn bộ
python tools/build.py assets guide   # một số bước
```

| Bước | Script | Đầu vào | Đầu ra | Cần |
|---|---|---|---|---|
| `logo` | `cdr/decompress.py`, `cdr/mkvector.py` | `source/logo/Logo_VCCI.cdr` | `build/logo/vcci-logo.svg`, `vcci-drum.svg` | Python |
| `assets` | `assets/build_assets.py`, `assets/colour_system.py` | SVG gốc ở trên (nếu chưa có thì dùng bản trong `brand-assets`) | `brand-assets/01_Logo`, `02_Colour`, `04_Graphics` | Edge |
| `board` | `board/render.py` | `board/vcci-brand-board.html` | `board/export/*`, `build/board/rects.json` | Edge |
| `word` | `word/make_art.py`, `word/make_templates.js`, `word/finalize.py` | `brand-assets` | `brand-assets/06_Templates/Word/*` | Node.js, Word, Poppler |
| `ppt` | `ppt/make_art.py`, `ppt/make_pptx.js`, `ppt/finalize.py` | `brand-assets` | `brand-assets/06_Templates/PowerPoint/*` | Node.js, PowerPoint |
| `guide` | `guide/prepare_images.py`, `guide/make_guide.py` | bảng nhận diện, template, `brand-assets` | `brand-assets/07_Guidelines/*.pdf` | Edge, Poppler |

## Hệ màu mở rộng

`assets/colour_system.py` tính thang sắc độ (trong không gian OKLCH, theo độ sáng tương đối WCAG), màu trạng thái và màu biểu đồ, rồi kiểm tra mọi cặp màu theo quy tắc trừ cấp độ. Chạy riêng để xem bảng và kết quả kiểm tra: `python tools/assets/colour_system.py`. `python tools/assets/build_assets.py colours` chỉ tạo lại `02_Colour` (không cần Edge) và báo lỗi nếu `brand-tokens.json` (sửa tay) lệch với giá trị tính ra.

## Chương trình bên ngoài

`tools/env.py` tự tìm Microsoft Edge và `pdftoppm`. Nếu cần chỉ định khác, đặt biến môi trường `VCCI_EDGE` và `VCCI_PDFTOPPM`.

Script `word/finalize.py` và `ppt/finalize.py` điều khiển Word và PowerPoint qua COM. **Hãy đóng Word và PowerPoint trước khi chạy**; script sẽ dừng lại nếu phát hiện có tài liệu đang mở.

## Ghi chú kỹ thuật

- **Logo từ CorelDRAW:** file `.cdr` (X3) là RIFF nén zlib. `cdr/parse.py` đọc cây chunk, `cdr/tosvg.py` giải mã đường cong (`loda`), ma trận (`trfd`) và màu tô (`fild`), `cdr/mkvector.py` chuẩn hóa thành SVG với chiều cao chữ bằng 1000 đơn vị.
- **Word:** font được nhúng theo chuẩn ECMA-376 (font obfuscated), kiểu bảng VCCI được chèn vào `styles.xml` (`word/table_styles.py`).
- **PowerPoint:** tên slide master trong pptxgenjs phải là ASCII, vì thư viện đặt tên file ảnh theo tên master. Tên layout tiếng Việt được gán lại ở bước `finalize` (`ppt/layout_names.json`).

## Bộ icon (`tools/icons/`)

Pipeline riêng do agent ChatGPT viết khi làm bộ icon v1. Kết quả đã được duyệt và nằm trong `brand-assets/05_Icons`; chỉ chạy lại khi cần sửa icon. Đường dẫn đã được cập nhật theo cấu trúc repo mới nhưng pipeline **chưa được chạy lại** sau khi chuyển thư mục; thứ tự dưới đây là thứ tự tham khảo.

```bash
python tools/icons/build_icons.py    # dựng SVG vào build/icons/review
node tools/icons/render.cjs          # xuất PNG và ảnh QA (cần sharp)
python tools/icons/validate.py
python tools/icons/sheets.py
python tools/icons/finalize.py       # đóng gói vào build/icons/final
```
