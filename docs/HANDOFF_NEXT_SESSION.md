# Bàn giao cho phiên làm việc mới

**Dự án:** Bộ nhận diện thương hiệu VCCI (Liên đoàn Thương mại và Công nghiệp Việt Nam)
**Chủ dự án:** Truong Duc Trong. Trao đổi bằng **tiếng Việt**.
**Trạng thái:** v1.0 đã commit (nhánh `main`, chưa có remote). v1.1 (10/10/2026, chủ dự án đã duyệt): thêm Sky, thang sắc độ, màu trạng thái, chương Dữ liệu và biểu đồ (hướng dẫn PDF 36 trang); theme màu Office mới cho template Word và PowerPoint, biểu đồ mẫu trục từ 0. Xem `docs/GAP_ANALYSIS_2026-10.md`.

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
| Font | `brand-assets/03_Fonts` | Lora, Be Vietnam Pro (OFL) |
| Họa tiết trống đồng | `brand-assets/04_Graphics` | 5 họa tiết |
| Bộ icon v1 | `brand-assets/05_Icons` | 48 UI (dựa trên Lucide) và 24 hero; do agent ChatGPT làm theo `docs/handoff-icons/` |
| Template Word | `brand-assets/06_Templates/Word` | Letterhead, Báo cáo, Thư mời; kiểu bảng VCCI Table / Light / Tint; font nhúng |
| Skill cho AI agent `vcci-brand` | `skills/vcci-brand`, `.claude-plugin/`, `AGENTS.md` | Word thô → báo cáo VCCI; PowerPoint thô hoặc dàn ý → bài trình bày VCCI (extract → biên tập Markdown → render → finalize). Đã thử với một tham luận và một bài trình bày thật, cùng hai ví dụ giả lập (06/10/2026) |
| Template PowerPoint | `brand-assets/06_Templates/PowerPoint` | 16:9, 18 layout, 17 slide mẫu, font nhúng |
| Hướng dẫn thương hiệu | `brand-assets/07_Guidelines` | PDF 30 trang, tiếng Việt, A4 ngang |
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
- `example/` chứa tài liệu thật của chủ dự án để thử skill; git bỏ qua, **không** đưa lên GitHub.
- Máy chưa có **GitHub CLI (`gh`)**. Git Credential Manager có sẵn; git identity: `Trong Truong <trongtrd@gmail.com>`.

## 5. Việc còn mở

| # | Việc | Ghi chú |
|---|---|---|
| 1 | **Đưa repo lên GitHub (công khai)** | Chủ dự án sẽ tự làm, hoặc yêu cầu trong phiên mới. Cách làm: tạo repo trống `vcci-brand-identity` trên github.com, chạy `git remote add origin <URL>`, rồi `git push -u origin main`. Lần đầu Git Credential Manager mở cửa sổ đăng nhập để chủ dự án tự đăng nhập. Nếu dùng `gh`, phải cài qua winget và để chủ dự án tự chạy `gh auth login`. |
| 2 | Kiểm tra font nhúng trên máy chưa cài font | Mở các file `.dotx`, `.potx` trên một máy khác. Nếu font bị thay thế, khuyến nghị cài font từ `03_Fonts`. |
| 3 | Chạy lại pipeline icon (`tools/icons`) | Đường dẫn đã được sửa sau khi đổi cấu trúc nhưng chưa chạy lại. Cần thêm `svgpathtools`, `requests` và `sharp`. Không ảnh hưởng bộ icon đã bàn giao. |
| 4 | Xem lại nội dung | Nhờ VCCI duyệt các đoạn định vị và giọng điệu trong hướng dẫn (trang 3–4). Mã Pantone cần nhà in đề xuất từ CMYK. |
| 5 | Mở rộng skill `vcci-brand` | Đã có báo cáo Word và bài trình bày PowerPoint. Tiếp theo: vẽ lại biểu đồ dạng ảnh trong báo cáo theo bảng màu VCCI; thư, thư mời. |
| 6 | (Tùy chọn) Mở rộng | Ví dụ template Excel, chữ ký email, nền Zoom/Teams, mẫu bài mạng xã hội, chứng nhận. |

## 6. Cách làm việc đã thống nhất với chủ dự án

- Trả lời bằng tiếng Việt, ngắn gọn, nêu rõ việc gì đã kiểm chứng và việc gì chưa.
- Với yêu cầu lớn hoặc chưa rõ, **hỏi trước** (chủ dự án thích hình thức hỏi theo vòng, mỗi câu kèm khuyến nghị).
- Sau mỗi thay đổi hình ảnh: render lại và tự xem kết quả trước khi báo cáo.
- Chỉ commit hoặc push khi chủ dự án yêu cầu.
