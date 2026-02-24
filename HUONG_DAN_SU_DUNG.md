# HƯỚNG DẪN SỬ DỤNG ZOOM AUTO SCHEDULER

Zoom Auto Scheduler là ứng dụng giúp bạn tự động vào các phòng học/họp Zoom theo lịch đã hẹn trước, giúp bạn không bao giờ bị muộn giờ.

## 🚀 Bắt đầu nhanh

### 1. Thêm lịch mới
1. Nhấn nút **"➕ Thêm lịch"** ở góc trên bên phải.
2. Nhập **Tên phòng Zoom** (ví dụ: "Họp team buổi sáng").
3. Nhập **Link Zoom** (khuyên dùng) hoặc **Meeting ID** và **Mật khẩu**.
4. Chọn **Giờ** và **Phút** muốn tự động vào phòng.
5. Chọn chế độ **Lặp lại** (Không lặp, Hàng ngày, Hàng tuần, hoặc Tùy chỉnh).
6. Nhấn **"Lưu"**.

### 2. Bật lịch hẹn
- Đảm bảo nút gạt ở cột **Bật/Tắt** đang ở trạng thái BẬT (màu xanh).
- Bạn có thể tắt tạm thời lịch hẹn mà không cần xóa nó.

### 3. Để phần mềm chạy ngầm
- Giữ phần mềm **luôn mở** (có thể thu nhỏ xuống thanh taskbar).
- Khi đến giờ, phần mềm sẽ tự động mở Zoom trong trình duyệt mặc định của bạn.

---

## 📅 Quản lý lịch hẹn

### Các chức năng chính
- **Bật/Tắt lịch:** Sử dụng nút gạt để kích hoạt hoặc vô hiệu hóa lịch.
- **Sửa lịch:** Chọn lịch và nhấn nút **"✏️ Sửa"** để thay đổi thông tin.
- **Nhân bản:** Chọn lịch và nhấn nút **"📋 Nhân bản"** để tạo bản sao.
- **Xóa lịch:** Chọn lịch và nhấn nút **"🗑️ Xóa"** để xóa vĩnh viễn.
- **Test Zoom:** Nhấn nút **Test** để kiểm tra xem Link/ID có hoạt động không.

### Các chế độ lặp lại
- **Không lặp lại:** Chỉ chạy một lần duy nhất vào ngày giờ cụ thể.
- **Hàng ngày:** Chạy mỗi ngày vào giờ đã hẹn.
- **Hàng tuần:** Chạy vào thứ trong tuần mà bạn tạo lịch.
- **Mọi ngày trong tuần:** Chạy từ thứ 2 đến thứ 6.
- **Tùy chỉnh:** Cho phép thiết lập lặp lại mỗi X ngày/tuần/tháng/năm.

---

## ⚙️ Cài đặt Zoom để tự động hoàn toàn

Để phần mềm có thể đưa bạn vào thẳng phòng họp mà không cần thao tác thêm:

1. **Đăng nhập Zoom trên trình duyệt:**
   - Mở trình duyệt web mặc định (Chrome, Edge, Firefox...).
   - Truy cập [zoom.us](https://zoom.us) và đăng nhập tài khoản của bạn.

2. **Cấu hình (Nếu bạn là chủ phòng):**
   - Vào **Settings (Cài đặt)** > **Security (Bảo mật)**.
   - **TẮT** tính năng **"Waiting Room" (Phòng chờ)**.
   - Hoặc **BẬT** tính năng **"Allow participants to join before host"**.

**Lưu ý:** Việc tắt phòng chờ giúp vào nhanh nhưng cần cân nhắc về bảo mật.

---

## ❓ Câu hỏi thường gặp (FAQ)

**Q: Tôi có thể tắt phần mềm sau khi đặt lịch không?**
A: Không. Bạn cần giữ phần mềm chạy (có thể thu nhỏ cửa sổ) để nó có thể kích hoạt lịch đúng giờ.

**Q: Máy tính đang Sleep (Ngủ) thì phần mềm có chạy không?**
A: Không. Máy tính cần phải đang hoạt động vào thời điểm hẹn giờ. Hãy tắt chế độ Sleep nếu cần thiết.

**Q: Tại sao nên dùng Link Zoom thay vì Meeting ID?**
A: Link Zoom thường chứa cả mật khẩu mã hóa, giúp đăng nhập nhanh hơn và chính xác hơn.

**Q: Dữ liệu lịch được lưu ở đâu?**
A: Dữ liệu được lưu trong file `zoom_schedule.json` tại thư mục cài đặt phần mềm.

---

## 📞 Hỗ trợ

Nếu gặp lỗi hoặc cần trợ giúp, vui lòng liên hệ nhà phát triển (thông tin trong phần Giới thiệu của ứng dụng).
