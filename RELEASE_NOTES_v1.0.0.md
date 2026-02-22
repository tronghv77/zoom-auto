## 🎉 Zoom Auto Scheduler v1.0.0

### 🚀 Major Release - First Stable Version

Đây là phiên bản ổn định đầu tiên của Zoom Auto Scheduler với nhiều tính năng mới và cải tiến quan trọng.

### ✨ New Features

#### 💻 Chế độ mở Zoom linh hoạt
- ✅ **Mở bằng Trình duyệt** (mặc định): Mở link HTTPS qua trình duyệt web
- ✅ **Mở bằng App Zoom Desktop**: Mở trực tiếp ứng dụng Zoom với protocol `zoommtg://`
- ✅ Cài đặt được lưu tự động cho lần sau
- ✅ Truy cập: Menu → 💻 Cách mở Zoom

#### 📅 Cải tiến quản lý lịch
- ✅ Highlight vàng ▶ cho lịch sắp chạy tiếp theo
- ✅ Đếm ngược thời gian trên thanh trạng thái
- ✅ Tự động xóa lịch "once" không hợp lệ
- ✅ Thu nhỏ vào khay hệ thống khi đóng cửa sổ

### 🔧 Technical Improvements
- Thêm `SETTINGS_FILE` để lưu cài đặt người dùng
- Cải thiện xử lý lỗi cho lịch "once" không hợp lệ
- Parse Meeting ID và Password từ Zoom link khi mở bằng App
- Fallback sang browser nếu không mở được App Zoom

### 📦 Installation
Chạy `ZoomAuto-Setup-1.0.0.exe` và làm theo hướng dẫn.

### 🗂️ Data Location
- User data: `%LOCALAPPDATA%\ZoomAuto\zoom_schedule.json`
- Settings: `%LOCALAPPDATA%\ZoomAuto\settings.json`
- Installation: `%LOCALAPPDATA%\Programs\ZoomAuto`

### 🛠️ Uninstall
Sử dụng Windows Settings → Apps hoặc uninstaller trong Start Menu.

### 📊 Release Info
- Build date: February 22, 2026
- Previous version: 0.1.3
- Changelog: See features above

---

### ⬆️ Upgrade từ v0.1.3
- Lịch đã tạo trước đó vẫn được giữ nguyên
- Cài đặt mới sẽ được tạo tự động

**Sẵn sàng cho production! ✅**
