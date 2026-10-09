// VCCI PowerPoint template: 18 slide layouts (11 light, 7 blue) + a sample deck that demonstrates each layout.
// Output: build/ppt/out/VCCI_Presentation.pptx  (post-processed into .potx by tools/ppt/finalize.py)
// Run from the repository root: node tools/ppt/make_pptx.js
const path = require('path');
const fs = require('fs');
const pptxgen = require('pptxgenjs');

const ROOT = process.cwd();
const A = (...p) => path.join(ROOT, ...p);
const ART = (n) => A('build', 'ppt', 'art', n);
const OUT = A('build', 'ppt', 'out'); fs.mkdirSync(OUT, { recursive: true });

const C = { blue: '264896', gold: 'FFCD00', bronze: 'CC713C', ink2: '9C570C', deep: '0B1A4F', tint: 'E7ECF6', ink: '161A26',
            slate: '5C6478', stone: 'E6E1D5', ivory: 'F4F0E6', paper: 'FBF9F4', white: 'FFFFFF', mist: 'C9D3EA' };
const F = { serif: 'Lora', serifMed: 'Lora Medium', sans: 'Be Vietnam Pro', sansSemi: 'Be Vietnam Pro SemiBold' };
const LOGO = A('brand-assets', '01_Logo', 'PNG', 'VCCI_Logo_Primary_1200px.png');            // 1200 x 361
const PLATE = A('brand-assets', '01_Logo', 'PNG', 'VCCI_Logo_Primary_Plate_1200px.png');      // plate version
const HERO = (v, n) => A('brand-assets', '05_Icons', 'Hero', 'PNG', v, `VCCI_Hero_${n}_512px.png`);
const ICON = (n) => A('brand-assets', '05_Icons', 'UI', 'PNG', 'Blue', `VCCI_UI_${n}_96px.png`);

const W = 13.333, H = 7.5, L = 0.8, R = W - 0.8, CW = R - L;   // content width 11.733 in
const LOGO_AR = 361 / 1200;

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'VCCI';
pptx.company = 'Liên đoàn Thương mại và Công nghiệp Việt Nam';
pptx.title = 'VCCI — Template trình chiếu';
pptx.theme = { headFontFace: F.serifMed, bodyFontFace: F.sans };

// ---------------------------------------------------------------- helpers
const ph = (name, type, x, y, w, h, text, o = {}) => ({ placeholder: { options: { name, type, x, y, w, h, margin: 0, ...o }, text } });
const rect = (x, y, w, h, fill) => ({ rect: { x, y, w, h, fill: { color: fill }, line: { type: 'none' } } });
const goldRule = (x, y) => rect(x, y, 0.62, 0.055, C.gold);
const img = (p, x, y, w, h) => ({ image: { path: p, x, y, w, h } });
const sldNum = (color) => ({ x: R - 0.8, y: 6.93, w: 0.8, h: 0.3, fontFace: F.sans, fontSize: 10, color, align: 'right' });
const titleOpts = (o = {}) => ({ fontFace: F.serifMed, fontSize: 30, color: C.blue, valign: 'bottom', align: 'left', ...o });
const bodyOpts = (o = {}) => ({ align: 'left', fontFace: F.sans, fontSize: 18, color: C.ink, valign: 'top', paraSpaceAfter: 8, lineSpacingMultiple: 1.1, ...o });
const labelOpts = (o = {}) => ({ fontFace: F.sansSemi, fontSize: 11, color: C.ink2, charSpacing: 2.5, valign: 'bottom', ...o });

// light chrome: paper background, small logo top-right, slide number
const lightObjects = () => [img(LOGO, R - 1.3, 0.42, 1.3, 1.3 * LOGO_AR)];
const lightMaster = (title, objects) => pptx.defineSlideMaster({ title, background: { color: C.paper }, objects: [...lightObjects(), ...objects], slideNumber: sldNum(C.slate) });
const blueMaster = (title, art, objects, num = true) => pptx.defineSlideMaster({ title, background: { path: ART(art) }, objects, ...(num ? { slideNumber: sldNum('B9C6E4') } : {}) });

const TITLE = (o = {}) => ph('title', 'title', L, 0.5, CW - 1.7, 0.95, 'Tiêu đề slide', titleOpts(o));
const RULE = goldRule(L, 1.62);

// =============================================================== LAYOUTS
// 01 light cover
pptx.defineSlideMaster({ title: 'L01', background: { path: ART('cover_light.png') }, objects: [
  img(LOGO, L, 0.75, 3.4, 3.4 * LOGO_AR),
  goldRule(L, 2.55),
  ph('title', 'title', L, 2.75, 6.9, 1.9, 'Tên bài trình bày', titleOpts({ fontSize: 36, valign: 'top' })),
  ph('subtitleEN', 'body', L, 4.75, 6.9, 0.6, 'English title (optional)', { fontFace: F.serif, italic: true, fontSize: 17, color: C.slate }),
  ph('meta', 'body', L, 6.25, 6.9, 0.55, 'Người trình bày · Sự kiện · Hà Nội, ngày/tháng/năm', { fontFace: F.sans, fontSize: 13, color: C.slate, valign: 'bottom' }),
] });
// 02 agenda
lightMaster('L02', [
  TITLE(), RULE,
  ph('body', 'body', L, 2.0, CW, 4.6, 'Mục 1\nMục 2\nMục 3', bodyOpts({ fontSize: 20, paraSpaceAfter: 14 })),
]);
// 03 title + content
lightMaster('L03', [TITLE(), RULE, ph('body', 'body', L, 2.0, CW, 4.6, 'Nội dung', bodyOpts())]);
// 04 two columns
lightMaster('L04', [TITLE(), RULE,
  ph('left', 'body', L, 2.0, CW / 2 - 0.3, 4.6, 'Cột trái', bodyOpts()),
  ph('right', 'body', L + CW / 2 + 0.3, 2.0, CW / 2 - 0.3, 4.6, 'Cột phải', bodyOpts())]);
// 05 comparison
lightMaster('L05', [TITLE(), RULE,
  ph('labelL', 'body', L, 2.0, CW / 2 - 0.3, 0.4, 'NHÃN CỘT TRÁI', labelOpts()),
  rect(L, 2.48, CW / 2 - 0.3, 0.02, C.blue),
  ph('left', 'body', L, 2.7, CW / 2 - 0.3, 3.9, 'Nội dung', bodyOpts()),
  ph('labelR', 'body', L + CW / 2 + 0.3, 2.0, CW / 2 - 0.3, 0.4, 'NHÃN CỘT PHẢI', labelOpts()),
  rect(L + CW / 2 + 0.3, 2.48, CW / 2 - 0.3, 0.02, C.blue),
  ph('right', 'body', L + CW / 2 + 0.3, 2.7, CW / 2 - 0.3, 3.9, 'Nội dung', bodyOpts())]);
// 06 dense
lightMaster('L06', [TITLE({ fontSize: 24 }), RULE,
  ph('left', 'body', L, 1.95, CW / 2 - 0.25, 4.7, 'Nội dung chi tiết (14 pt) cho bài gửi đọc', bodyOpts({ fontSize: 14, paraSpaceAfter: 6 })),
  ph('right', 'body', L + CW / 2 + 0.25, 1.95, CW / 2 - 0.25, 4.7, 'Nội dung chi tiết', bodyOpts({ fontSize: 14, paraSpaceAfter: 6 }))]);
// 07 chart / table
lightMaster('L07', [TITLE(), RULE,
  ph('takeaway', 'body', R - 3.3, 2.0, 3.3, 4.1, 'Thông điệp chính của biểu đồ', bodyOpts({ fontFace: F.serif, fontSize: 18, color: C.blue })),
  ph('source', 'body', L, 6.3, CW - 3.7, 0.35, 'Nguồn: …', { fontFace: F.sans, fontSize: 10, color: C.slate, valign: 'bottom' })]);
// 08 image + text
pptx.defineSlideMaster({ title: 'L08', background: { color: C.paper }, slideNumber: sldNum(C.slate), objects: [
  rect(0, 0, 6.2, H, C.stone),
  ph('pic', 'pic', 0, 0, 6.2, H, 'Chèn ảnh'),
  img(LOGO, R - 1.3, 0.42, 1.3, 1.3 * LOGO_AR),
  ph('title', 'title', 6.9, 1.35, R - 6.9, 1.5, 'Tiêu đề', titleOpts({ fontSize: 28 })),
  goldRule(6.9, 3.02),
  ph('body', 'body', 6.9, 3.35, R - 6.9, 3.2, 'Nội dung', bodyOpts())] });
// 09 speakers
const spW = (CW - 3 * 0.45) / 4;
lightMaster('L09', [TITLE(), RULE, ...[0, 1, 2, 3].flatMap(i => {
  const x = L + i * (spW + 0.45);
  return [rect(x, 2.0, spW, spW * 0.95, C.stone), ph(`pic${i + 1}`, 'pic', x, 2.0, spW, spW * 0.95, 'Ảnh'),
          ph(`name${i + 1}`, 'body', x, 2.12 + spW * 0.95, spW, 1.4, 'Họ và tên\nChức danh, đơn vị', bodyOpts({ fontSize: 14, paraSpaceAfter: 2 }))];
})]);
// 10 title only, 11 blank
lightMaster('L10', [TITLE(), RULE]);
lightMaster('L11', []);

// 12 event cover (blue): logo on paper plate
blueMaster('L12', 'blue_event.png', [
  img(PLATE, L, 0.7, 3.4, 3.4 * 476 / 1200),
  goldRule(L, 2.75),
  ph('title', 'title', L, 2.95, 7.6, 2.0, 'Tên sự kiện', titleOpts({ fontSize: 44, color: C.white, valign: 'top' })),
  ph('subtitleEN', 'body', L, 5.0, 7.6, 0.6, 'English event name', { fontFace: F.serif, italic: true, fontSize: 18, color: C.mist }),
  ph('meta', 'body', L, 6.25, 7.6, 0.55, 'Hà Nội · ngày/tháng/năm', { fontFace: F.sans, fontSize: 13, color: C.mist, valign: 'bottom' })], false);
// 13 section divider
blueMaster('L13', 'blue_section.png', [
  ph('num', 'body', L, 1.05, 3.5, 1.5, '01', { fontFace: F.serifMed, fontSize: 88, color: C.gold, valign: 'bottom' }),
  ph('title', 'title', L, 2.75, 7.6, 1.9, 'Tên chương', titleOpts({ fontSize: 40, color: C.white, valign: 'top' })),
  ph('subtitleEN', 'body', L, 4.75, 7.6, 0.6, 'Chapter title in English', { fontFace: F.serif, italic: true, fontSize: 17, color: C.mist }),
  ph('icon', 'pic', 10.75 - 0.85, 3.75 - 0.85, 1.7, 1.7, 'Hero icon')]);
// 14 key figures
const kW = (CW - 2 * 0.5) / 3;
blueMaster('L14', 'blue_plain.png', [
  ph('title', 'title', L, 0.6, CW, 0.9, 'Số liệu nổi bật', titleOpts({ fontSize: 28, color: C.white })),
  ...[0, 1, 2].flatMap(i => {
    const x = L + i * (kW + 0.5);
    return [rect(x, 2.3, kW, 0.03, '6F86C2'),
            ph(`fig${i + 1}`, 'body', x, 2.5, kW, 1.5, '00', { fontFace: F.serifMed, fontSize: 60, color: i === 0 ? C.gold : C.white, valign: 'top' }),
            ph(`label${i + 1}`, 'body', x, 4.1, kW, 1.6, 'Mô tả ngắn cho con số', { fontFace: F.sans, fontSize: 16, color: C.mist, valign: 'top' })];
  })]);
// 15 statement
blueMaster('L15', 'blue_plain.png', [
  goldRule(L, 1.75),
  ph('title', 'title', L, 2.0, 10.4, 3.2, 'Một câu thông điệp lớn, tối đa ba dòng.', titleOpts({ fontSize: 44, color: C.white, valign: 'top' })),
  ph('note', 'body', L, 5.5, 8, 0.5, 'Ghi chú hoặc nguồn', { fontFace: F.sans, fontSize: 14, color: C.mist })]);
// 16 quote
blueMaster('L16', 'blue_plain.png', [
  { text: { text: '“', options: { x: L - 0.05, y: 0.75, w: 1.2, h: 1.4, fontFace: F.serif, fontSize: 120, color: C.gold, margin: 0 } } },
  ph('title', 'title', L, 2.05, 10.4, 2.8, 'Nội dung trích dẫn, tối đa bốn dòng.', titleOpts({ fontFace: F.serif, italic: true, fontSize: 32, color: C.white, valign: 'top' })),
  ph('who', 'body', L, 5.2, 8, 0.9, 'Họ và tên\nChức danh, đơn vị', { fontFace: F.sans, fontSize: 14, color: C.mist })]);
// 17 full photo with blue caption band
pptx.defineSlideMaster({ title: 'L17', background: { color: C.blue }, slideNumber: sldNum('B9C6E4'), objects: [
  rect(0, 0, W, H - 1.15, C.stone),
  ph('pic', 'pic', 0, 0, W, H - 1.15, 'Chèn ảnh'),
  { image: { path: ART('blue_plain.png'), x: 0, y: H - 1.15, w: W, h: 1.15, sizing: { type: 'crop', x: 0, y: H - 1.15, w: W, h: 1.15 } } },
  ph('caption', 'body', L, H - 1.0, CW - 1.2, 0.7, 'Chú thích ảnh', { fontFace: F.sans, fontSize: 14, color: C.white, valign: 'middle' })] });
// 18 closing
blueMaster('L18', 'blue_closing.png', [
  ph('title', 'title', 6.9, 1.2, 5.6, 1.4, 'Cảm ơn', titleOpts({ fontSize: 54, color: C.white })),
  ph('subtitleEN', 'body', 6.9, 2.65, 5.6, 0.6, 'Thank you', { fontFace: F.serif, italic: true, fontSize: 20, color: C.mist }),
  img(LOGO, 7.3, 4.0, 2.6, 2.6 * LOGO_AR),
  ph('contact', 'body', 7.3, 4.95, 4.9, 1.55, 'Liên đoàn Thương mại và Công nghiệp Việt Nam\nSố 9 Đào Duy Anh, Đống Đa, Hà Nội\nvcci.com.vn',
     { fontFace: F.sans, fontSize: 12, color: C.slate, paraSpaceAfter: 2 })], false);

// =============================================================== SAMPLE DECK
const SAMPLES = process.env.SAMPLES || 'all';
const want = (k) => SAMPLES === 'all' || SAMPLES.split(',').includes(k);
const note = (s, text) => s.addNotes(text);
const tip = (s, text, color = C.slate) => s.addText(text, { x: L, y: 6.3, w: 8.5, h: 0.4, fontFace: F.sans, fontSize: 9, italic: false, color, margin: 0 });
const S = (layout) => pptx.addSlide({ masterName: layout });
if (SAMPLES !== 'none') {

let s = S('L01');
s.addText('Môi trường kinh doanh Việt Nam 2026: góc nhìn từ doanh nghiệp', { placeholder: 'title' });
s.addText('Vietnam business environment 2026: the enterprise perspective', { placeholder: 'subtitleEN' });
s.addText('[Họ và tên] · Diễn đàn Doanh nghiệp 2026 · Hà Nội, 12/12/2026', { placeholder: 'meta' });
note(s, 'Layout 01 – Bìa sáng. Dùng cho họp, làm việc với đối tác, bài gửi đọc. Tiêu đề tối đa 3 dòng.');

s = S('L12');
s.addText('Diễn đàn Doanh nghiệp Việt Nam 2026', { placeholder: 'title' });
s.addText('Vietnam Business Forum 2026', { placeholder: 'subtitleEN' });
s.addText('Trung tâm Hội nghị Quốc gia · Hà Nội · 12/12/2026', { placeholder: 'meta' });
note(s, 'Layout 12 – Bìa sự kiện (nền xanh). Logo luôn nằm trên ô nền sáng. Dùng cho sân khấu, màn hình LED.');

s = S('L02');
s.addText('Chương trình', { placeholder: 'title' });
s.addText([
  { text: '08:30   ', options: { fontFace: F.serifMed, color: C.blue } }, { text: 'Khai mạc và phát biểu chào mừng', options: { breakLine: true } },
  { text: '09:00   ', options: { fontFace: F.serifMed, color: C.blue } }, { text: 'Phiên 1 · Cải cách môi trường kinh doanh', options: { breakLine: true } },
  { text: '10:30   ', options: { fontFace: F.serifMed, color: C.blue } }, { text: 'Phiên 2 · Chuyển đổi xanh và chuyển đổi số', options: { breakLine: true } },
  { text: '11:45   ', options: { fontFace: F.serifMed, color: C.blue } }, { text: 'Tổng kết và bế mạc' },
], { placeholder: 'body' });
note(s, 'Layout 02 – Chương trình / Mục lục.');

s = S('L13');
s.addText('01', { placeholder: 'num' });
s.addText('Bức tranh môi trường kinh doanh', { placeholder: 'title' });
s.addText('The business environment at a glance', { placeholder: 'subtitleEN' });
s.addImage({ path: HERO('Gold-on-dark', '03_business-environment-reform'), placeholder: 'icon', x: 10.75 - 0.85, y: 3.75 - 0.85, w: 1.7, h: 1.7 });
note(s, 'Layout 13 – Chuyển chương. Đổi hero icon theo chủ đề: nhấp chuột phải vào icon → Change Picture → chọn file trong 05_Icons/Hero/PNG/Gold-on-dark.');

s = S('L03');
s.addText('Những phát hiện chính', { placeholder: 'title' });
s.addText([
  { text: 'Chi phí tuân thủ thủ tục hành chính tiếp tục giảm ở phần lớn các tỉnh, thành phố.', options: { bullet: { code: '25A0' }, breakLine: true } },
  { text: 'Doanh nghiệp đánh giá cao chuyển đổi số trong dịch vụ công trực tuyến.', options: { bullet: { code: '25A0' }, breakLine: true } },
  { text: 'Tiếp cận đất đai và tín dụng vẫn là hai rào cản lớn nhất.', options: { bullet: { code: '25A0' }, breakLine: true } },
  { text: 'Mỗi slide một thông điệp; tối đa 5 ý, mỗi ý một câu.', options: { bullet: { code: '25A0' } } },
], { placeholder: 'body' });
note(s, 'Layout 03 – Tiêu đề và nội dung. Thân bài 18 pt.');

s = S('L04');
s.addText('Bối cảnh và đề xuất', { placeholder: 'title' });
s.addText('Bối cảnh: mô tả ngắn tình hình, số liệu chính và vấn đề cần giải quyết. Viết rõ ràng, mỗi đoạn một ý.', { placeholder: 'left' });
s.addText('Đề xuất: các giải pháp cụ thể, đầu mối thực hiện và mốc thời gian. Mỗi đề xuất nên đo lường được.', { placeholder: 'right' });

s = S('L05');
s.addText('Trước và sau cải cách', { placeholder: 'title' });
s.addText('TRƯỚC 2024', { placeholder: 'labelL' });
s.addText('Thủ tục cấp phép: 22 ngày\nHồ sơ giấy, nộp trực tiếp\nNhiều đầu mối xử lý', { placeholder: 'left' });
s.addText('SAU 2025', { placeholder: 'labelR' });
s.addText('Thủ tục cấp phép: 9 ngày\nHồ sơ điện tử, liên thông\nMột cửa, một đầu mối', { placeholder: 'right' });
note(s, 'Số liệu trong slide mẫu chỉ để minh họa.');

s = S('L14');
s.addText('Kết quả khảo sát 2026', { placeholder: 'title' });
s.addText('12.500', { placeholder: 'fig1' }); s.addText('doanh nghiệp tham gia khảo sát', { placeholder: 'label1' });
s.addText('34', { placeholder: 'fig2' }); s.addText('tỉnh, thành phố được đánh giá', { placeholder: 'label2' });
s.addText('71%', { placeholder: 'fig3' }); s.addText('đánh giá môi trường kinh doanh cải thiện', { placeholder: 'label3' });
note(s, 'Layout 14 – Số liệu nổi bật. Chỉ con số đầu tiên màu vàng (một điểm nhấn vàng). Số liệu minh họa.');

s = S('L07');
s.addText('Chỉ số theo năm', { placeholder: 'title' });
s.addChart(pptx.ChartType.bar, [{ name: 'Chỉ số', labels: ['2021', '2022', '2023', '2024', '2025'], values: [63.2, 64.5, 65.1, 66.0, 67.4] }], {
  x: L, y: 2.0, w: CW - 3.7, h: 4.2, barDir: 'col', chartColors: [C.blue, C.blue, C.blue, C.blue, C.gold], valAxisMinVal: 0, valAxisMaxVal: 80, valAxisMajorUnit: 20, dataLabelFormatCode: '0.0', valAxisLabelFormatCode: '0',
  showValue: true, dataLabelFontFace: F.serifMed, dataLabelFontSize: 12, dataLabelColor: C.blue, dataLabelPosition: 'outEnd',
  catAxisLabelFontFace: F.sans, catAxisLabelFontSize: 11, catAxisLabelColor: C.slate, valAxisLabelFontFace: F.sans, valAxisLabelFontSize: 10,
  valAxisLabelColor: C.slate, valGridLine: { color: C.stone, size: 0.75 }, catAxisLineColor: C.slate, valAxisLineShow: false, barGapWidthPct: 70,
  showLegend: false });
s.addText('Chỉ số tăng đều qua 5 năm; năm 2025 đạt mức cao nhất (cột vàng).', { placeholder: 'takeaway' });
s.addText('Nguồn: VCCI · số liệu minh họa', { placeholder: 'source' });
note(s, 'Biểu đồ thật của PowerPoint: nhấp chuột phải → Edit Data. Dùng một cột vàng cho giá trị cần nhấn mạnh, còn lại màu xanh.');

s = S('L10');
s.addText('Bảng số liệu', { placeholder: 'title' });
const hdr = (t, al) => ({ text: t, options: { bold: false, fontFace: F.sansSemi, color: C.white, fill: { color: C.blue }, align: al } });
const cell = (t, al, last) => ({ text: t, options: { align: al, fontFace: last ? F.sansSemi : F.sans, fill: { color: last ? C.ivory : C.paper } } });
const rows = [['Tiêu chí', '2024', '2025', 'Thay đổi'], ['Gia nhập thị trường', '64,5', '66,0', '+1,5'], ['Chi phí thời gian', '58,2', '61,3', '+3,1'],
              ['Tính minh bạch', '71,0', '70,4', '–0,6'], ['Trung bình', '64,6', '65,9', '+1,3']];
s.addTable(rows.map((r, ri) => r.map((t, ci) => ri === 0 ? hdr(t, ci ? 'right' : 'left') : cell(t, ci ? 'right' : 'left', ri === rows.length - 1))), {
  x: L, y: 2.0, w: CW, colW: [CW * 0.4, CW * 0.2, CW * 0.2, CW * 0.2], fontFace: F.sans, fontSize: 14, color: C.ink, rowH: 0.5, valign: 'middle',
  margin: [0.04, 0.12, 0.04, 0.12],
  border: [{ type: 'none' }, { type: 'none' }, { pt: 0.75, color: C.stone }, { type: 'none' }] });
tip(s, 'Bảng: hàng tiêu đề nền xanh, kẻ ngang mảnh, hàng tổng nền Ivory, số căn phải. Số liệu minh họa.');

s = S('L08');
s.addText('Doanh nghiệp là trung tâm', { placeholder: 'title' });
s.addText('Dùng ảnh thật về doanh nghiệp, nhà máy, hội nghị. Nhấp vào khung bên trái để chèn ảnh; ảnh tự cắt vừa khung.', { placeholder: 'body' });

s = S('L09');
s.addText('Diễn giả', { placeholder: 'title' });
['Họ và tên\nChức danh, Liên đoàn Thương mại và Công nghiệp Việt Nam', 'Họ và tên\nChức danh, cơ quan', 'Họ và tên\nChức danh, doanh nghiệp', 'Họ và tên\nChức danh, tổ chức quốc tế']
  .forEach((t, i) => s.addText(t, { placeholder: `name${i + 1}` }));

s = S('L15');
s.addText('Doanh nghiệp vững mạnh là nền tảng của một nền kinh tế tự chủ.', { placeholder: 'title' });
s.addText('Thông điệp của Diễn đàn Doanh nghiệp 2026', { placeholder: 'note' });

s = S('L16');
s.addText('Điều doanh nghiệp cần nhất là một môi trường kinh doanh ổn định, minh bạch và có thể dự báo được.', { placeholder: 'title' });
s.addText('[Họ và tên]\n[Chức danh, doanh nghiệp]', { placeholder: 'who' });

s = S('L06');
s.addText('Phương pháp và phạm vi khảo sát', { placeholder: 'title' });
s.addText('Layout dành cho bài trình bày gửi qua email để người nhận tự đọc. Chữ 14 pt cho phép đưa nhiều nội dung hơn, nhưng vẫn cần chia đoạn rõ ràng và dùng tiêu đề nhỏ.\n\nPhạm vi: [số doanh nghiệp], [địa bàn], [ngành].\nThời gian: [tháng 03 – 08/2026].\nNguồn dữ liệu: khảo sát doanh nghiệp, số liệu thống kê, phỏng vấn chuyên gia.', { placeholder: 'left' });
s.addText('Phương pháp: [mô tả cách chọn mẫu, bảng hỏi, cách tính chỉ số].\n\nHạn chế: [nêu các giới hạn của số liệu để người đọc diễn giải đúng].\n\nKhông dùng layout này để trình chiếu trên sân khấu.', { placeholder: 'right' });

s = S('L17');
s.addText('Chú thích ảnh: sự kiện, địa điểm, thời gian · Ảnh: [tác giả]', { placeholder: 'caption' });

s = S('L18');
s.addText('Cảm ơn', { placeholder: 'title' });
s.addText('Thank you', { placeholder: 'subtitleEN' });
s.addText('Liên đoàn Thương mại và Công nghiệp Việt Nam\nSố 9 Đào Duy Anh, Đống Đa, Hà Nội\n[email@vcci.com.vn] · vcci.com.vn', { placeholder: 'contact' });

}
pptx.writeFile({ fileName: path.join(OUT, process.env.OUTNAME || 'VCCI_Presentation.pptx') }).then(f => console.log('wrote', f));
