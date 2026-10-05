# Nhật ký quyết định thiết kế

Các quyết định đã được chủ dự án xác nhận trong quá trình xây dựng bộ nhận diện (tháng 10/2026). Khi sửa hệ thống, hãy kiểm tra các quyết định này trước.

## Logo

| Quyết định | Lý do |
|---|---|
| Logo gốc là file CorelDRAW `source/logo/Logo_VCCI.cdr`. Hình dáng, tỉ lệ và màu lấy từ file này. | File PNG cũ bị kéo giãn khoảng 2,4%; trống đồng ở bản PNG bị phóng to và mất vòng ngăn với chữ C. |
| Chỉ một phiên bản màu: chữ VCCI Blue, trống đồng màu gốc, trên nền sáng. | Giữ nhận diện nhất quán. |
| Không dùng logo chữ trắng. | Trong văn hóa Việt Nam, kiểu thể hiện này bị kiêng kị. |
| Không dùng logo chữ vàng, không dùng trống đồng đứng riêng thay logo. | Chủ dự án đã xem thử các phương án này và không chấp nhận. |
| Trên nền xanh, nền tối hoặc ảnh: logo đặt trên ô nền sáng (Paper #FBF9F4), lề trong bằng x. | Là phương án duy nhất được chấp nhận cho nền tối. |
| Phiên bản logo màu đỏ (`source/logo/Logo_VCCI_red.jpg`) không đưa vào hệ thống. | Chủ dự án quyết định. |

## Màu và chữ

| Quyết định | Lý do |
|---|---|
| Màu chính VCCI Blue CMYK 100/80/0/0 (#264896); vàng C0 M20 Y100 K0; nâu đồng C0 M60 Y80 K20. | Theo file .CDR gốc. Màu navy #112873 của bản PNG cũ bị thay thế. |
| Không ghi mã Pantone. | File gốc không có; nhà in sẽ đề xuất từ CMYK. |
| Bronze Ink #9C570C cho chữ nhãn cỡ nhỏ. | Nâu đồng của logo chỉ đạt độ tương phản 3,3:1 trên nền sáng. |
| Lora (tiêu đề) và Be Vietnam Pro (nội dung). | Cả hai miễn phí (OFL) và hỗ trợ đầy đủ tiếng Việt. |

## Văn bản và template

| Quyết định | Lý do |
|---|---|
| Không áp dụng Nghị định 30/2020/NĐ-CP cho thiết kế. | VCCI muốn ấn phẩm sáng tạo và tự do hơn văn bản của cơ quan Nhà nước. |
| Template Word: letterhead, báo cáo, thư mời; kiểu bảng VCCI Table / Light / Tint; font được nhúng. | Đây là các loại văn bản dùng nhiều nhất. |
| PowerPoint: 16:9, một file có cả layout sáng và tối, 18 layout, phụ đề tiếng Anh ở bìa và slide chuyển chương, logo chỉ ở bìa và slide kết thúc (cùng góc slide nền sáng), hero icon ở slide chuyển chương, biểu đồ thật, chỗ trống cho ảnh, hiệu ứng Fade chỉ ở slide chuyển chương. | Kết quả phỏng vấn yêu cầu (2 vòng, 12 câu hỏi). |

## Icon

| Quyết định | Lý do |
|---|---|
| Không sao chép bộ icon của ANU; chỉ tham khảo cách tổ chức hai cấp. | Quyền sở hữu và tính nhận diện riêng. |
| Bộ icon v1 do agent ChatGPT thực hiện theo [hồ sơ bàn giao](handoff-icons/): 48 icon UI dựa trên Lucide, 24 hero icon riêng, phong cách "Geometric Clarity" (hướng A). | Chủ dự án duyệt ngày 05/10/2026. Hero tăng từ 20 lên 24 chủ đề. |
