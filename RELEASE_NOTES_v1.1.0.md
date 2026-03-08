# Zoom Auto Scheduler v1.1.0

## Tính năng mới

- Nâng cấp Join Zoom theo từng lịch với `Profile Join`:
  - App -> Browser -> Link raw
  - Browser -> App -> Link raw
  - Chỉ App / Chỉ Browser / Chỉ Link raw
- Hỗ trợ retry có giới hạn theo từng lịch:
  - Số lần thử lại
  - Thời gian trễ giữa các lần thử
- Hỗ trợ fallback mode tự động khi mode hiện tại thất bại.

## Cải tiến vận hành

- Nút `Vào Ngay` dùng cùng policy retry/fallback như scheduler.
- Ghi trạng thái chạy gần nhất của từng lịch:
  - Thành công/thất bại
  - Mode đã dùng
  - Số lần attempt
  - Mã lỗi/lý do lỗi
- Hiển thị thông tin join profile + lần chạy gần nhất trong panel chi tiết.

## Logging lỗi

- Tích hợp gửi lỗi tự động lên Sentry (`sentry-sdk`).
- Hỗ trợ đọc DSN từ:
  - Biến môi trường `ZOOMAUTO_SENTRY_DSN`
  - `settings.json` key `sentry_dsn`
- Bắt lỗi unhandled toàn cục qua `sys.excepthook`.

## Tương thích dữ liệu

- Tương thích với dữ liệu lịch cũ.
- Nếu lịch cũ chưa có `join_profile/retry_policy`, hệ thống tự dùng giá trị mặc định an toàn.
