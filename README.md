# Bộ nhận diện thương hiệu VCCI

Hệ thống nhận diện thương hiệu cho **Liên đoàn Thương mại và Công nghiệp Việt Nam** (VCCI · Vietnam Chamber of Commerce and Industry): logo, màu sắc, kiểu chữ, họa tiết trống đồng, bộ icon, template Word và PowerPoint, theme biểu đồ cho Python, R và Stata, extension Quarto cho báo cáo, working paper và tờ trình, và tài liệu hướng dẫn 37 trang. Repo chứa cả sản phẩm hoàn chỉnh lẫn công cụ để dựng lại toàn bộ từ file logo gốc.

![Bảng nhận diện thương hiệu VCCI](board/export/VCCI-Brand-Identity-Board_preview.jpg)

## Dùng ngay

Mọi thứ cần để làm ấn phẩm nằm trong [`brand-assets/`](brand-assets/README.md):

| Thư mục | Nội dung |
|---|---|
| [`01_Logo`](brand-assets/01_Logo) | Logo chính, lockup song ngữ ngang và đứng, bản trên ô nền sáng: SVG, PNG, PDF; file gốc CorelDRAW |
| [`02_Colour`](brand-assets/02_Colour) | Bảng màu, thang sắc độ, màu trạng thái và màu biểu đồ cho Office, Adobe (ASE), CSS, JSON |
| [`03_Fonts`](brand-assets/03_Fonts) | Lora và Be Vietnam Pro (SIL OFL 1.1) |
| [`04_Graphics`](brand-assets/04_Graphics) | Họa tiết vòng trống đồng, mặt trời 14 cánh, cung chữ C, trường chấm |
| [`05_Icons`](brand-assets/05_Icons) | 48 icon giao diện, 24 hero icon theo lĩnh vực của VCCI |
| [`06_Templates`](brand-assets/06_Templates/README.md) | Template Word (thư, báo cáo, thư mời) và PowerPoint 16:9 (18 layout) |
| [`07_Guidelines`](brand-assets/07_Guidelines) | **Hướng dẫn Nhận diện Thương hiệu VCCI** (PDF, tiếng Việt) |
| [`brand-tokens.json`](brand-assets/brand-tokens.json) | Toàn bộ thông số (màu, tỉ lệ logo, thang chữ, khoảng cách) dạng máy đọc được |

**Viết bằng Markdown hoặc Quarto?** Mẫu báo cáo, working paper và tờ trình (PDF và Word) được phát hành riêng: [trongtrd/quarto-vcci](https://github.com/trongtrd/quarto-vcci). Cài bằng `quarto use template trongtrd/quarto-vcci`. Mã nguồn của mẫu nằm trong [`quarto-vcci/`](quarto-vcci/README.md).

### Năm quy tắc cốt lõi

1. Logo chỉ có **một phiên bản màu**: chữ VCCI Blue (CMYK 100/80/0/0), trống đồng giữ màu gốc, đặt trên nền sáng.
2. Trên nền xanh, nền tối hoặc ảnh: đặt logo trên **ô nền sáng**. **Không** dùng logo chữ trắng (kiêng kị văn hóa), không dùng chữ vàng, không tách trống đồng ra dùng riêng.
3. Khoảng trống bảo vệ **x = bán kính trống đồng** (≈ 0,26 chiều cao chữ).
4. Hai họ chữ: **Lora** cho tiêu đề, **Be Vietnam Pro** cho nội dung.
5. **Một điểm nhấn vàng** trên mỗi bố cục.

Chi tiết trong [tài liệu hướng dẫn](brand-assets/07_Guidelines/VCCI_Huong-dan-Nhan-dien-Thuong-hieu_v1.1.pdf).

## Dùng với AI agent (Claude Code, Codex, Antigravity)

Repo có sẵn skill [`vcci-brand`](skills/vcci-brand/SKILL.md) để agent chuyển tài liệu thô sang bộ nhận diện VCCI:

- **File Word thô thành báo cáo VCCI:** bìa trước, mục lục, chương có nhãn và gạch vàng, kiểu bảng VCCI, chú thích hình và bảng, chú thích cuối trang, bìa sau.
- **File PowerPoint thô (hoặc dàn ý) thành bài trình bày VCCI:** dựng trên 18 layout của template, có thêm thẻ số liệu, biểu đồ thật (sửa được số liệu), thẻ nội dung, chuỗi bước, bảng, slide chuyển chương có hero icon.

Quy trình gồm bốn bước:

1. Script trích nội dung thô ra Markdown.
2. Agent đánh dấu cấu trúc. Agent không sửa câu chữ hay số liệu.
3. Script dựng file theo template.
4. `finalize.py` dùng Word hoặc PowerPoint trên Windows để xuất PDF và ảnh từng trang cho agent tự kiểm tra.

Ví dụ (số liệu giả lập): [báo cáo](skills/vcci-brand/examples/sample-report_VCCI.pdf), [bài trình bày](skills/vcci-brand/examples/sample-deck_VCCI.pdf).

### Cài đặt theo công cụ

| Công cụ | Cách cài |
|---|---|
| **Claude Code** | Plugin, hai lệnh trong Claude Code (bên dưới) |
| **Codex** (OpenAI: ứng dụng, CLI, extension IDE) | `python tools/install_skill.py codex` |
| **Antigravity** (Google) | `python tools/install_skill.py antigravity`; bản dòng lệnh: `antigravity-cli` |
| Agent khác đọc được skill dạng `SKILL.md` | `python tools/install_skill.py --dest <thư-mục-skill-của-agent>/vcci-brand` |
| ChatGPT trên web, điện thoại | Không dùng được: ChatGPT chạy mã trên máy chủ, không có template của repo và không có Word, PowerPoint. Người có gói ChatGPT dùng **Codex** (chạy trên máy của mình) |

**Claude Code:** gõ trong Claude Code:

```
/plugin marketplace add trongtrd/vcci-brand-identity
/plugin install vcci-brand@vcci-brand-identity
```

**Codex, Antigravity và agent khác:**

1. Cài Python 3.9 trở lên ([python.org](https://www.python.org/downloads/); trên Windows, đánh dấu "Add python.exe to PATH" khi cài), rồi cài ba thư viện:
   ```bash
   python -m pip install lxml pillow python-pptx
   ```
   Trên macOS, dùng `python3` thay cho `python` ở mọi lệnh.
2. Tải repo về một chỗ cố định, ví dụ thư mục Documents. Có Git thì:
   ```bash
   git clone https://github.com/trongtrd/vcci-brand-identity.git
   cd vcci-brand-identity
   ```
   Không có Git: trên trang repo, bấm **Code → Download ZIP**, giải nén, rồi mở cửa sổ dòng lệnh trong thư mục vừa giải nén.
3. Cài skill cho công cụ của bạn (chạy trong thư mục repo):
   ```bash
   python tools/install_skill.py codex
   ```
   Thay `codex` bằng `antigravity`, `antigravity-cli` hoặc `claude` (Claude Code không qua plugin). Muốn skill chỉ có trong một dự án: `python tools/install_skill.py --project <thư-mục-dự-án>`; lệnh này chép vào `<thư-mục-dự-án>/.agents/skills/`, nơi cả Codex và Antigravity đều tìm skill.
4. Khởi động lại agent.

Lệnh cài chép skill sang thư mục của agent và ghi kèm đường dẫn tới thư mục repo, nơi để template, logo và icon. Vì vậy **đừng xóa hay di chuyển thư mục repo**. Nếu đã di chuyển, chạy lại lệnh cài từ chỗ mới. Cập nhật: `git pull` (hoặc tải ZIP mới), rồi chạy lại lệnh cài. Gỡ: thêm `--uninstall` vào lệnh cài.

Codex còn có cách không cần cài: mở Codex ngay trong thư mục repo, Codex đọc [`AGENTS.md`](AGENTS.md) và dùng skill trong `skills/vcci-brand`.

### Sử dụng

Yêu cầu bằng lời, ví dụ: *"Định dạng bao_cao_tho.docx thành báo cáo VCCI"* hoặc *"Chuyển slide_tho.pptx sang mẫu trình bày VCCI"*. Agent tự chọn skill theo mô tả. Trong Codex có thể gọi thẳng bằng `$vcci-brand`.

Bước 4 của quy trình (xuất PDF và ảnh từng trang để agent tự kiểm tra) cần Microsoft Word hoặc PowerPoint trên Windows. Trên macOS, Linux, agent vẫn dựng được file `.docx`, `.pptx` nhưng bỏ qua bước tự kiểm này; hãy mở file để xem lại. Thư, công văn và thư mời vẫn dùng template thủ công. Báo cáo, working paper và tờ trình viết bằng Markdown thì dùng [quarto-vcci](https://github.com/trongtrd/quarto-vcci), không cần agent.

## Cấu trúc repo

```
brand-assets/    Sản phẩm bàn giao: logo, màu, font, họa tiết, icon, template, hướng dẫn
board/           Bảng nhận diện một trang (HTML) và bản xuất PNG/PDF
skills/          Skill cho AI agent (vcci-brand); .claude-plugin/ khai báo plugin cho Claude Code
docs/            Nhật ký quyết định thiết kế; hồ sơ bàn giao bộ icon
source/          Đầu vào gốc: logo CorelDRAW và các bản logo cũ
tools/           Công cụ dựng lại toàn bộ sản phẩm (Python, Node.js)
build/           File trung gian khi dựng (không đưa lên git)
```

## Dựng lại từ nguồn

Yêu cầu: Windows; Python 3.12 trở lên; Node.js 18 trở lên; Microsoft Edge; Poppler (`pdftoppm`); Microsoft Word và PowerPoint cho bước template.

Trên Windows, nên clone với tùy chọn đường dẫn dài. Một số tên file icon dài, nên clone vào thư mục sâu có thể vượt giới hạn 260 ký tự và báo lỗi "Filename too long":

```bash
git -c core.longpaths=true clone <địa-chỉ-repo>
```

```bash
pip install -r requirements.txt
npm install
python tools/build.py all
```

Có thể chạy từng bước: `logo`, `assets`, `board`, `word`, `ppt`, `guide`. Xem [`tools/README.md`](tools/README.md).

## Ghi công

- Phát triển và thiết kế: **Truong Duc Trong**.
- Thiết kế hệ thống, logo vector, template và tài liệu hướng dẫn: thực hiện cùng Claude (Anthropic).
- Bộ icon v1: thực hiện cùng một agent ChatGPT theo [hồ sơ bàn giao](docs/handoff-icons/); icon giao diện dựa trên [Lucide](https://lucide.dev) (ISC).
- Font: [Lora](https://github.com/cyrealtype/Lora-Cyrillic) và [Be Vietnam Pro](https://github.com/bettergui/BeVietnamPro), SIL Open Font License 1.1.

## Giấy phép

Logo và tên VCCI là tài sản của Liên đoàn Thương mại và Công nghiệp Việt Nam. Mã nguồn trong `tools/` và các script trong `skills/` dùng giấy phép MIT. Chi tiết từng phần trong [LICENSE.md](LICENSE.md).
