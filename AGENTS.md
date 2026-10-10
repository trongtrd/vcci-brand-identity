# Hướng dẫn cho agent (Codex, Claude Code và các agent khác)

Repo này là Bộ nhận diện thương hiệu VCCI. Để tạo tài liệu theo thương hiệu VCCI, đọc và làm theo skill [`skills/vcci-brand/SKILL.md`](skills/vcci-brand/SKILL.md).

- Báo cáo từ file Word thô: quy trình 4 bước trong skill (`extract_docx.py` → biên tập Markdown → `render_report.py` → `finalize.py`).
- Bài trình bày từ file PowerPoint thô hoặc dàn ý: phần B của skill (`extract_pptx.py` → biên tập Markdown → `render_deck.py` → `finalize.py`).
- Báo cáo, working paper, tờ trình bằng Quarto và biểu đồ bằng Python, R, Stata: phần C của skill và `quarto-vcci/README.md`.
- Quy tắc thương hiệu bắt buộc: phần "Quy tắc thương hiệu bắt buộc" trong skill và [`docs/DECISIONS.md`](docs/DECISIONS.md). Không thay đổi các quyết định đã chốt.
- Không điều khiển Word hay PowerPoint khi người dùng đang mở tài liệu; không tắt tiến trình Office của người dùng.
- Sửa chính bộ nhận diện (logo, template, tài liệu hướng dẫn): xem [`tools/README.md`](tools/README.md).
- Cài skill cho agent ở thư mục khác (Codex, Antigravity, Claude Code): `python tools/install_skill.py <codex|antigravity|antigravity-cli|claude>`; hướng dẫn ở README, mục "Dùng với AI agent". Sửa `tools/install_skill.py` hay `find_brand_root` thì chạy `python tools/test_install_skill.py`.
