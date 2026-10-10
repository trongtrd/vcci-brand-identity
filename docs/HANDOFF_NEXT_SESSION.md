# Bàn giao cho phiên làm việc mới

**Dự án:** Bộ nhận diện thương hiệu VCCI (Liên đoàn Thương mại và Công nghiệp Việt Nam)
**Chủ dự án:** Truong Duc Trong. Trao đổi bằng **tiếng Việt**.
**Trạng thái (10/10/2026):** v1.1 của bộ nhận diện đã duyệt (thêm Sky, thang sắc độ, màu trạng thái, chương Dữ liệu và biểu đồ, theme màu Office mới). Extension Quarto `quarto-vcci/` xong cả bước 0–6: báo cáo, working paper, tờ trình; theme biểu đồ cho Python, R, Stata; font JetBrains Mono cho mã. Bản 1.0.0 đã phát hành tại [trongtrd/vcci-quarto](https://github.com/trongtrd/vcci-quarto) (công khai); repo đổi tên từ `quarto-vcci` ngày 10/10/2026 (GitHub chuyển hướng tên cũ), còn thư mục nguồn trong repo này vẫn là `quarto-vcci/` vì trang 34 của tài liệu hướng dẫn nhắc tên thư mục đó, sinh bằng `quarto-vcci/release.py`; bản sao làm việc của repo phát hành ở `C:\GitHub Projects\vcci-quarto`. Hướng dẫn thương hiệu 37 trang. Repo bộ nhận diện này: [trongtrd/vcci-brand-identity](https://github.com/trongtrd/vcci-brand-identity) (công khai), nhánh `main`. Xem `docs/PLAN_QUARTO_VCCI.md` (mục 10–15) và `quarto-vcci/README.md`.

---

## 1. Đọc trước khi làm bất cứ việc gì

1. `README.md`: tổng quan, cấu trúc repo, năm quy tắc cốt lõi.
2. `docs/DECISIONS.md`: **mọi quyết định đã chốt**, kèm lý do. Không thay đổi các quyết định này nếu chủ dự án chưa đồng ý.
3. `tools/README.md`: cách dựng lại sản phẩm.
4. `brand-assets/07_Guidelines/VCCI_Huong-dan-Nhan-dien-Thuong-hieu_v1.1.pdf`: hướng dẫn thương hiệu dành cho người dùng cuối.

## 2. Đã hoàn thành

| Sản phẩm | Vị trí | Ghi chú |
|---|---|---|
| Logo vector giải mã từ file CorelDRAW gốc | `brand-assets/01_Logo` | SVG, PNG, PDF; 6 phiên bản (chính, ô nền sáng, lockup ngang và đứng song ngữ) |
| Màu | `brand-assets/02_Colour` | Office theme, ASE, CSS, JSON |
| Font | `brand-assets/03_Fonts` | Lora, Be Vietnam Pro; JetBrains Mono chỉ cho mã nguồn (đều OFL) |
| Họa tiết trống đồng | `brand-assets/04_Graphics` | 5 họa tiết |
| Bộ icon v1 | `brand-assets/05_Icons` | 48 UI (dựa trên Lucide) và 24 hero; do agent ChatGPT làm theo `docs/handoff-icons/` |
| Template Word | `brand-assets/06_Templates/Word` | Letterhead, Báo cáo, Thư mời; kiểu bảng VCCI Table / Light / Tint; font nhúng |
| Skill cho AI agent `vcci-brand` | `skills/vcci-brand`, `.claude-plugin/`, `AGENTS.md` | Word thô → báo cáo VCCI; PowerPoint thô hoặc dàn ý → bài trình bày VCCI (extract → biên tập Markdown → render → finalize). Đã thử với một tham luận và một bài trình bày thật, cùng hai ví dụ giả lập (06/10/2026) |
| Template PowerPoint | `brand-assets/06_Templates/PowerPoint` | 16:9, 18 layout, 17 slide mẫu, font nhúng |
| Hướng dẫn thương hiệu | `brand-assets/07_Guidelines` | PDF 37 trang, tiếng Việt, A4 ngang; trang 34 về Quarto và biểu đồ |
| Extension Quarto `quarto-vcci` | `quarto-vcci/` | `vcci-report`, `vcci-wp`, `vcci-memo`; PDF bằng Typst và Word; mẫu trong `templates/`, kết quả trong `examples/`; bộ kiểm thử 8 lớp (`tests/run_tests.py`) |
| Theme biểu đồ | `quarto-vcci/charts/`, bản sao ở `brand-assets/06_Templates/Charts/` | matplotlib, ggplot2, Stata; sinh từ `brand-tokens.json` bằng `quarto-vcci/build.py` |
| Bảng nhận diện (poster) | `board/` | HTML và bản xuất PNG 2×, PDF, ảnh xem trước |

## 3. Quy tắc bắt buộc (tóm tắt từ DECISIONS.md)

- Logo chỉ một phiên bản màu: chữ **VCCI Blue #264896 (CMYK 100/80/0/0)**, trống đồng màu gốc, trên nền sáng.
- **Không bao giờ** dùng logo chữ trắng (kiêng kị văn hóa), logo chữ vàng, hay trống đồng đứng riêng thay logo. Trên nền tối, đặt logo trên **ô nền sáng** (Paper #FBF9F4, lề trong x = bán kính trống ≈ 0,26 chiều cao chữ).
- Bản logo đỏ không thuộc hệ thống.
- VCCI **không** bị ràng buộc bởi Nghị định 30/2020; được thiết kế tự do.
- Không sao chép tài sản thương hiệu của tổ chức khác (ví dụ ANU); chỉ tham khảo cách tổ chức.
- VCCI đã cho phép chia sẻ công khai repo này.

## 4. Môi trường và lưu ý kỹ thuật

- Windows, thư mục dự án nằm trong **Dropbox**. Dropbox thỉnh thoảng khóa thư mục khi đang đồng bộ, khiến lệnh xóa hoặc di chuyển báo "busy"; chờ một lát rồi thử lại.
- Chạy mọi lệnh từ **thư mục gốc repo**: `python tools/build.py all` hoặc từng bước `logo | assets | board | word | ppt | guide`.
- Bước `word` và `ppt` điều khiển Word và PowerPoint qua COM. Script **tự dừng nếu người dùng đang mở tài liệu**. Không được tắt các tiến trình Office có cửa sổ của người dùng.
- Khi xuất PDF ở chế độ nền, Word có thể crash lúc đóng một tài liệu có mục lục đã cập nhật. PDF vẫn được tạo; script đã xử lý trường hợp này.
- **Font Lora và Be Vietnam Pro đã được cài trên máy này**, nên việc nhúng font chưa được kiểm chứng trên máy không có font.
- Với pptxgenjs, tên slide master phải là **ASCII**. Tên có dấu làm hỏng tên file ảnh bên trong file và PowerPoint sẽ từ chối mở. Tên tiếng Việt được gán lại trong `tools/ppt/finalize.py`, theo `tools/ppt/layout_names.json`.
- `build/` là thư mục trung gian, git bỏ qua. `.statamcp/` là log debug do máy chủ MCP Stata tự tạo; vô hại, git bỏ qua, có thể xóa.
- Phần mềm cho `quarto-vcci`: Quarto 1.9 (có Typst), Python 3.14 (matplotlib, Jupyter, fontTools, PyMuPDF), R 4.6.1 (ggplot2 4.0, svglite, ragg, systemfonts; chưa có reticulate), Stata MP 19 (`C:\Program Files\StataNow19\StataMP-64.exe`). Các bẫy kỹ thuật đã gặp ghi ở mục 14 của `docs/PLAN_QUARTO_VCCI.md`.
- `tools/assets/build_assets.py` xóa và dựng lại cả `02_Colour`, nên theme biểu đồ đặt ở `06_Templates/Charts`.
- `example/` chứa tài liệu thật của chủ dự án để thử skill; git bỏ qua, **không** đưa lên GitHub.
- **GitHub CLI** 2.102.0 (`C:\Program Files\GitHub CLI\gh.exe`; terminal mở trước khi cài chưa có trong PATH, trong PowerShell gọi bằng `& "…\gh.exe"`) đã đăng nhập tài khoản `trongtrd`. Git Credential Manager có sẵn; git identity: `Trong Truong <trongtrd@gmail.com>`.

## 5. Việc còn mở

| # | Việc | Ghi chú |
|---|---|---|
| 2 | Kiểm tra font nhúng trên máy chưa cài font | Mở các file `.dotx`, `.potx` trên một máy khác. Nếu font bị thay thế, khuyến nghị cài font từ `03_Fonts`. |
| 3 | Chạy lại pipeline icon (`tools/icons`) | Đường dẫn đã được sửa sau khi đổi cấu trúc nhưng chưa chạy lại. Cần thêm `svgpathtools`, `requests` và `sharp`. Không ảnh hưởng bộ icon đã bàn giao. |
| 4 | Xem lại nội dung | Nhờ VCCI duyệt các đoạn định vị và giọng điệu trong hướng dẫn (trang 3–4). Mã Pantone cần nhà in đề xuất từ CMYK. |
| 5 | Mở rộng skill `vcci-brand` | Đã có báo cáo Word, bài trình bày PowerPoint, phần C (Quarto và theme biểu đồ). Tiếp theo: vẽ lại biểu đồ dạng ảnh trong báo cáo Word theo bảng màu VCCI; thư, thư mời. |
| 8 | Thử skill trong Codex và Antigravity | `tools/install_skill.py` cài skill theo thư mục mà tài liệu chính thức của OpenAI (`~/.agents/skills`) và Google (`~/.gemini/config/skills`, `.agents/skills`) ghi (10/2026); đã kiểm bằng `tools/test_install_skill.py` (15/15) nhưng chưa chạy thật trong hai công cụ này vì máy chưa cài. |
| 6 | (Tùy chọn) Mở rộng | Ví dụ template Excel, chữ ký email, nền Zoom/Teams, mẫu bài mạng xã hội, chứng nhận. |

## 6. Cách làm việc đã thống nhất với chủ dự án

- Trả lời bằng tiếng Việt, ngắn gọn, nêu rõ việc gì đã kiểm chứng và việc gì chưa.
- Với yêu cầu lớn hoặc chưa rõ, **hỏi trước** (chủ dự án thích hình thức hỏi theo vòng, mỗi câu kèm khuyến nghị).
- Sau mỗi thay đổi hình ảnh: render lại và tự xem kết quả trước khi báo cáo.
- Chỉ commit hoặc push khi chủ dự án yêu cầu, hoặc khi chủ dự án đã duyệt bước đó.
- Mỗi kiểm tra tự động mới phải kèm một tài liệu cố tình lỗi trong `quarto-vcci/tests/selftest/`.
- Tải file từ Internet: hỏi trước, tải vào thư mục riêng, đọc rồi mới dùng.
