// Generates the VCCI Word templates (as .docx; post-processed into .dotx with embedded fonts by finalize.py).
// Run from the repository root: node tools/word/make_templates.js
const fs = require('fs');
const path = require('path');
const D = require('docx');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer, Table, TableRow, TableCell, WidthType,
  AlignmentType, BorderStyle, ShadingType, PageNumber, TableOfContents, LevelFormat, PositionalTab,
  PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader, HorizontalPositionRelativeFrom,
  VerticalPositionRelativeFrom, TextWrappingType, FrameAnchorType, VerticalAlign, PageBreak, HeadingLevel,
  TableLayoutType, TableAnchorType, OverlapType,
} = D;

const ROOT = process.cwd();
const A = (...p) => fs.readFileSync(path.join(ROOT, ...p));
const OUT = path.join(ROOT, 'build', 'word', 'out');
fs.mkdirSync(OUT, { recursive: true });

// ---------------------------------------------------------------- brand tokens
const C = { blue: '264896', gold: 'FFCD00', bronzeInk: '9C570C', deep: '0B1A4F', tint: 'E7ECF6', ink: '161A26',
            slate: '5C6478', stone: 'E6E1D5', ivory: 'F4F0E6', paper: 'FBF9F4', white: 'FFFFFF' };
const F = { serif: 'Lora', serifMed: 'Lora Medium', serifSemi: 'Lora SemiBold',
            sans: 'Be Vietnam Pro', sansMed: 'Be Vietnam Pro Medium', sansSemi: 'Be Vietnam Pro SemiBold' };
const MM = 56.6929;                  // twips per mm
const mm = v => Math.round(v * MM);
const px = v => v * 96 / 25.4;       // mm -> docx-js image pixels
const emu = v => Math.round(v * 36000); // mm -> EMU
const PAGE = { width: 11906, height: 16838 };
const MARGIN = { top: mm(24), bottom: mm(22), left: mm(22), right: mm(22), header: mm(10), footer: mm(9) };
const CONTENT_W = PAGE.width - MARGIN.left - MARGIN.right;

const dims = JSON.parse(fs.readFileSync(path.join(ROOT, 'build', 'word', 'art', 'dims.json')));
const IMG = {
  lockup: A('brand-assets', '01_Logo', 'PNG', 'VCCI_Lockup_Horizontal_VI-EN_2400px.png'),
  logo: A('brand-assets', '01_Logo', 'PNG', 'VCCI_Logo_Primary_1200px.png'),
  cover: A('build', 'word', 'art', 'cover.png'), back: A('build', 'word', 'art', 'back.png'),
  watermark: A('build', 'word', 'art', 'watermark.png'), band: A('build', 'word', 'art', 'band.png'),
  chart: A('build', 'word', 'art', 'chart.png'), rule: A('build', 'word', 'art', 'gold_rule.png'),
};
const ui = n => A('brand-assets', '05_Icons', 'UI', 'PNG', 'Blue', `VCCI_UI_${n}_96px.png`);
const hero = (variant, n) => A('brand-assets', '05_Icons', 'Hero', 'PNG', variant, `VCCI_Hero_${n}_512px.png`);

// ---------------------------------------------------------------- helpers
const img = (data, wmm, hmm, extra = {}) => new ImageRun({ type: 'png', data, transformation: { width: px(wmm), height: px(hmm) }, ...extra });
const floatImg = (data, xmm, ymm, wmm, hmm, behind = true) => img(data, wmm, hmm, {
  floating: {
    horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: emu(xmm) },
    verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: emu(ymm) },
    behindDocument: behind, allowOverlap: true, lockAnchor: true,
    wrap: { type: TextWrappingType.NONE },
  },
});
const t = (text, o = {}) => new TextRun({ text, ...o });
const P = (children, o = {}) => new Paragraph({ children: Array.isArray(children) ? children : [typeof children === 'string' ? t(children) : children], ...o });
const S = (style, text, o = {}) => P(text, { style, ...o });
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none };
const cellNoBorders = { top: none, bottom: none, left: none, right: none };
const goldRule = (after = 240) => P(img(IMG.rule, 16, 0.9), { spacing: { before: 0, after } });
const rightTab = () => new PositionalTab({ alignment: PositionalTabAlignment.RIGHT, relativeTo: PositionalTabRelativeTo.MARGIN, leader: PositionalTabLeader.NONE });
// eslint-disable-next-line no-unused-vars
const frame = (xmm, ymm, wmm, hmm) => ({ type: 'absolute', position: { x: mm(xmm), y: mm(ymm) }, width: mm(wmm), height: mm(hmm),
  anchor: { horizontal: FrameAnchorType.PAGE, vertical: FrameAnchorType.PAGE }, rule: 'atLeast' });

const floatBox = (xmm, ymm, wmm, children) => new Table({
  width: { size: mm(wmm), type: WidthType.DXA }, columnWidths: [mm(wmm)], layout: TableLayoutType.FIXED, borders: noBorders,
  float: { horizontalAnchor: TableAnchorType.PAGE, verticalAnchor: TableAnchorType.PAGE,
           absoluteHorizontalPosition: mm(xmm), absoluteVerticalPosition: mm(ymm), overlap: OverlapType.OVERLAP },
  rows: [new TableRow({ children: [new TableCell({ width: { size: mm(wmm), type: WidthType.DXA }, borders: cellNoBorders,
    margins: { top: 0, bottom: 0, left: 0, right: 0 }, children })] })],
});

// ---------------------------------------------------------------- styles (shared by all templates)
const pStyle = (id, name, run, para = {}, extra = {}) => ({ id, name, basedOn: 'Normal', next: 'Normal', quickFormat: true, run, paragraph: para, ...extra });
const STYLES = {
  default: {
    document: { run: { font: F.sans, size: 20, color: C.ink }, paragraph: { spacing: { after: 140, line: 336 } } },
    heading1: { run: { font: F.serifMed, size: 44, color: C.blue }, paragraph: { spacing: { before: 120, after: 200, line: 264 }, keepNext: true, keepLines: true } },
    heading2: { run: { font: F.serifSemi, size: 28, color: C.blue }, paragraph: { spacing: { before: 360, after: 120, line: 288 }, keepNext: true } },
    heading3: { run: { font: F.sansSemi, size: 17, color: C.bronzeInk, allCaps: true, characterSpacing: 24 }, paragraph: { spacing: { before: 280, after: 80 }, keepNext: true } },
    title: { run: { font: F.serifMed, size: 68, color: C.blue }, paragraph: { spacing: { before: 0, after: 240, line: 240 } } },
    listParagraph: { run: { font: F.sans, size: 20 } },
  },
  paragraphStyles: [
    pStyle('Subtitle', 'Subtitle', { font: F.sans, size: 26, color: C.slate }, { spacing: { after: 240, line: 312 } }),
    pStyle('VCCILabel', 'VCCI Label', { font: F.sansSemi, size: 16, color: C.bronzeInk, allCaps: true, characterSpacing: 36 }, { spacing: { before: 0, after: 160 } }),
    pStyle('VCCILead', 'VCCI Lead', { font: F.serif, size: 26, color: C.blue }, { spacing: { after: 240, line: 360 } }),
    pStyle('Quote', 'Quote', { font: F.serif, italics: true, size: 26, color: C.blue },
      { spacing: { before: 240, after: 240, line: 336 }, indent: { left: mm(8) },
        border: { left: { style: BorderStyle.SINGLE, size: 24, color: C.gold, space: 14 } } }),
    pStyle('VCCICallout', 'VCCI Callout', { font: F.sans, size: 19, color: C.ink },
      { spacing: { before: 200, after: 200, line: 312 }, indent: { left: mm(4), right: mm(4) },
        shading: { type: ShadingType.CLEAR, color: 'auto', fill: C.tint },
        border: { left: { style: BorderStyle.SINGLE, size: 24, color: C.blue, space: 10 },
                  top: { style: BorderStyle.SINGLE, size: 4, color: C.tint, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 4, color: C.tint, space: 8 },
                  right: { style: BorderStyle.SINGLE, size: 4, color: C.tint, space: 10 } } }),
    pStyle('Caption', 'Caption', { font: F.sans, size: 15, color: C.slate }, { spacing: { before: 80, after: 280 } }),
    pStyle('VCCISmall', 'VCCI Small', { font: F.sans, size: 15, color: C.slate }, { spacing: { after: 40, line: 264 } }),
    pStyle('VCCIFigure', 'VCCI Figure Number', { font: F.serifMed, size: 48, color: C.blue }, { spacing: { after: 0, line: 240 } }),
    pStyle('VCCITocHeading', 'VCCI TOC Heading', { font: F.serifMed, size: 44, color: C.blue }, { spacing: { after: 360 } }),
    pStyle('Header', 'header', { font: F.sans, size: 14, color: C.slate }, { spacing: { after: 0, line: 240 } }, { next: 'Header' }),
    pStyle('Footer', 'footer', { font: F.sans, size: 14, color: C.slate }, { spacing: { after: 0, line: 240 } }, { next: 'Footer' }),
    pStyle('TOC1', 'toc 1', { font: F.serifSemi, size: 22, color: C.blue }, { spacing: { before: 200, after: 80 } }),
    pStyle('TOC2', 'toc 2', { font: F.sans, size: 19, color: C.ink }, { spacing: { after: 60 }, indent: { left: mm(6) } }),
    pStyle('TOC3', 'toc 3', { font: F.sans, size: 18, color: C.slate }, { spacing: { after: 40 }, indent: { left: mm(12) } }),
  ],
};
const NUMBERING = { config: [
  { reference: 'vcci-bullets', levels: [
    { level: 0, format: LevelFormat.BULLET, text: '■', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: mm(6), hanging: mm(4.5) } }, run: { color: C.blue, size: 12 } } },
    { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: mm(12), hanging: mm(4.5) } }, run: { color: C.slate } } } ] },
  { reference: 'vcci-numbers', levels: [
    { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: mm(6), hanging: mm(6) } }, run: { font: F.sansSemi, color: C.blue } } } ] },
] };
const bullet = (text, level = 0) => P(text, { numbering: { reference: 'vcci-bullets', level } });
const numbered = (text) => P(text, { numbering: { reference: 'vcci-numbers', level: 0 } });

const section = (o) => ({ properties: { page: { size: PAGE, margin: MARGIN }, ...(o.properties || {}) }, ...o });
const doc = (title, description, sections) => new Document({
  creator: 'VCCI', title, description, styles: STYLES, numbering: NUMBERING,
  features: { updateFields: false }, sections,
});
const save = async (d, name) => { fs.writeFileSync(path.join(OUT, name), await Packer.toBuffer(d)); console.log('wrote', name); };

// ---------------------------------------------------------------- shared header / footer parts
const lockupW = 88, lockupH = lockupW * dims.lockup[1] / dims.lockup[0];
const addressBlock = [
  'Số 9 Đào Duy Anh, Đống Đa, Hà Nội',
  'T  +84 24 3574 2022',
  'vcci.com.vn',
];
const brandHeader = (withWatermark) => new Header({ children: [
  new Table({
    width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [mm(110), CONTENT_W - mm(110)], borders: noBorders,
    layout: TableLayoutType.FIXED,
    rows: [new TableRow({ children: [
      new TableCell({ width: { size: mm(110), type: WidthType.DXA }, borders: cellNoBorders, verticalAlign: VerticalAlign.BOTTOM,
        children: [P([img(IMG.lockup, lockupW, lockupH), ...(withWatermark ? [floatImg(IMG.watermark, 130, 217, 90, 90)] : [])], { style: 'Header' })] }),
      new TableCell({ width: { size: CONTENT_W - mm(110), type: WidthType.DXA }, borders: cellNoBorders, verticalAlign: VerticalAlign.BOTTOM,
        children: addressBlock.map(a => P(a, { style: 'Header', alignment: AlignmentType.RIGHT, spacing: { after: 20 } })) }),
    ] })],
  }),
  P('', { style: 'Header', spacing: { before: 120, after: 0 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: C.stone, space: 1 } } }),
] });
const runningHeader = (label) => new Header({ children: [
  P([img(IMG.logo, 24, 24 * dims.logo[1] / dims.logo[0]), new TextRun({ children: [rightTab(), label] })],
    { style: 'Header', border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: C.stone, space: 6 } } }),
] });
const pageFooter = (left) => new Footer({ children: [
  P([t(left), new TextRun({ children: [rightTab(), 'Trang ', PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES_IN_SECTION] })], { style: 'Footer' }),
] });
const brandFooter = () => new Footer({ children: [
  P([t('Liên đoàn Thương mại và Công nghiệp Việt Nam', { font: F.sansSemi, color: C.blue }), t('  ·  Vietnam Chamber of Commerce and Industry'),
     new TextRun({ children: [rightTab(), 'vcci.com.vn'] })],
    { style: 'Footer', border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.stone, space: 6 } } }),
] });
const emptyHF = () => ({ headers: { default: new Header({ children: [P('')] }), first: new Header({ children: [P('')] }) },
                         footers: { default: new Footer({ children: [P('')] }), first: new Footer({ children: [P('')] }) } });

// =============================================================== 1. LETTERHEAD
async function letterhead() {
  const body = [
    P([t('Số: [128]/VCCI-[HV]')], { style: 'VCCISmall' }),
    P([t('Hà Nội, ngày [05] tháng [10] năm [2026]')], { style: 'VCCISmall', alignment: AlignmentType.RIGHT, spacing: { after: 360 } }),
    P([t('Kính gửi:  ', { font: F.sansSemi }), t('[Ông/Bà Họ và tên]', { font: F.sansSemi })], { spacing: { after: 40 } }),
    P('[Chức danh], [Tên doanh nghiệp / cơ quan]', { spacing: { after: 40 } }),
    P('[Địa chỉ]', { spacing: { after: 360 } }),
    S('VCCILabel', 'V/v'),
    P(t('[Tiêu đề thư: nêu ngắn gọn nội dung chính trong một hoặc hai dòng]', { font: F.serifMed, size: 30, color: C.blue }), { spacing: { after: 280, line: 300 } }),
    P('Liên đoàn Thương mại và Công nghiệp Việt Nam (VCCI) xin gửi tới Quý [Ông/Bà] lời chào trân trọng.'),
    P('[Đoạn mở đầu: bối cảnh và mục đích của thư. Viết rõ ràng, trang trọng, đi thẳng vào vấn đề. Mỗi đoạn nên có một ý chính.]'),
    P('[Đoạn nội dung: thông tin chi tiết, đề xuất hoặc yêu cầu. Khi cần liệt kê, dùng danh sách để người đọc dễ theo dõi:]'),
    bullet('[Nội dung thứ nhất]'), bullet('[Nội dung thứ hai]'), bullet('[Nội dung thứ ba]'),
    P('[Đoạn kết: bước tiếp theo, đầu mối liên hệ và thời hạn phản hồi nếu có.]', { spacing: { before: 140 } }),
    P('Trân trọng,', { spacing: { before: 280, after: 900 } }),
    P(t('[Họ và tên]', { font: F.serifMed, size: 24, color: C.blue }), { spacing: { after: 40 } }),
    P('[Chức danh]', { style: 'VCCISmall', spacing: { after: 480 } }),
    S('VCCILabel', 'Nơi nhận', { spacing: { after: 60 } }),
    P('Như trên;', { style: 'VCCISmall' }), P('Lưu: VT, [Đơn vị].', { style: 'VCCISmall' }),
  ];
  const d = doc('VCCI — Letterhead', 'Mẫu thư / văn bản có tiêu đề VCCI', [section({
    properties: { titlePage: true, page: { size: PAGE, margin: { ...MARGIN, top: mm(44) } } },
    headers: { first: brandHeader(true), default: runningHeader('Liên đoàn Thương mại và Công nghiệp Việt Nam') },
    footers: { first: brandFooter(), default: pageFooter('vcci.com.vn') },
    children: body,
  })]);
  await save(d, 'VCCI_Letterhead.docx');
}

// =============================================================== 2. REPORT
async function report() {
  const W = CONTENT_W;
  const cell = (children, w, o = {}) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: cellNoBorders,
    margins: { top: mm(3), bottom: mm(3), left: mm(3), right: mm(3) }, children, ...o });
  const kpi = (num, label) => new TableCell({ width: { size: Math.floor(W / 3), type: WidthType.DXA },
    children: [P(t(num), { style: 'VCCIFigure' }), P(label, { style: 'VCCISmall' })] });
  const keyFigures = new Table({ style: 'VCCITableTint', width: { size: W, type: WidthType.DXA }, layout: TableLayoutType.FIXED,
    columnWidths: [Math.floor(W / 3), Math.floor(W / 3), W - 2 * Math.floor(W / 3)],
    tableLook: { firstRow: false, lastRow: false, firstColumn: false, lastColumn: false, noHBand: true, noVBand: true },
    rows: [new TableRow({ children: [kpi('[67,4]', '[Chỉ số / đơn vị đo]'), kpi('[12.500]', '[Doanh nghiệp tham gia khảo sát]'), kpi('[63%]', '[Tỷ lệ đánh giá tích cực]')] })] });

  const lw = [Math.round(W * 0.3)]; lw.push(W - lw[0]);
  const lightRow = (a, b, head) => new TableRow({ tableHeader: !!head, children: [a, b].map((x, i) =>
    new TableCell({ width: { size: lw[i], type: WidthType.DXA }, children: [P(x)] })) });
  const lightTable = new Table({ style: 'VCCITableLight', width: { size: W, type: WidthType.DXA }, columnWidths: lw, layout: TableLayoutType.FIXED,
    tableLook: { firstRow: true, lastRow: false, firstColumn: true, lastColumn: false, noHBand: true, noVBand: true },
    rows: [lightRow('Hạng mục', 'Mô tả', true), lightRow('Nguồn dữ liệu', '[Khảo sát doanh nghiệp, số liệu thống kê, phỏng vấn chuyên gia]'),
           lightRow('Phạm vi', '[Số doanh nghiệp, địa bàn, ngành]'), lightRow('Thời gian', '[Tháng 03 – 08/2026]')] });

  const cols = [Math.round(W * 0.40), Math.round(W * 0.2), Math.round(W * 0.2)]; cols.push(W - cols.reduce((a, b) => a + b));
  const rowsData = [['[Tiêu chí 1]', '[64,5]', '[66,0]', '[+1,5]'], ['[Tiêu chí 2]', '[58,2]', '[61,3]', '[+3,1]'], ['[Tiêu chí 3]', '[71,0]', '[70,4]', '[–0,6]'], ['Trung bình', '[64,6]', '[65,9]', '[+1,3]']];
  const mkCell = (txt, i) => new TableCell({ width: { size: cols[i], type: WidthType.DXA },
    children: [P(txt, { alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.RIGHT })] });
  const dataTable = new Table({ style: 'VCCITable', width: { size: W, type: WidthType.DXA }, columnWidths: cols, layout: TableLayoutType.FIXED,
    tableLook: { firstRow: true, lastRow: true, firstColumn: false, lastColumn: false, noHBand: true, noVBand: true },
    rows: [new TableRow({ tableHeader: true, children: ['Tiêu chí', '2024', '2025', 'Thay đổi'].map((x, i) => mkCell(x, i)) }),
           ...rowsData.map((r) => new TableRow({ children: r.map((x, i) => mkCell(x, i)) }))] });

  const cover = section({
    properties: { titlePage: false, page: { size: PAGE, margin: { top: mm(22), bottom: mm(10), left: mm(22), right: mm(22), header: 0, footer: 0 } } },
    ...emptyHF(),
    children: [
      P([floatImg(IMG.cover, 0, 0, 210, 297), img(IMG.lockup, 96, 96 * dims.lockup[1] / dims.lockup[0])], { spacing: { after: mm(34) } }),
      S('VCCILabel', 'Báo cáo  ·  Report  ·  2026'),
      new Paragraph({ heading: HeadingLevel.TITLE, children: [t('[Tên báo cáo: tối đa ba dòng, ngắn gọn và rõ ý]')] }),
      S('Subtitle', '[Tiêu đề phụ hoặc mô tả ngắn về phạm vi, đối tượng và thời gian của báo cáo]'),
      // texts and topic icon on the blue field (floating table at fixed page position)
      floatBox(22, 205, 150, [
        P(t('[Tháng 10 / 2026]', { font: F.serifMed, size: 30, color: C.white }), { spacing: { after: 60 } }),
        P(t('[Đơn vị thực hiện]  ·  Liên đoàn Thương mại và Công nghiệp Việt Nam', { font: F.sans, size: 17, color: 'D9E1F2' }), { spacing: { after: 360 } }),
        P(img(hero('Gold-on-dark', '03_business-environment-reform'), 26, 26), { spacing: { after: 0 } }),
      ]),
      P('', { spacing: { after: 0 } }),
    ],
  });

  const body = section({
    properties: { titlePage: false, page: { size: PAGE, margin: MARGIN, pageNumbers: { start: 1 } } },
    headers: { default: runningHeader('[Tên báo cáo rút gọn]  ·  2026') },
    footers: { default: pageFooter('vcci.com.vn') },
    children: [
      S('VCCITocHeading', 'Mục lục'),
      new TableOfContents('Mục lục', { hyperlink: true, headingStyleRange: '1-3' }),
      P(new PageBreak()),
      S('VCCILabel', 'Chương 01'),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t('Tóm tắt')] }),
      goldRule(),
      S('VCCILead', '[Đoạn dẫn: hai đến ba câu nêu thông điệp quan trọng nhất của báo cáo. Đây là đoạn người đọc bận rộn sẽ đọc đầu tiên.]'),
      P('[Đoạn thân bài. Kiểu chữ Be Vietnam Pro 10 pt, giãn dòng 1,4. Mỗi đoạn nên giữ một ý; với văn bản dài, chia mục bằng các cấp tiêu đề để mục lục tự cập nhật.]'),
      keyFigures,
      P('', { spacing: { after: 120 } }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t('Những phát hiện chính')] }),
      bullet('[Phát hiện thứ nhất, viết thành một câu hoàn chỉnh]'),
      bullet('[Phát hiện thứ hai]'), bullet('[Ý phụ của phát hiện thứ hai]', 1), bullet('[Phát hiện thứ ba]'),
      S('VCCICallout', '[Hộp nhấn mạnh (kiểu VCCI Callout): dùng cho khuyến nghị, định nghĩa hoặc lưu ý quan trọng. Không dùng quá một hộp trên một trang.]'),
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [t('Phương pháp')] }),
      P('[Mô tả ngắn phạm vi, nguồn dữ liệu và phương pháp phân tích.]'),
      numbered('[Bước thứ nhất]'), numbered('[Bước thứ hai]'), numbered('[Bước thứ ba]'),
      S('Caption', 'Bảng 1.  Phạm vi khảo sát  ·  kiểu VCCI Table Light', { spacing: { before: 200, after: 80 } }),
      lightTable,
      S('VCCILabel', 'Chương 02', { pageBreakBefore: true }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t('Phân tích')] }),
      goldRule(),
      P('[Đoạn mở đầu chương. Bảng dưới đây dùng kiểu VCCI Table: chọn bảng, vào Table Design và chọn VCCI Table; bật Header Row và Total Row. Số căn phải.]'),
      S('Caption', 'Bảng 2.  [Tên bảng]  ·  Nguồn: [nguồn dữ liệu]  ·  kiểu VCCI Table', { spacing: { before: 200, after: 80 } }),
      dataTable,
      P('', { spacing: { after: 200 } }),
      P(img(IMG.chart, W / MM, (W / MM) * 820 / 1600)),
      S('Caption', 'Hình 1.  [Tên biểu đồ; số liệu minh họa]  ·  Nguồn: [nguồn dữ liệu]'),
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t('[Tiêu đề cấp 2]')] }),
      P('[Đoạn thân bài.]'),
      S('Quote', '“[Trích dẫn: ý kiến của doanh nghiệp, chuyên gia hoặc lãnh đạo, tối đa ba dòng.]”', { keepNext: true }),
      P(t('— [Họ và tên], [Chức danh]', { color: C.slate, size: 17 }), { spacing: { before: 0, after: 280 } }),
      P('[Đoạn thân bài tiếp theo.]'),
    ],
  });

  const back = section({
    properties: { page: { size: PAGE, margin: { top: mm(10), bottom: mm(10), left: mm(22), right: mm(22), header: 0, footer: 0 } } },
    ...emptyHF(),
    children: [
      P([floatImg(IMG.back, 0, 0, 210, 297)], { spacing: { after: 0 } }),
      floatBox(30, 238, 150, [
        P(t('Liên đoàn Thương mại và Công nghiệp Việt Nam', { font: F.sansSemi, size: 18, color: C.blue }), { spacing: { after: 60 } }),
        P(t('Số 9 Đào Duy Anh, Đống Đa, Hà Nội  ·  T +84 24 3574 2022  ·  vcci.com.vn', { size: 16, color: C.slate }), { spacing: { after: 60 } }),
        P(t('[Đầu mối liên hệ: Họ và tên · email@vcci.com.vn]', { size: 16, color: C.slate }), { spacing: { after: 0 } }),
      ]),
      P('', { spacing: { after: 0 } }),
    ],
  });
  const only = (process.env.REPORT_PARTS || 'cover,body,back').split(',');
  const parts = { cover, body, back };
  await save(doc('VCCI — Report', 'Mẫu báo cáo VCCI: bìa, mục lục, thân bài, bìa sau', only.map(k => parts[k])), 'VCCI_Report.docx');
}

// =============================================================== 3. INVITATION
async function invitation() {
  const W = CONTENT_W, c1 = mm(44), c2 = W - c1;
  const row = (icon, label, lines) => new TableRow({ children: [
    new TableCell({ width: { size: c1, type: WidthType.DXA }, verticalAlign: VerticalAlign.TOP, margins: { top: mm(1.8), bottom: mm(1.8), left: 0, right: mm(2) },
      children: [P([img(ui(icon), 5, 5), t('   '), t(label, { font: F.sansSemi, size: 16, color: C.bronzeInk, allCaps: true, characterSpacing: 30 })], { spacing: { after: 0 } })] }),
    new TableCell({ width: { size: c2, type: WidthType.DXA }, verticalAlign: VerticalAlign.TOP, margins: { top: mm(1.8), bottom: mm(1.8), left: mm(2), right: 0 },
      children: lines.map((l, i) => P(t(l, i === 0 ? { font: F.sansSemi, color: C.ink } : { color: C.slate, size: 18 }), { spacing: { after: 20 } })) }),
  ] });
  const details = new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [c1, c2], layout: TableLayoutType.FIXED,
    borders: { top: { style: BorderStyle.SINGLE, size: 8, color: C.blue }, bottom: { style: BorderStyle.SINGLE, size: 4, color: C.stone },
               left: none, right: none, insideVertical: none, insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: C.stone } },
    rows: [
      row('calendar', 'Thời gian', ['[08:30 – 12:00, Thứ Bảy, ngày 12/12/2026]', '[Đón tiếp đại biểu từ 08:00]']),
      row('map-pin', 'Địa điểm', ['[Trung tâm Hội nghị Quốc gia]', '[Đại lộ Thăng Long, Nam Từ Liêm, Hà Nội]']),
      row('landmark', 'Chủ trì', ['[Họ và tên]', '[Chức danh], Liên đoàn Thương mại và Công nghiệp Việt Nam']),
      row('mail', 'Xác nhận', ['[Trước ngày 05/12/2026]', '[Họ và tên đầu mối] · [email@vcci.com.vn] · [+84 24 3574 2022]']),
    ] });
  const agenda = [['08:00', 'Đón tiếp đại biểu'], ['08:30', 'Phát biểu khai mạc'], ['09:00', '[Phiên thảo luận chuyên đề]'], ['11:30', 'Tổng kết và bế mạc']];
  const L = Math.round(W * 0.56), R = W - L, aw1 = mm(18);
  const agendaTable = new Table({ width: { size: L - mm(6), type: WidthType.DXA }, columnWidths: [aw1, L - mm(6) - aw1], layout: TableLayoutType.FIXED, borders: noBorders,
    rows: agenda.map(([a, b]) => new TableRow({ children: [
      new TableCell({ width: { size: aw1, type: WidthType.DXA }, margins: { top: mm(0.4), bottom: mm(0.4), left: 0, right: 0 }, children: [P(t(a, { font: F.serifMed, color: C.blue }), { spacing: { after: 0 } })] }),
      new TableCell({ width: { size: L - mm(6) - aw1, type: WidthType.DXA }, margins: { top: mm(0.4), bottom: mm(0.4), left: 0, right: 0 }, children: [P(b, { spacing: { after: 0 } })] }),
    ] })) });
  const bottomBlock = new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [L, R], layout: TableLayoutType.FIXED, borders: noBorders,
    rows: [new TableRow({ children: [
      new TableCell({ width: { size: L, type: WidthType.DXA }, borders: cellNoBorders, margins: { top: 0, bottom: 0, left: 0, right: mm(6) }, children: [
        new Paragraph({ heading: HeadingLevel.HEADING_3, children: [t('Chương trình dự kiến')], spacing: { before: 0, after: 80 } }), agendaTable] }),
      new TableCell({ width: { size: R, type: WidthType.DXA }, borders: cellNoBorders, margins: { top: 0, bottom: 0, left: mm(4), right: 0 }, children: [
        P('Sự hiện diện của Quý [Ông/Bà] là niềm vinh dự đối với Ban Tổ chức.', { spacing: { after: 80 } }),
        P('Trân trọng,', { spacing: { after: 560 } }),
        P(t('[Họ và tên]', { font: F.serifMed, size: 24, color: C.blue }), { spacing: { after: 40 } }),
        P('[Chức danh], Liên đoàn Thương mại và Công nghiệp Việt Nam', { style: 'VCCISmall' })] }),
    ] })] });
  const footer = new Footer({ children: [
    P([floatImg(IMG.band, 0, 267, 210, 30), t('vcci.com.vn', { font: F.sansSemi, color: C.white }),
       new TextRun({ children: [rightTab(), 'Liên đoàn Thương mại và Công nghiệp Việt Nam'], color: 'D9E1F2' })], { style: 'Footer' }),
  ] });
  const d = doc('VCCI — Invitation', 'Mẫu thư mời sự kiện VCCI', [section({
    properties: { titlePage: true, page: { size: PAGE, margin: { ...MARGIN, top: mm(41), bottom: mm(33), footer: mm(13) } } },
    headers: { first: brandHeader(false), default: runningHeader('Thư mời') },
    footers: { first: footer, default: pageFooter('vcci.com.vn') },
    children: [
      P([floatImg(hero('Blue-Gold', '20_forum-events'), 160, 49, 28, 28, false)], { spacing: { after: 0 } }),
      S('VCCILabel', 'Thư mời  ·  Invitation'),
      P(t('[Tên sự kiện: Diễn đàn Doanh nghiệp Việt Nam 2026]', { font: F.serifMed, size: 46, color: C.blue }), { spacing: { after: 140, line: 252 }, indent: { right: mm(36) } }),
      goldRule(220),
      P('Liên đoàn Thương mại và Công nghiệp Việt Nam (VCCI) trân trọng kính mời'),
      P(t('[Ông/Bà Họ và tên]', { font: F.serifMed, size: 30, color: C.blue }), { spacing: { after: 40 } }),
      P('[Chức danh], [Tên doanh nghiệp / cơ quan]', { style: 'VCCISmall', spacing: { after: 200 } }),
      P('tham dự [tên sự kiện], với chủ đề “[chủ đề sự kiện]”. [Một đến hai câu giới thiệu mục đích và điểm nổi bật của sự kiện.]', { spacing: { after: 240 } }),
      details,
      P('', { spacing: { after: 160 } }),
      bottomBlock,
    ],
  })]);
  await save(d, 'VCCI_Invitation.docx');
}

(async () => { await letterhead(); await report(); await invitation(); })().catch(e => { console.error(e); process.exit(1); });
