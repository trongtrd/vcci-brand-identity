# Phát triển quarto-vcci

Tài liệu cho người sửa extension, theme biểu đồ hay bộ kiểm thử. Người dùng xem [README.md](README.md). Kế hoạch và lịch sử quyết định: [docs/PLAN_QUARTO_VCCI.md](../docs/PLAN_QUARTO_VCCI.md).

## Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `src/shared/vcci.typ` | Lớp Typst dùng chung: trang, chữ, tiêu đề, bảng, chú thích, logo, hero icon, vòng trống, gạch vàng, nhãn, đoạn dẫn, hộp nhấn mạnh, thẻ số liệu, hộp `callout` theo màu trạng thái, dấu bản thảo |
| `src/shared/vcci.lua` | Bộ lọc khối `lead`, `highlight`, `label`, `figures` cho Typst và Word; cờ `cover`/`back-cover` |
| `src/formats/<định dạng>/` | `_extension.yml`, `template.typ`, `typst-show.typ` của từng định dạng |
| `src/charts/` | Nguồn theme biểu đồ; `{{…}}` được thay bằng màu và font từ `brand-tokens.json` |
| `charts/`, `brand-assets/06_Templates/Charts/` | Theme biểu đồ **sinh tự động** bằng `build.py`; không sửa tay |
| `_extensions/vcci/<định dạng>/` | **Sinh tự động** bằng `build.py`; không sửa tay |
| `templates/` | Tài liệu mẫu cho người dùng |
| `tests/baseline/` | Ảnh chuẩn đã duyệt của từng trang PDF (lớp 5) |
| `tests/fixtures/` | Tài liệu thử: `minimal` (tối giản), `stress` (tiêu đề ba dòng, bảng 63 dòng qua trang, bảng rộng, trích dẫn, phương trình, đủ loại hộp ghi chú), `code` (mã nguồn), `charts-tools`, `charts-py` (biểu đồ) |
| `tests/selftest/` | Tài liệu cố tình lỗi, để chứng minh bộ kiểm thử bắt được lỗi; `selftest/charts/` cho biểu đồ |
| `tests/charts/` | Bộ biểu đồ mẫu vẽ bằng Python, R và Stata từ cùng số liệu (`data/`) |

`build.py` lấy màu, font, logo, hero icon, họa tiết từ `brand-assets/` và file Word mẫu từ `VCCI_Report.dotx`. Mỗi extension tự chứa đủ (Quarto không cho các extension dùng chung file), nên phần dùng chung được chép vào từng extension. Logo và icon được nhúng thẳng vào mã Typst, nên không có file nào bị chép vào thư mục của người dùng.

## Phát hành

Repo [trongtrd/quarto-vcci](https://github.com/trongtrd/quarto-vcci) là bản sinh ra, không sửa tay. Nó nằm ngoài Dropbox, ở `C:\GitHub Projects\quarto-vcci`.

1. Nâng `version` trong cả ba `src/formats/*/_extension.yml` (SemVer: 1.0.x sửa lỗi, 1.x.0 thêm tùy chọn, x.0.0 đổi khóa YAML hay bố cục) và thêm mục vào `src/release/CHANGELOG.md`.
2. `python quarto-vcci/build.py`, rồi chạy đủ bộ kiểm thử.
3. `python quarto-vcci/release.py --out "C:/GitHub Projects/quarto-vcci"`.
4. Trong repo phát hành: commit, tag `vX.Y.Z`, push; tạo GitHub Release kèm các file `.docx` trong `examples/`.
5. `python quarto-vcci/tests/run_tests.py --install-from trongtrd/quarto-vcci@vX.Y.Z`.

Repo phát hành để extension ở `_extensions/<định dạng>/`, không có cấp `vcci/`. Lý do: `quarto use template` (Quarto 1.9) chỉ đọc `_extensions/<tên>` của repo mẫu; nếu có thêm cấp tổ chức thì nó không cài extension nào. Khi cài từ GitHub, Quarto tự đặt extension vào `_extensions/trongtrd/<định dạng>/`. Tên định dạng (`vcci-report-typst`…) không đổi.

README của bản phát hành chính là `README.md` (viết cho người dùng), bỏ đi các khối nằm giữa `<!-- dev-only -->` và `<!-- /dev-only -->`. Ngoài các khối đó, README không được nhắc `templates/`, `brand-assets`, `DEVELOPMENT.md` hay đường dẫn `../`; khi nâng phiên bản, sửa `@vX.Y.Z` và đường dẫn tải file Word trong README (`release.py` dừng nếu còn số phiên bản cũ). `release.py` dựng ảnh `examples/preview.png` từ các PDF mẫu. `src/release/` chứa `LICENSE.md`, `CHANGELOG.md`, `.quartoignore`.

## Dựng và kiểm thử

Chạy từ thư mục gốc repo:

```bash
python quarto-vcci/build.py
```

```bash
python quarto-vcci/tests/run_tests.py
```

`build.py --check` báo lỗi nếu `_extensions/` lệch với nguồn. `run_tests.py` dựng mọi tài liệu thử và tài liệu mẫu trong thư mục sạch, ở chế độ bỏ qua font hệ thống (giống máy chưa cài font). Các lớp kiểm tra:

1. **Tĩnh:** extension khớp nguồn và `brand-tokens.json`.
2. **Dựng:** dựng thành công, không có cảnh báo nào.
3. **PDF:**
   - Chỉ font thương hiệu, đều được nhúng; khổ **A4**; số trang trong khoảng.
   - Đủ câu yêu cầu và **nhìn thấy được** (chữ bị đẩy ra ngoài trang tính là thiếu).
   - Không chữ nào sát mép giấy hay tràn lề hai bên; không chữ nào đè lên chữ khác.
4. **Word:**
   - Khổ **A4** ở mọi section; mọi style đều được định nghĩa; bảng dùng VCCI Table; font được nhúng.
   - Sau đó Microsoft Word mở file và xuất PDF. PDF đó phải khổ A4, mọi chữ theo font thương hiệu (trừ ký hiệu đầu dòng và phương trình).
   - Lớp này tự bỏ qua khi Word đang mở tài liệu của bạn, hoặc khi chạy với `--no-word`.
5. **So ảnh:** mỗi trang PDF được so với ảnh chuẩn đã duyệt trong `tests/baseline/`, theo từng ô 32 × 32 điểm ảnh (khoảng 16 mm), nên chỉ một từ thay đổi cũng bị phát hiện. Trang lệch thì báo kèm ảnh khác biệt (`diff-*.png`). Thay đổi cố ý đã được duyệt thì chạy lại với `--update-baseline`.
6. **Cài đặt:** xuất repo phát hành (`release.py`) vào thư mục tạm, rồi cài như người dùng bằng `quarto use template` và `quarto add` vào thư mục trống. Phải có đủ tài liệu mẫu và theme biểu đồ; extension giống hệt bản dựng, đúng phiên bản; không có file mà `.quartoignore` loại; mọi mẫu dựng được. `--install-from trongtrd/quarto-vcci@v1.0.0` chạy riêng lớp này với bản trên GitHub.
7. **Tự kiểm:** các tài liệu trong `tests/selftest/` phải bị đúng kiểm tra tương ứng bắt lỗi.
8. **Biểu đồ:**
   - Bộ biểu đồ mẫu (cột có điểm nhấn, đường, cột chồng, phân tán, sáu chuỗi, bảng nhiệt) được vẽ bằng cả ba theme.
   - Từng file SVG phải: chỉ dùng màu VCCI (không màu mặc định, không màu trạng thái); không trong suốt; giữ chữ dạng chữ, bằng font thương hiệu; có tiêu đề tiếng Việt; dùng dấu phẩy thập phân; không có lưới dọc; vàng chỉ nhấn tối đa một giá trị; biểu đồ cột bắt đầu từ 0; sáu chuỗi đúng thứ tự màu.
   - Tài liệu thử `charts-tools` chèn các biểu đồ này vào báo cáo, `charts-py` chạy khối mã Python bằng Jupyter, mẫu `templates/charts.qmd` chạy khối mã R; cả ba qua lớp 2–5.
   - Mỗi ví dụ mã trong `charts/README.md` được chạy thật.
   - Phần R hoặc Stata tự bỏ qua khi máy chưa cài; tắt Stata bằng `--no-stata`. Đặt `VCCI_STATA` nếu Stata cài ở chỗ khác.

Kết quả nằm ở `tests/out/summary.md` (kèm PDF, DOCX, PDF do Word xuất và ảnh từng trang).

Cần: Quarto ≥ 1.6 (có sẵn Typst), Python 3 với PyYAML, PyMuPDF và matplotlib (Jupyter cho `charts-py`), Poppler (`pdffonts`, `pdfinfo`, `pdftotext`, `pdftoppm`); Microsoft Word cho lớp 4; R (ggplot2, svglite, ragg, systemfonts, knitr) và Stata 18+ cho lớp 8.
