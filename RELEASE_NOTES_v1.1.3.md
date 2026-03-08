# Release Notes - v1.1.3

## Sửa lỗi

### Tự động cập nhật (Auto-update)

- **Bỏ cửa sổ CMD đen xuất hiện khi cập nhật** — Dùng `SW_HIDE` + `CREATE_NO_WINDOW` + `STARTUPINFO` để ẩn hoàn toàn mọi cửa sổ console khi chạy installer hoặc batch script.
- **Installer Inno Setup chạy ngầm** — Thêm flag `/VERYSILENT` để cài đặt hoàn toàn im lặng, không hiện wizard hay hộp thoại.
- **Batch script không còn tạo CMD mới để tự xóa** — Thay `start "" cmd /c del "%~f0"` bằng `(goto) 2>nul & del /q "%~f0"` (xóa ngay trong batch hiện tại).
- **Sửa batch treo khi dùng `timeout`** — `timeout` yêu cầu interactive console, thay bằng `ping -n 2 127.0.0.1` hoạt động ổn trên mọi Windows.
- **Sửa kiểm tra PID không chính xác** — Dùng `tasklist /fo csv` kết hợp `find` thay vì `findstr` regex để match PID chính xác hơn.
- **Sửa path có khoảng trắng trong batch** — Quote đầy đủ `%CURR%` và `%NEW%`.
