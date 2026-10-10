# quarto-vcci: mẫu tài liệu VCCI cho Quarto

<!-- dev-only -->
> Đây là thư mục nguồn trong repo bộ nhận diện. Người dùng cài bản phát hành từ [trongtrd/quarto-vcci](https://github.com/trongtrd/quarto-vcci) như hướng dẫn dưới đây. Ở đây, các tài liệu mẫu nằm trong `templates/` (`report.qmd` là mẫu báo cáo). Người sửa extension xem [DEVELOPMENT.md](DEVELOPMENT.md).
<!-- /dev-only -->

Bộ mẫu này giúp viết báo cáo, working paper và tờ trình theo bộ nhận diện thương hiệu của Liên đoàn Thương mại và Công nghiệp Việt Nam (VCCI). Bạn viết nội dung bằng văn bản thường (Markdown), chạy một lệnh, và nhận về:

- **PDF khổ A4** đúng bộ nhận diện (bìa, màu, font, logo): bản để gửi đi và in;
- **Word (.docx)** dùng style VCCI: bản để đồng nghiệp sửa.

*English: Quarto templates for VCCI (Vietnam Chamber of Commerce and Industry) reports, working papers and memos, rendered to an A4 PDF (Typst) and Word. Every format also supports English (`lang: en`). Install with `quarto use template trongtrd/quarto-vcci`.*

![Bìa báo cáo, một trang chương, trang đầu working paper và tờ trình](examples/preview.png)

| Loại tài liệu | Dùng khi | Bản mẫu |
|---|---|---|
| **Báo cáo** (`vcci-report`) | Báo cáo tư vấn, báo cáo nghiên cứu: có bìa, mục lục, chương, bìa sau | [PDF](examples/report.pdf) · [Word](https://github.com/trongtrd/quarto-vcci/releases/download/v1.0.0/report.docx) |
| **Working paper** (`vcci-wp`) | Bài nghiên cứu: số hiệu, tóm tắt song ngữ, mã JEL, trích dẫn APA | [PDF](examples/wp.pdf) · [tiếng Anh](examples/wp-en.pdf) · [Word](https://github.com/trongtrd/quarto-vcci/releases/download/v1.0.0/wp.docx) |
| **Tờ trình** (`vcci-memo`) | Văn bản đệ trình nội bộ 1–2 trang: Gửi, Từ, Về việc, chữ ký | [PDF](examples/memo.pdf) · [tiếng Anh](examples/memo-en.pdf) · [Word](https://github.com/trongtrd/quarto-vcci/releases/download/v1.0.0/memo.docx) |
| **Biểu đồ** | Theme cho matplotlib (Python), ggplot2 (R), Stata | [PDF](examples/charts.pdf) |

## Mục lục

1. [Cần chuẩn bị](#1-cần-chuẩn-bị)
2. [Bắt đầu trong 5 phút](#2-bắt-đầu-trong-5-phút)
3. [Viết nội dung](#3-viết-nội-dung)
4. [Báo cáo](#4-báo-cáo-vcci-report)
5. [Working paper](#5-working-paper-vcci-wp)
6. [Tờ trình](#6-tờ-trình-vcci-memo)
7. [Trích dẫn và tài liệu tham khảo](#7-trích-dẫn-và-tài-liệu-tham-khảo)
8. [Biểu đồ: Python, R, Stata](#8-biểu-đồ-python-r-stata)
9. [Bản Word](#9-bản-word)
10. [Cập nhật, dùng trong dự án có sẵn](#10-cập-nhật-dùng-trong-dự-án-có-sẵn)
11. [Gặp lỗi?](#11-gặp-lỗi)

## 1. Cần chuẩn bị

**Bắt buộc: Quarto** (miễn phí, có cho Windows, macOS, Linux).

1. Tải và cài từ [quarto.org/docs/get-started](https://quarto.org/docs/get-started/). Cần bản 1.6 trở lên; bộ mẫu được kiểm thử với Quarto 1.9.
2. Mở một cửa sổ dòng lệnh **mới** (xem cách mở ở bước 2) và gõ:
   ```bash
   quarto --version
   ```
   Thấy số phiên bản (ví dụ `1.9.38`) là được.

Không cần cài font, LaTeX hay Microsoft Word: font Lora, Be Vietnam Pro và JetBrains Mono đi kèm bộ mẫu, và Quarto có sẵn Typst để tạo PDF.

**Nên có: một trình soạn thảo** để sửa file `.qmd` và bấm nút dựng tài liệu: [Positron](https://positron.posit.co/), [RStudio](https://posit.co/download/rstudio-desktop/) hoặc [VS Code](https://code.visualstudio.com/) có extension Quarto. Notepad cũng dùng được, khi đó bạn dựng tài liệu bằng lệnh.

**Chỉ cần khi vẽ biểu đồ bằng mã** trong tài liệu: R hoặc Python (mục 8). Không vẽ biểu đồ thì bỏ qua.

## 2. Bắt đầu trong 5 phút

### Bước 1. Mở cửa sổ dòng lệnh ở thư mục bạn muốn

- **Windows 11:** mở thư mục (ví dụ `Documents`) trong File Explorer, nhấp chuột phải vào chỗ trống, chọn **Open in Terminal**.
- **macOS:** mở ứng dụng Terminal, gõ `cd ` (có dấu cách), kéo thư mục vào cửa sổ rồi nhấn Enter.
- **Trong Positron, RStudio, VS Code:** dùng thẻ Terminal của trình soạn thảo.

### Bước 2. Tạo dự án từ mẫu

```bash
quarto use template trongtrd/quarto-vcci
```

Quarto hỏi bốn câu:

| Câu hỏi | Trả lời |
|---|---|
| `Do you trust the authors of this template?` | Nhấn **Y** rồi Enter |
| `Create a subdirectory for template?` | Nhấn **Y** rồi Enter (tạo thư mục mới cho dự án) |
| `Directory name:` | Gõ tên thư mục, không dấu, không cách, ví dụ `bao-cao-pci`, rồi Enter |
| `Would you like to continue?` (sau danh sách VCCI Memo, VCCI Report, VCCI Working Paper) | Nhấn **Y** rồi Enter |

Quarto tải bộ mẫu từ GitHub và tạo thư mục `bao-cao-pci` gồm:

| File | Nội dung |
|---|---|
| `bao-cao-pci.qmd` | **Báo cáo mẫu.** File mẫu báo cáo mang tên thư mục |
| `wp.qmd`, `references.bib` | Working paper mẫu và danh mục tài liệu tham khảo của nó |
| `memo.qmd` | Tờ trình mẫu |
| `charts.qmd` | Báo cáo mẫu có biểu đồ vẽ bằng R |
| `charts/` | Theme biểu đồ cho Python, R, Stata |
| `_extensions/` | Bộ mẫu (định dạng, font, logo). **Không sửa, không xóa.** |

Không dùng mẫu nào thì xóa file `.qmd` của mẫu đó; giữ nguyên `_extensions/`.

### Bước 3. Dựng thử

```bash
cd bao-cao-pci
quarto render bao-cao-pci.qmd
```

Sau khoảng 10 giây, cạnh file `.qmd` có **`bao-cao-pci.pdf`** và **`bao-cao-pci.docx`**. Mở PDF để xem. Nó giống [bản mẫu](examples/report.pdf).

Trong Positron, RStudio, VS Code: mở file `.qmd` rồi bấm **Render** (hoặc Ctrl+Shift+K; trên macOS ⌘+Shift+K).

### Bước 4. Viết báo cáo của bạn

Mở `bao-cao-pci.qmd` bằng trình soạn thảo. File có hai phần:

1. **Phần thông tin** nằm giữa hai dòng `---` ở đầu file: tiêu đề, tác giả, ngày, bên đặt hàng… Sửa giá trị sau dấu hai chấm, giữ nguyên tên khóa và thụt lề. Ý nghĩa từng khóa ở mục 4.
2. **Phần nội dung** bên dưới: thay chữ mẫu bằng nội dung của bạn (cách viết ở mục 3).

Lưu file, dựng lại (bước 3), xem PDF. Lặp lại đến khi xong.

### Bước 5. Chỉ dựng PDF hoặc chỉ dựng Word

Mặc định một lần dựng ra cả hai. Muốn nhanh hơn:

```bash
quarto render bao-cao-pci.qmd --to vcci-report-typst
quarto render bao-cao-pci.qmd --to vcci-report-docx
```

Lệnh thứ nhất chỉ ra PDF, lệnh thứ hai chỉ ra Word. Với working paper và tờ trình, thay `vcci-report` bằng `vcci-wp` hoặc `vcci-memo`.

## 3. Viết nội dung

Nội dung viết bằng Markdown: văn bản thường, thêm vài ký hiệu để đánh dấu.

| Muốn có | Viết |
|---|---|
| Chương (mỗi chương sang trang mới, nhãn "CHƯƠNG 01") | `# Kết quả` |
| Mục, mục con | `## Chi phí thời gian`, `### Theo ngành` |
| Chương không đánh số (Tóm tắt, Phụ lục) | `# Tóm tắt {.unnumbered}` |
| Chữ đậm, chữ nghiêng | `**đậm**`, `*nghiêng*` |
| Danh sách | Mỗi dòng bắt đầu bằng `- ` (hoặc `1. ` cho danh sách đánh số) |
| Chú thích cuối trang | `Câu văn.^[Nội dung chú thích.]` |
| Liên kết | `[VCCI](https://vcci.com.vn)` |
| Hình, có chú thích | `![Chú thích hình](hinh/ten-anh.png)` |
| Trích dẫn tài liệu | `[@vcci2025]` (mục 7) |

**Bảng:**

```markdown
| Thủ tục          | 2024 | 2025 |
|------------------|-----:|-----:|
| Chấp thuận đầu tư |   21 |   18 |
| Giao đất         |   32 |   30 |

: Số ngày trung bình theo thủ tục {#tbl-thutuc}
```

Dòng bắt đầu bằng `:` là tiêu đề bảng; `{#tbl-thutuc}` cho phép nhắc lại "xem @tbl-thutuc" (ra "Bảng 1"). `--:` căn phải cột số. Cột có chữ dài thì cho nhiều dấu `-` hơn ở dòng thứ hai, vì độ rộng cột chia theo số dấu `-`.

**Khối riêng của VCCI:**

```markdown
::: lead
Hai, ba câu nêu thông điệp chính, in to màu xanh ở đầu chương.
:::

::: figures
64 ngày | Thời gian hoàn tất thủ tục
38% | Doanh nghiệp đi lại từ ba lần trở lên
:::

::: {.highlight title="Ba khuyến nghị ưu tiên"}
Hộp nhấn mạnh nền xanh nhạt, gạch xanh bên trái.
:::

::: label
Nhãn chữ in hoa nhỏ
:::
```

`figures` tạo các thẻ số liệu: mỗi dòng là `số | mô tả`. Hộp ghi chú của Quarto (`::: callout-note`, `-tip`, `-warning`, `-important`, `-caution`) tự theo màu trạng thái của VCCI.

Phương trình viết kiểu LaTeX: `$y = a + bx$` trong câu, `$$ ... $$ {#eq-ten}` cho phương trình riêng dòng có đánh số. Mã nguồn đặt giữa hai dòng ```` ``` ````.

Hướng dẫn Markdown đầy đủ của Quarto: [quarto.org/docs/authoring/markdown-basics](https://quarto.org/docs/authoring/markdown-basics.html).

## 4. Báo cáo (`vcci-report`)

Bắt đầu từ file báo cáo mẫu (`<tên-thư-mục>.qmd`). Phần đầu file:

```yaml
---
title: "Đánh giá chi phí tuân thủ thủ tục đầu tư"
subtitle: "Báo cáo tư vấn cho Ủy ban nhân dân tỉnh"
report-label: "Báo cáo tư vấn"
client: "Ủy ban nhân dân tỉnh Hòa Bình Xanh"
author:
  - name: Nguyễn Văn An
    affiliations:
      - name: Ban Pháp chế, VCCI
date: 2026-10-10
status: "Bản thảo"       # xóa dòng này khi phát hành
hero: 4                  # hình minh họa trên bìa, số 1–24
toc: true                # có mục lục
format:
  vcci-report-typst: default
  vcci-report-docx: default
---
```

| Khóa | Ý nghĩa | Hiện ở |
|---|---|---|
| `title`, `subtitle` | Tiêu đề, phụ đề | Bìa, trang thông tin |
| `report-label` | Nhãn trên tiêu đề, mặc định "Báo cáo" (ví dụ "Báo cáo tư vấn") | Bìa |
| `short-title` | Tên rút gọn | Đầu trang |
| `client` | Bên đặt hàng | Bìa, trang thông tin |
| `author` (kèm `affiliations`), `team` | Tác giả; `team` thay danh sách nhóm thực hiện nếu cần | Bìa, trang thông tin |
| `date`, `version` | Ngày (viết `2026-10-10`, in ra "10 tháng 10 năm 2026"), phiên bản | Bìa, trang thông tin |
| `status` | Ví dụ "Bản thảo", "Mật": nhãn trên bìa và dấu chìm mọi trang. Xóa khi phát hành | Bìa, mọi trang |
| `hero` | Hình minh họa trên bìa, số 1–24 | Bìa |
| `citation-text` | Gợi ý trích dẫn báo cáo này | Trang thông tin |
| `disclaimer` | Lưu ý, miễn trừ | Trang thông tin |
| `contact` | Thay địa chỉ liên hệ mặc định của VCCI | Bìa sau |
| `cover: false`, `back-cover: false` | Bỏ bìa trước (cùng trang thông tin) hoặc bìa sau | |
| `toc: true` | Mục lục | Sau trang thông tin |
| `bibliography` | File tài liệu tham khảo (mục 7) | Chú thích, cuối tài liệu |
| `lang: en` | Báo cáo tiếng Anh; thêm `date-format: "D MMMM YYYY"` | |

## 5. Working paper (`vcci-wp`)

Bắt đầu từ `wp.qmd` (kèm `references.bib`). Trang đầu gồm: tên bộ và số hiệu, tiêu đề, tác giả (đơn vị, email), ngày, tóm tắt kèm từ khóa (một hoặc hai ngôn ngữ), mã JEL. Chân trang đầu có trích dẫn đề nghị, tác giả liên hệ, lời miễn trừ. Thân bài đánh số mục 1, 1.1; phương trình đánh số; tài liệu tham khảo kiểu APA ở cuối.

| Khóa | Ý nghĩa |
|---|---|
| `wp-number` | Số hiệu, ví dụ `"2026/01"`: hiện "VCCI Working Paper số 2026/01" (tiếng Anh: "No. 2026/01") |
| `wp-series` | Tên bộ, mặc định "VCCI Working Paper" |
| `lang` | `vi` (mặc định) hoặc `en`. Bài tiếng Anh nên thêm `date-format: "D MMMM YYYY"` |
| `author` | `name`, `email`, `affiliations`; `attributes: {corresponding: true}` đánh dấu \* tác giả liên hệ |
| `abstract`, `keywords` | Tóm tắt và từ khóa theo ngôn ngữ của bài |
| `abstract-en`, `keywords-en` | Tóm tắt tiếng Anh cho bài tiếng Việt (bài tiếng Anh dùng `abstract-vi`, `keywords-vi`) |
| `jel` | Mã JEL, ví dụ `[D22, K23]` |
| `thanks` | Lời cảm ơn: chú thích † ở tiêu đề |
| `citation-text` | Thay gợi ý trích dẫn tự sinh ("Tác giả (năm). Tiêu đề. VCCI Working Paper số …. Hà Nội: VCCI.") |
| `disclaimer` | Thay lời miễn trừ mặc định |
| `status`, `short-title`, `version`, `toc` | Như báo cáo |

## 6. Tờ trình (`vcci-memo`)

Bắt đầu từ `memo.qmd`. Tờ trình dài 1–2 trang; từ trang 2, đầu trang nhắc lại "Về việc".

| Khóa | Ý nghĩa |
|---|---|
| `title` | Nội dung "Về việc" |
| `recipient`, `sender`, `copy-to` | Gửi, Từ, Đồng gửi. **Không dùng `to` và `from`** (Quarto dành riêng hai khóa này). Không có `sender` thì lấy `author` |
| `date` | Ngày |
| `priority` | Ví dụ "Khẩn": nhãn cạnh chữ "TỜ TRÌNH" |
| `status` | Ví dụ "Nội bộ", "Mật": dấu chìm mọi trang |
| `signature` | `name` và `title` (chức vụ), đặt bên phải cuối tờ trình |
| `attachments` | Danh sách tài liệu kèm theo |
| `memo-label` | Thay chữ "Tờ trình" (tiếng Anh: "Memo") |
| `lang: en` | Tờ trình tiếng Anh ("MEMO", To, From, Subject…); thêm `date-format: "D MMMM YYYY"` |

## 7. Trích dẫn và tài liệu tham khảo

1. Ghi tài liệu vào một file `.bib` (xem `references.bib` mẫu). Phần mềm Zotero, Mendeley, EndNote đều xuất được file này.
2. Khai báo trong phần đầu tài liệu: `bibliography: references.bib`.
3. Trích dẫn trong bài bằng khóa của tài liệu.

| Loại tài liệu | Kiểu trích dẫn | Viết |
|---|---|---|
| Báo cáo, tờ trình | Chicago, chú thích cuối trang (lần đầu đầy đủ, các lần sau rút gọn) | Luôn trong ngoặc vuông: `[@vcci2025]`, `[@vcci2025, tr. 12]`. Viết `@vcci2025` không có ngoặc sẽ in cả nguồn vào giữa câu |
| Working paper | APA, tác giả–năm | `[@vcci2025]` cho "(VCCI, 2025)"; `@vcci2025` cho "VCCI (2025)" trong câu |

Lưu ý khi viết file `.bib`:
- **Tên người Việt** đặt trong ngoặc nhọn kép: `author = {{Nguyễn Thị Hạnh} and {Trần Đức Long}}`. Không có ngoặc, tên bị đảo thành "Thị Hạnh Nguyễn" hay viết tắt thành "Nguyễn, T. H.".
- **Báo cáo kỹ thuật** (`@techreport`): thêm `type = {Báo cáo kỹ thuật}` để không hiện chữ "technical report".
- Danh mục "Tài liệu tham khảo" tự xuất hiện ở cuối tài liệu (sau phụ lục). Không tự thêm mục này.

## 8. Biểu đồ: Python, R, Stata

Thư mục `charts/` có theme biểu đồ theo phần "Dữ liệu và biểu đồ" của hướng dẫn thương hiệu: màu chuỗi theo thứ tự VCCI, font, lưới, dấu phẩy thập phân. Cách dùng và ví dụ cho từng công cụ: [charts/README.md](charts/README.md).

| Công cụ | Trong tài liệu Quarto | Cần cài |
|---|---|---|
| **R** (ggplot2) | Khối mã đầu tiên: `source("charts/theme_vcci.R", encoding = "UTF-8")` rồi `vcci_setup()`. Mẫu: `charts.qmd` ([kết quả](examples/charts.pdf)) | R, và trong R: `install.packages(c("rmarkdown", "knitr", "ggplot2", "scales", "systemfonts", "svglite", "ragg"))` |
| **Python** (matplotlib) | `import sys; sys.path.insert(0, "charts")`, `import vcci_charts as vcci`, rồi `vcci.use()`. Thêm `fig-format: svg` cho PDF, `fig-format: png` cho Word | Python, và `python -m pip install jupyter matplotlib` |
| **Stata** | Vẽ trong Stata: `adopath + "charts"`, `do charts/vcci_graph.do`, vẽ, `graph export ten.svg`; rồi chèn vào tài liệu `![Chú thích](ten.svg)` | Stata 18 trở lên; cài font Lora và Be Vietnam Pro vào máy (file `.ttf` trong `_extensions/…/fonts`) |

Chú thích hình (`fig-cap`) nêu thông điệp của biểu đồ. Nguồn số liệu ghi dưới biểu đồ (`caption` trong ggplot, `vcci.source()`, `note()` trong Stata). Không dùng R thì xóa `charts.qmd`, vì file này chỉ dựng được khi có R.

<!-- dev-only -->
Trong repo bộ nhận diện, theme biểu đồ có thêm một bản ở `brand-assets/06_Templates/Charts/` cho người không dùng Quarto.
<!-- /dev-only -->

## 9. Bản Word

Bản Word dùng style VCCI (tiêu đề, bảng VCCI Table, hộp nhấn mạnh) và có nhúng font, để đồng nghiệp sửa nội dung. Bản PDF là bản để phát hành. Khác biệt:

- Không có bìa màu; trang đầu là tiêu đề, tác giả, ngày.
- **Mục lục trống khi mở lần đầu:** nhấp vào mục lục rồi nhấn F9 (hoặc nhấp chuột phải, chọn Update Field).
- Danh sách đặt trong hộp `::: highlight` nằm ngoài hộp.
- Phương trình dùng font Cambria Math.

## 10. Cập nhật, dùng trong dự án có sẵn

**Cập nhật bộ mẫu lên bản mới** (chạy trong thư mục dự án, trả lời Y khi được hỏi):

```bash
quarto add trongtrd/quarto-vcci
```

Lệnh chỉ thay `_extensions/`, không đụng tới file `.qmd` của bạn. Các thay đổi giữa các bản ghi trong [CHANGELOG](https://github.com/trongtrd/quarto-vcci/blob/main/CHANGELOG.md).

**Giữ đúng một phiên bản** (ví dụ cho dự án cần dựng lại y hệt sau này):

```bash
quarto use template trongtrd/quarto-vcci@v1.0.0
```

**Dùng cho một dự án đã có**, không cần các file mẫu: chạy `quarto add trongtrd/quarto-vcci` trong thư mục đó, rồi khai báo định dạng ở đầu file `.qmd`:

```yaml
format:
  vcci-report-typst: default     # PDF; working paper: vcci-wp-typst, tờ trình: vcci-memo-typst
  vcci-report-docx: default      # Word
```

## 11. Gặp lỗi?

| Hiện tượng | Cách xử lý |
|---|---|
| `quarto` không được nhận ra ("not recognized", "command not found") | Quarto chưa cài, hoặc cửa sổ dòng lệnh mở trước khi cài. Đóng và mở cửa sổ mới. |
| `Unable to read the extension 'vcci-report'` | File `.qmd` không nằm cùng thư mục với `_extensions/`. Chuyển file vào thư mục dự án, hoặc chạy `quarto add trongtrd/quarto-vcci` ở thư mục của file. |
| `quarto use template` báo thư mục không trống | Trả lời **Y** khi được hỏi tạo thư mục con, hoặc chạy lệnh trong một thư mục trống. |
| Báo lỗi khi ghi file PDF hay Word | File đang mở trong Acrobat hay Word. Đóng file rồi dựng lại. |
| `charts.qmd` báo lỗi về R hay thiếu gói (`there is no package called …`) | Cài R và các gói ở mục 8, hoặc xóa `charts.qmd` nếu không cần. |
| Tờ trình báo `cannot produce pdf output from …` | Đang dùng khóa `to` hay `from`; đổi thành `recipient`, `sender`. |
| Tên tác giả Việt bị đảo hay viết tắt trong tài liệu tham khảo | Đặt tên trong ngoặc nhọn kép trong file `.bib` (mục 7). |
| Nguồn tài liệu bị in vào giữa câu (báo cáo, tờ trình) | Viết trích dẫn trong ngoặc vuông: `[@khoa]`. |
| Mục lục bản Word trống | Nhấp vào mục lục, nhấn F9. |
| Bảng rộng bị chia cột không đều | Cho nhiều dấu `-` hơn ở cột có chữ dài (mục 3). |

Vẫn chưa được? Mở một [issue](https://github.com/trongtrd/quarto-vcci/issues), kèm lệnh đã chạy và thông báo lỗi.

## Giấy phép

Mã nguồn theo giấy phép MIT. Logo, tên và nhãn hiệu VCCI thuộc sở hữu của VCCI, chỉ dùng cho tài liệu của VCCI. Font theo SIL Open Font License. Chi tiết: [LICENSE.md](https://github.com/trongtrd/quarto-vcci/blob/main/LICENSE.md).
