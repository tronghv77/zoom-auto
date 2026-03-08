# Zoom Auto Scheduler v1.1.1

## Hotfix

- Fix lỗi cài mới bị crash với thông báo `No module named 'PyQt6'`.
- Cập nhật quy trình build để luôn dùng `.venv`, tự kiểm tra/cài dependency trước khi đóng gói và fail sớm nếu thiếu module quan trọng.
- Fix luồng auto-update bị mở cửa sổ `cmd` treo:
  - chạy batch ở chế độ ẩn
  - thêm timeout vòng chờ tiến trình
  - dọn file tạm an toàn hơn

## Ghi chú

- Khuyến nghị người dùng tải lại installer `v1.1.1` để tránh lỗi từ bản cài cũ.
