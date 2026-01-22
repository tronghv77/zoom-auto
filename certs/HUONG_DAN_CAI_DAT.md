# Hướng dẫn cài đặt ZoomAuto (Nội bộ)

## Tổng quan
ZoomAuto là ứng dụng được ký số bằng chứng thư nội bộ. Để chạy mà không bị cảnh báo "ứng dụng không đáng tin cậy", bạn cần cài đặt chứng thư này vào máy.

---

## Bước 1: Tải chứng thư

Bạn sẽ nhận được:
- File `ZoomAuto-Internal.cer` (chứng thư)
- File `ZoomAuto.exe` hoặc `ZoomAuto-0.1.0.exe` (ứng dụng đã ký)

Lưu file `.cer` vào máy (ví dụ: Desktop hoặc Downloads).

---

## Bước 2: Cài đặt chứng thư vào Trusted Root

**Cách 1: Giao diện đồ họa (dễ nhất)**

1. **Mở Certificate Manager:**
   - Nhấn `Win + R` → gõ `certmgr.msc` → Enter

2. **Import vào Trusted Root:**
   - Bên trái, mở rộng → chọn **Trusted Root Certification Authorities**
   - Click chuột phải trên **Certificates** → chọn **All Tasks** → **Import...**
   - Chọn file `ZoomAuto-Internal.cer`
   - Next → Finish → **Yes** khi được hỏi

3. **Import vào Intermediate (để chắc chắn):**
   - Bên trái, chọn **Intermediate Certification Authorities**
   - Click chuột phải trên **Certificates** → **All Tasks** → **Import...**
   - Chọn file `ZoomAuto-Internal.cer` lần nữa
   - Next → Finish

4. **Kiểm tra:**
   - Quay lại Trusted Root Certificates, tìm "ZoomAuto-Internal" trong danh sách
   - Nếu thấy → cài đặt thành công ✓

---

**Cách 2: Command Line (PowerShell)**

Nếu bạn quen dùng PowerShell (chạy với quyền Admin):

```powershell
# Cài vào Trusted Root
Import-Certificate -FilePath "C:\path\to\ZoomAuto-Internal.cer" -CertStoreLocation Cert:\CurrentUser\Root

# Cài vào Intermediate
Import-Certificate -FilePath "C:\path\to\ZoomAuto-Internal.cer" -CertStoreLocation Cert:\CurrentUser\CA
```

Thay `C:\path\to` bằng đường dẫn thực tế đến file `.cer`.

---

## Bước 3: Chạy ứng dụng

Sau khi cài đặt chứng thư:

1. **Chạy bình thường:**
   - Double-click vào `ZoomAuto.exe` hoặc `ZoomAuto-0.1.0.exe`
   - Ứng dụng sẽ chạy mà không bị cảnh báo "không tin cậy"

2. **Nếu vẫn thấy cảnh báo SmartScreen:**
   - Click **More info**
   - Chọn **Run anyway**
   - Điều này sẽ xảy ra lần đầu, sau đó Windows sẽ nhớ

---

## Kiểm tra chứng thư đã cài

Để xác nhận chứng thư đã được cài đúng:

```powershell
# Kiểm tra ứng dụng có chữ ký
Get-AuthenticodeSignature "C:\path\to\ZoomAuto.exe"

# Nếu Status = "Valid" hoặc "UnknownError" nhưng SignerCertificate hiện "ZoomAuto-Internal" 
# → chứng thư đã được nhận diện
```

---

## Gỡ cài đặt (nếu cần)

Nếu muốn xóa chứng thư:

1. Mở `certmgr.msc`
2. Vào **Trusted Root Certification Authorities** → **Certificates**
3. Tìm "ZoomAuto-Internal", click chuột phải → **Delete**
4. Lặp lại ở **Intermediate Certification Authorities**

---

## Liên hệ hỗ trợ

Nếu gặp lỗi:
- Kiểm tra lại bạn đã import chứng thư vào đúng 2 nơi (Trusted Root + Intermediate)?
- Restart máy sau khi import?
- Chạy PowerShell với quyền Admin?

Liên hệ nhà phát triển nếu vẫn có vấn đề.

---

**Cập nhật:** 22/01/2026
