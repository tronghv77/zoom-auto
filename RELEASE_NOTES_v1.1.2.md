# Zoom Auto Scheduler v1.1.2

## Hotfix updater

- Sửa dứt điểm lỗi còn mở/kẹt cửa sổ `cmd` khi tự cập nhật.
- Đổi cơ chế áp dụng cập nhật:
  - Nếu file tải về là installer `.exe`, ứng dụng chạy trực tiếp installer để cập nhật.
  - Không còn phụ thuộc batch/copy cho luồng cập nhật installer.
- Giữ fallback batch cho payload không phải installer để tương thích.

## Build/Release

- Kế thừa các cải tiến pipeline đóng gói từ v1.1.1 (đảm bảo đóng gói đủ dependency).
