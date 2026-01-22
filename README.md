# 🎯 Zoom Auto Scheduler

Ứng dụng Windows để tự động mở phòng Zoom vào thời gian hẹn trước.

## 🌟 Tính Năng

- ✅ **Hẹn giờ tự động** - Mở Zoom vào đúng giờ phút
- ✅ **Giao diện đẹp** - Dễ sử dụng, không cần nhập dòng lệnh
- ✅ **Lưu lịch** - Các lịch được lưu tự động và tải lại khi khởi động
- ✅ **Chạy nền** - Ứng dụng chạy ở background
- ✅ **Quản lý dễ dàng** - Thêm, xóa, sửa lịch một cách nhanh chóng

## 📋 Yêu Cầu

- Windows 7 trở lên
- Python 3.8+
- Cài đặt Zoom trên máy

## 🚀 Cài Đặt & Chạy

### 1. Clone/Download Project
```bash
cd d:\Projects\zoom-auto
```

### 2. Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy Ứng Dụng
```bash
python main.py
```

## 🔄 Cập Nhật Ứng Dụng (GitHub Releases)

- Ứng dụng hỗ trợ tự cập nhật khi phát hành bản mới trên GitHub Releases.
- Cấu hình trong file `update_config.json`:

```json
{
	"provider": "github",
	"repo": "owner/repo",
	"asset_regex": "^ZoomAuto.*\\.exe$",
	"require_sha256": true,
	"check_on_startup": true,
	"check_interval_hours": 24
}
```

### Quy trình phát hành (maintainer)

1. Tăng phiên bản trong `version.py` (ví dụ: `__version__ = "0.2.0"`).
2. Build exe với PyInstaller, đặt tên file theo `asset_regex` (ví dụ `ZoomAuto-0.2.0.exe`).
3. Tính SHA256 và tạo file checksum:

```powershell
Get-FileHash .\dist\ZoomAuto-0.2.0.exe -Algorithm SHA256 | Select-Object -ExpandProperty Hash | Out-File .\dist\ZoomAuto-0.2.0.exe.sha256 -NoNewline
```

4. Tạo GitHub Release:
	 - Tag: `v0.2.0` (khuyến nghị dạng `vX.Y.Z`).
	 - Đính kèm 2 assets: `.exe` và `.exe.sha256`.
	 - (Tùy chọn) Ghi SHA256 vào phần mô tả: `SHA256: <HASH>`.

5. Cập nhật `update_config.json` trên máy người dùng với `repo: "<owner>/<repo>"`.

Ứng dụng sẽ:
- Kiểm tra nền khi khởi động (tần suất theo `check_interval_hours`).
- Cho phép kiểm tra thủ công tại menu Trợ giúp → “Kiểm tra cập nhật…”.
- Tải bản mới, xác minh SHA256, áp dụng thay thế an toàn và khởi động lại.

## 📖 Hướng Dẫn Sử Dụng

### Thêm Lịch Mới

1. Nhấn nút **"➕ Thêm lịch"**
2. Nhập **Meeting ID** của phòng Zoom
3. (Tùy chọn) Nhập **Mật khẩu** nếu có
4. Chọn **Giờ** và **Phút** bạn muốn mở Zoom
5. Nhấn **"Lưu"**

### Xóa Lịch

- Chọn lịch trong bảng và nhấn **"🗑️"** để xóa

### Làm Mới

- Nhấn **"🔄 Làm mới"** để cập nhật bảng

## 📝 Ví Dụ

**Meeting ID:** `123456789`
**Mật khẩu:** `123456` (nếu cần)
**Giờ:** `14` (2:00 PM)
**Phút:** `30`

→ Zoom sẽ tự động mở lúc **14:30** mỗi ngày

## 💾 Lưu Trữ Dữ Liệu

Các lịch được lưu trong file `zoom_schedule.json` tại cùng thư mục với `main.py`.

## 🔧 Troubleshooting

### Zoom không mở được
- Kiểm tra xem Zoom đã được cài đặt chưa
- Thử nhập Meeting ID mà không có mật khẩu

### Ứng dụng không khởi động
- Kiểm tra xem đã cài đặt tất cả dependencies: `pip install -r requirements.txt`

## 📱 Tạo Shortcut (Tùy Chọn)

Để chạy ứng dụng dễ dàng hơn, bạn có thể tạo batch file:

**Tạo file `run.bat`:**
```batch
@echo off
D:\Projects\zoom-auto\.venv\Scripts\python.exe D:\Projects\zoom-auto\main.py
pause
```

Rồi double-click `run.bat` để chạy ứng dụng.

## 📄 License

Sử dụng tự do

---

**Chúc bạn sử dụng vui vẻ! 🎉**
