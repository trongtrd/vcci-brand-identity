# Bộ nhận diện thương hiệu VCCI

Bộ nhận diện thương hiệu cho **Liên đoàn Thương mại và Công nghiệp Việt Nam** (VCCI · Vietnam Chamber of Commerce and Industry). Bộ này gồm:
- logo, màu sắc, kiểu chữ, họa tiết trống đồng và bộ icon;
- template Word và PowerPoint; theme biểu đồ cho Python, R và Stata; mẫu Quarto cho báo cáo, working paper và tờ trình;
- tài liệu hướng dẫn dài 37 trang.

Repo có cả sản phẩm dùng ngay lẫn công cụ để tạo lại toàn bộ từ file logo gốc.

> **Lưu ý:** đây không phải bộ nhận diện chính thức của VCCI. Bộ này được làm phi thương mại, để phục vụ công việc. Xem mục [Lưu ý](#lưu-ý).

![Bảng nhận diện thương hiệu VCCI](board/export/VCCI-Brand-Identity-Board_preview.jpg)

## Dùng ngay

Mọi thứ cần để làm một ấn phẩm đều nằm trong [`brand-assets/`](brand-assets/README.md):

| Thư mục | Nội dung |
|---|---|
| [`01_Logo`](brand-assets/01_Logo) | Logo chính; logo kèm tên song ngữ, xếp ngang và xếp dọc; logo đặt trên ô nền sáng. Định dạng SVG, PNG, PDF và file gốc CorelDRAW |
| [`02_Colour`](brand-assets/02_Colour) | Bảng màu, thang sắc độ, màu trạng thái và màu biểu đồ, cho Office, Adobe (ASE), CSS và JSON |
| [`03_Fonts`](brand-assets/03_Fonts) | Lora, Be Vietnam Pro và JetBrains Mono (cho mã nguồn), giấy phép SIL OFL 1.1 |
| [`04_Graphics`](brand-assets/04_Graphics) | Họa tiết vòng trống đồng, mặt trời 14 cánh, cung chữ C, trường chấm |
| [`05_Icons`](brand-assets/05_Icons) | 48 icon giao diện và 24 hero icon (hình minh họa lớn) theo lĩnh vực hoạt động của VCCI |
| [`06_Templates`](brand-assets/06_Templates/README.md) | Template Word (thư, báo cáo, thư mời) và PowerPoint 16:9 (18 layout) |
| [`07_Guidelines`](brand-assets/07_Guidelines) | **Hướng dẫn Nhận diện Thương hiệu VCCI** (PDF, tiếng Việt) |
| [`brand-tokens.json`](brand-assets/brand-tokens.json) | Mọi thông số (màu, tỉ lệ logo, cỡ chữ, khoảng cách) ở dạng phần mềm đọc trực tiếp được |

**Viết bằng Markdown hoặc Quarto?** Mẫu báo cáo, working paper và tờ trình (xuất PDF và Word) được phát hành ở một repo riêng, [trongtrd/vcci-quarto](https://github.com/trongtrd/vcci-quarto) (tên cũ: quarto-vcci). Cài bằng lệnh `quarto use template trongtrd/vcci-quarto`. Mã nguồn của mẫu nằm trong thư mục [`quarto-vcci/`](quarto-vcci/README.md) của repo này.

### Năm quy tắc cần nhớ

1. Logo chỉ có **một phiên bản màu**: chữ màu VCCI Blue (CMYK 100/80/0/0), trống đồng giữ màu gốc, đặt trên nền sáng.
2. Trên nền xanh, nền tối hay trên ảnh, đặt logo vào **ô nền sáng**. **Không** dùng logo chữ trắng (kiêng kị về văn hóa), không dùng logo chữ vàng, không tách trống đồng ra dùng riêng.
3. Khoảng trống bảo vệ quanh logo **bằng bán kính trống đồng** (khoảng 0,26 chiều cao chữ).
4. Chỉ dùng hai họ chữ: **Lora** cho tiêu đề, **Be Vietnam Pro** cho nội dung.
5. Mỗi bố cục chỉ có **một điểm nhấn màu vàng**.

Chi tiết xem trong [tài liệu hướng dẫn](brand-assets/07_Guidelines/VCCI_Huong-dan-Nhan-dien-Thuong-hieu_v1.1.pdf).

## Dùng với AI agent (Claude Code, Codex, Antigravity)

Repo có sẵn skill [`vcci-brand`](skills/vcci-brand/SKILL.md). Với skill này, agent trình bày lại tài liệu thô theo bộ nhận diện VCCI:

- **Từ file Word thô ra báo cáo VCCI:** bìa trước, mục lục, chương có nhãn và gạch vàng, bảng theo kiểu VCCI, chú thích hình và bảng, chú thích cuối trang, bìa sau.
- **Từ file PowerPoint thô (hoặc dàn ý) ra bài trình bày VCCI:** dùng 18 layout của template, thêm thẻ số liệu, biểu đồ PowerPoint sửa được số liệu, thẻ nội dung, chuỗi bước, bảng, và slide chuyển chương có hero icon.

Quy trình có bốn bước:

1. Script lấy nội dung từ file thô ra dạng Markdown.
2. Agent đánh dấu cấu trúc: đâu là chương, mục, bảng, hình. Agent không sửa câu chữ hay số liệu.
3. Script tạo file mới theo template.
4. `finalize.py` mở Word hoặc PowerPoint trên Windows, xuất PDF và ảnh từng trang để agent tự soát lại.

Ví dụ (số liệu giả lập): [báo cáo](skills/vcci-brand/examples/sample-report_VCCI.pdf), [bài trình bày](skills/vcci-brand/examples/sample-deck_VCCI.pdf).

### Cài đặt cho từng công cụ

| Công cụ | Cách cài |
|---|---|
| **Claude Code** | Cài plugin bằng hai lệnh trong Claude Code (xem bên dưới) |
| **Codex** (của OpenAI; bản ứng dụng, dòng lệnh hoặc extension trong IDE) | `python tools/install_skill.py codex` |
| **Antigravity** (của Google) | `python tools/install_skill.py antigravity`; bản dòng lệnh dùng `antigravity-cli` |
| Agent khác đọc được skill dạng `SKILL.md` | `python tools/install_skill.py --dest <thư-mục-skill-của-agent>/vcci-brand` |
| ChatGPT trên web, điện thoại | Không dùng được, vì ChatGPT chạy mã trên máy chủ: ở đó không có template của repo, cũng không có Word hay PowerPoint. Người có gói ChatGPT hãy dùng **Codex**, vì Codex chạy trên máy của mình |

**Claude Code:** gõ hai lệnh sau trong Claude Code:

```
/plugin marketplace add trongtrd/vcci-brand-identity
/plugin install vcci-brand@vcci-brand-identity
```

**Codex, Antigravity và các agent khác:**

1. Cài Python 3.9 trở lên từ [python.org](https://www.python.org/downloads/). Trên Windows, nhớ đánh dấu ô "Add python.exe to PATH" khi cài. Sau đó cài ba thư viện:
   ```bash
   python -m pip install lxml pillow python-pptx
   ```
   Trên macOS, gõ `python3` thay cho `python` trong mọi lệnh.
2. Tải repo về một chỗ cố định, chẳng hạn thư mục Documents. Nếu máy có Git:
   ```bash
   git clone https://github.com/trongtrd/vcci-brand-identity.git
   cd vcci-brand-identity
   ```
   Nếu không có Git: trên trang repo, bấm **Code → Download ZIP**, giải nén, rồi mở cửa sổ dòng lệnh trong thư mục vừa giải nén.
3. Cài skill cho công cụ bạn dùng (chạy lệnh trong thư mục repo):
   ```bash
   python tools/install_skill.py codex
   ```
   Dùng công cụ khác thì thay `codex` bằng `antigravity`, `antigravity-cli` hoặc `claude` (Claude Code mà không cài plugin). Chỉ muốn dùng skill trong một dự án thì chạy `python tools/install_skill.py --project <thư-mục-dự-án>`. Lệnh này chép skill vào `<thư-mục-dự-án>/.agents/skills/`, là nơi cả Codex lẫn Antigravity đều tìm skill.
4. Khởi động lại agent.

Lệnh cài chép skill sang thư mục của agent, kèm đường dẫn về thư mục repo, nơi chứa template, logo và icon. Vì thế **đừng xóa hay chuyển thư mục repo đi chỗ khác**. Nếu đã chuyển, hãy chạy lại lệnh cài ở chỗ mới. Muốn cập nhật: chạy `git pull` (hoặc tải lại file ZIP), rồi chạy lại lệnh cài. Muốn gỡ: thêm `--uninstall` vào cuối lệnh cài.

Với Codex còn một cách không cần cài: mở Codex ngay trong thư mục repo. Codex sẽ đọc [`AGENTS.md`](AGENTS.md) và dùng skill trong `skills/vcci-brand`.

### Sử dụng

Chỉ cần nói yêu cầu, chẳng hạn *"Định dạng bao_cao_tho.docx thành báo cáo VCCI"* hoặc *"Chuyển slide_tho.pptx sang mẫu trình bày VCCI"*. Agent tự nhận ra yêu cầu nào cần dùng skill. Trong Codex, có thể gọi thẳng skill bằng `$vcci-brand`.

Bước 4 của quy trình (xuất PDF và ảnh từng trang để agent tự soát) cần Microsoft Word hoặc PowerPoint trên Windows. Trên macOS hay Linux, agent vẫn tạo được file `.docx` và `.pptx` nhưng bỏ qua bước tự soát này, nên bạn hãy mở file ra xem lại. Thư, công văn và thư mời vẫn làm tay bằng template. Báo cáo, working paper và tờ trình viết bằng Markdown thì dùng [vcci-quarto](https://github.com/trongtrd/vcci-quarto), không cần agent.

## Cấu trúc repo

```
brand-assets/    Sản phẩm để dùng: logo, màu, font, họa tiết, icon, template, hướng dẫn
board/           Bảng nhận diện một trang (HTML) và bản xuất PNG, PDF
quarto-vcci/     Mã nguồn mẫu Quarto (bản phát hành: trongtrd/vcci-quarto)
skills/          Skill cho AI agent (vcci-brand); .claude-plugin/ khai báo plugin cho Claude Code
docs/            Nhật ký các quyết định thiết kế, kế hoạch, hồ sơ bàn giao bộ icon
source/          File gốc: logo CorelDRAW và các bản logo cũ
tools/           Công cụ tạo lại toàn bộ sản phẩm (Python, Node.js)
build/           File trung gian trong lúc tạo (không đưa lên git)
```

## Tạo lại từ file gốc

Cần có: Windows; Python 3.12 trở lên; Node.js 18 trở lên; Microsoft Edge; Poppler (`pdftoppm`); Microsoft Word và PowerPoint cho bước tạo template.

Trên Windows, nên clone với tùy chọn cho phép đường dẫn dài. Một số file icon có tên dài, nên nếu clone vào thư mục nằm sâu, đường dẫn có thể vượt giới hạn 260 ký tự và git báo lỗi "Filename too long":

```bash
git -c core.longpaths=true clone https://github.com/trongtrd/vcci-brand-identity.git
```

```bash
pip install -r requirements.txt
npm install
python tools/build.py all
```

Có thể chạy riêng từng bước: `logo`, `assets`, `board`, `word`, `ppt`, `guide`. Xem [`tools/README.md`](tools/README.md).

## Người thực hiện

- Phát triển và thiết kế: **Trương Đức Trọng**.
- Icon giao diện dựa trên bộ [Lucide](https://lucide.dev) (giấy phép ISC).
- Font: [Lora](https://github.com/cyrealtype/Lora-Cyrillic), [Be Vietnam Pro](https://github.com/bettergui/BeVietnamPro) và [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono), giấy phép SIL Open Font License 1.1.

## Lưu ý

Bộ nhận diện này do Trương Đức Trọng phát triển, phi thương mại, để phục vụ công việc. Đây **không phải** bộ nhận diện thương hiệu chính thức của VCCI và không thay cho các quy định hay ấn phẩm chính thức của VCCI.

*English: an unofficial, non-commercial brand identity kit developed by Truong Duc Trong for work use. It is not an official VCCI product.*

## Giấy phép

Logo và tên VCCI là tài sản của Liên đoàn Thương mại và Công nghiệp Việt Nam. Mã nguồn trong `tools/`, `quarto-vcci/` và các script trong `skills/` dùng giấy phép MIT. Chi tiết từng phần xem trong [LICENSE.md](LICENSE.md).
