# Zoom Auto Scheduler v1.0.1

## Sửa lỗi

- Sửa lỗi highlight lịch sắp diễn ra bị sai sau một thời gian chạy.
- Tối ưu cập nhật highlight: chỉ cập nhật các dòng thay đổi, không làm mới toàn bộ bảng.
- Sửa lỗi mất hiển thị dấu tick/checkbox ở cột đầu khi dòng được highlight.
- Sửa lỗi màu chữ không đồng nhất giữa các máy Windows/theme khác nhau.
- Sửa lỗi một số máy không nhìn thấy chữ lịch (chỉ hiện khi bấm chọn).

## An toàn dữ liệu

- Dữ liệu người dùng vẫn được lưu tại `%LOCALAPPDATA%\ZoomAuto\`:
  - `zoom_schedule.json`
  - `settings.json`

Cập nhật từ `v1.0.0` lên `v1.0.1` không xóa các file dữ liệu này.
