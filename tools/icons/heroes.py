"""Original, manually composed SVG geometry. No raster tracing."""
from xml.sax.saxutils import escape

def p(d): return f'<path d="{d}"/>'
def c(x,y,r): return f'<circle cx="{x}" cy="{y}" r="{r}"/>'
def r(x,y,w,h,rx=0): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'
def gold(x,y,rad=9): return f'<circle cx="{x}" cy="{y}" r="{rad}" fill="#FFCD00" stroke="none"/>'
def tile(x,y,w=12,h=12): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="#FFCD00" stroke="none"/>'

# nn, slug, Vietnamese name, English name, line geometry, one background accent
HEROES = [
('01','legislative-input','Góp ý xây dựng pháp luật','Legislative Input',
 p('M33 54H12a3 3 0 0 1-3-3V12a3 3 0 0 1 3-3h24a3 3 0 0 1 3 3v14M17 19h14M17 27h11M17 35h7')+p('m29 49 3-10 17-17a4.24 4.24 0 0 1 6 6L38 45l-9 4M45 26l6 6M32 39l6 6'),tile(43,43)),
('02','local-economic-governance','Điều hành kinh tế địa phương','Local Economic Governance',
 r(25,9,14,17,2)+p('M30 15h4M30 20h4M32 26v9M13 35h38M13 35v7M32 35v7M51 35v7')+r(7,42,12,12,1)+r(26,42,12,12,1)+r(45,42,12,12,1)+p('M13 48v6M32 48v6M51 48v6'),gold(43,15,8)),
('03','business-environment-reform','Cải thiện môi trường kinh doanh','Business Environment Reform',
 p('M9 55V17h12M9 26h7M9 35h7M43 17h12v38M48 26h7M48 35h7M22 55V37h20v18M28 37v-5h8v5M22 44h20M29 18l4 4 10-11'),tile(24,8,13,13)),
('04','administrative-reform','Cải cách thủ tục hành chính','Administrative Reform',
 p('M10 43H7V12h18v4')+r(12,18,18,31,2)+p('M17 25h8M17 32h8M17 39h5M35 33h8m-4-4 4 4-4 4')+r(47,22,10,23,2)+p('m49 32 2 2 4-5'),tile(44,12,14,14)),
('05','international-integration','Hội nhập quốc tế','International Integration',
 c(30,32,21)+p('M9 32h42M13 20h34M13 44h34M30 11c-13 12-13 30 0 42M30 11c13 12 13 30 0 42M51 10h6v6M57 10l-9 9'),gold(49,48,8)),
('06','public-private-dialogue','Đối thoại công–tư','Public-Private Dialogue',
 c(13,28,5)+c(51,28,5)+p('M8 54V41a4 4 0 0 1 8 0v6h7v7M56 54V41a4 4 0 0 0-8 0v6h-7v7M23 39h18M32 39v16M23 11h18v13h-9l-6 5v-5h-3z')+p('M28 17h8'),tile(26,8,13,13)),
('07','certificate-of-origin','Chứng nhận xuất xứ','Certificate of Origin',
 p('M27 55H11V9h25l9 9v12M36 9v10h9M17 25h17M17 33h10M17 41h7')+p('m31 39 13-6 13 6v14l-13 6-13-6zM31 39l13 6 13-6M44 45v14M38 36l13 6'),tile(43,45,10,10)),
('08','sme','Doanh nghiệp nhỏ và vừa','Small and Medium Enterprises',
 p('M8 55V35h20v20M6 35l4-10h16l4 10M14 55V44h8v11M36 55V16h19v39M42 24h2M49 24h1M42 32h2M49 32h1M42 40h2M49 40h1M43 55v-7h5v7'),gold(44,15,9)),
('09','private-sector-development','Phát triển kinh tế tư nhân','Private Sector Development',
 p('M7 55V38h12v17M26 55V29h12v26M45 55V20h12v35M12 45h2M12 50h2M31 36h2M31 43h2M50 28h2M50 35h2M11 28l18-10 17-8M38 9l8 1-3 8'),gold(26,12,7)),
('10','enterprise-productivity','Năng suất doanh nghiệp','Enterprise Productivity',
 p('M8 54V37h8v17M22 54V27h8v27M36 24V14h8v10M7 54h23')+p('m41 29 6 0 1 5 5 2 4-2 3 5-4 3v5l4 3-3 5-4-2-5 2-1 5h-6l-1-5-5-2-4 2-3-5 4-3v-5l-4-3 3-5 4 2 5-2z')+c(44,43,5),gold(18,19,8)),
('11','enterprise-green-transition','Chuyển đổi xanh doanh nghiệp','Enterprise Green Transition',
 p('M8 55V18h24v16M15 26h3M24 26h2M15 34h3M15 42h3M8 55h20M24 55V45')+p('M34 50C22 36 39 27 56 26c0 20-8 30-19 28M31 57l17-20'),gold(42,17,9)),
('12','enterprise-digital-transition','Chuyển đổi số doanh nghiệp','Enterprise Digital Transition',
 p('M8 55V15h22v40M8 55h27M15 24h2M23 24h1M15 33h2M23 33h1M16 55V43h7v12M36 25h7l6-7M36 35h14M36 45h7l6 7')+c(52,15,4)+c(54,35,4)+c(52,55,4),gold(39,13,8)),
('13','membership','Hội viên','Membership',
 c(32,15,6)+c(13,21,4)+c(51,21,4)+p('M22 34v-3a10 10 0 0 1 20 0v3M6 43v-8a7 7 0 0 1 12-5M58 43v-8a7 7 0 0 0-12-5')+r(17,37,30,19,2)+c(25,44,2)+p('M21 51a4 4 0 0 1 8 0M34 44h7M34 50h5'),tile(31,39,13,13)),
('14','trade-promotion','Xúc tiến thương mại','Trade Promotion',
 p('m8 32 14-6 14 6v18l-14 6-14-6zM8 32l14 6 14-6M22 38v18M15 29l14 6M30 16h24m-6-6 6 6-6 6M54 38H42m6-6-6 6 6 6'),gold(18,14,8)),
('15','trade-fair','Hội chợ, triển lãm','Trade Fair',
 r(8,10,48,10,1)+p('M12 20v35M52 20v35M7 55h50M20 55V43h24v12M18 43h28')+c(32,30,5)+p('M24 43v-1a8 8 0 0 1 16 0v1'),tile(22,11,20,8)),
('16','investment','Thu hút đầu tư','Investment',
 p('M8 55V34h17v21M33 55V26h21v29M14 42h4M14 49h4M40 34h3M47 34h1M40 42h3M47 42h1M41 55v-6h6v6M10 10c16 0 22 5 25 13M27 20l8 3 2-8'),gold(47,15,9)),
('17','arbitration','Trọng tài thương mại','Commercial Arbitration',
 p('M30 19v36M21 55h18M10 26h40M15 26 7 43h16zM45 26l-8 17h16zM7 43c1 7 15 7 16 0M37 43c1 7 15 7 16 0M35 8h21v12H45l-6 5v-5h-4zM40 14h10'),tile(39,9,13,10)),
('18','training','Đào tạo, nâng cao năng lực','Training',
 p('M32 27c-7-7-16-9-25-8v31c9-1 18 1 25 7 7-6 16-8 25-7V19c-9-1-18 1-25 8v30M14 29c4 0 8 1 11 3M14 37c4 0 8 1 11 3M39 32c3-2 7-3 11-3M39 40c3-2 7-3 11-3')+c(32,13,5),gold(32,13,7)),
('19','export-logistics','Xuất khẩu và logistics','Export and Logistics',
 p('M8 38h48l-7 13H15zM13 38V25h12v13M17 25V17h5v8M29 38V27h10v11M39 38V27h11v11M7 56q6-5 12 0t12 0 12 0 12 0'),gold(47,18,9)),
('20','forum-events','Diễn đàn, sự kiện','Forums and Events',
 c(32,13,5)+p('M23 30v-4a9 9 0 0 1 18 0v4M21 30h22M25 30v8M39 30v8')+c(12,44,4)+c(32,44,4)+c(52,44,4)+p('M6 57v-3a6 6 0 0 1 12 0v3M26 57v-3a6 6 0 0 1 12 0v3M46 57v-3a6 6 0 0 1 12 0v3'),gold(39,15,8)),
('21','research-index','Nghiên cứu, khảo sát','Research and Surveys',
 p('M26 55H9V9h34v18M16 18h16M16 25h9M16 44V36M23 44V31M30 34v-9')+c(41,41,10)+p('m48 48 9 9'),gold(43,40,7)),
('22','employers-labour','Quan hệ lao động','Labour Relations',
 c(15,22,6)+p('M7 55V39a8 8 0 0 1 16 0v3M11 34l4 7 4-7M57 55V39a8 8 0 0 0-16 0v3M43 23a6 6 0 0 0 12 0M42 21v-3a7 7 0 0 1 14 0v3M40 21h18M49 10v8M19 43l9 7a6 6 0 0 0 8 0l9-7M27 40l5 4 5-4'),gold(32,20,8)),
('23','networking-partnership','Kết nối, đối tác','Networking and Partnerships',
 c(12,20,6)+c(52,20,6)+p('M6 55V38a8 8 0 0 1 14-5M58 55V38a8 8 0 0 0-14-5M28 43l-3 3a6 6 0 0 1-8-8l6-6a6 6 0 0 1 8 0M36 35l3-3a6 6 0 0 1 8 8l-6 6a6 6 0 0 1-8 0M25 40l14-8'),gold(32,15,8)),
('24','business-advisory','Tư vấn doanh nghiệp','Business Advisory',
 r(7,31,36,24,2)+p('M17 31v-7h15v7M7 41h14M29 41h14M21 40h8v6h-8zM37 9h20v17H46l-7 6v-6h-2zM42 16h10M42 21h6'),tile(40,10,14,14)),
]
