# Huong Dan Doc Log Tren Sentry (Zoom Auto)

Tai lieu nay dung de ban theo doi, phan tich va ra quyet dinh xu ly loi tu nguoi dung.

## 1) Tong Quan

- Ung dung gui log loi len Sentry neu co cau hinh bien moi truong `ZOOMAUTO_SENTRY_DSN`.
- Loi duoc gui tu:
  - Loi join Zoom that bai (retry/fallback het cach).
  - Loi unhandled toan cuc (global excepthook).
- User khong xem duoc log neu khong co quyen vao project Sentry.

## 2) Cac Du Lieu Ban Se Thay Trong Event

Khi loi join xay ra, event thuong co:

- `error_code` (nam trong message), vi du:
  - `APP_NOT_INSTALLED`
  - `INVALID_MEETING_ID`
  - `BROWSER_OPEN_FAILED`
  - `INVALID_URL`
  - `RAW_OPEN_FAILED`
  - `INVALID_MODE`
  - `UNKNOWN_ERROR`
- `job_id`
- `attempts`
- `mode_priority` (thu tu fallback)
- `has_zoom_link`

Loi toan cuc co them context:
- `where = global_excepthook`

## 3) Quy Trinh Doc Log Hang Ngay

1. Vao Sentry -> Chon project `zoom-auto-desktop` (hoac ten ban dat).
2. Vao `Issues`:
   - Sap xep theo `Last seen` de uu tien loi moi.
   - Loc khoang thoi gian: `24h` hoac `7d`.
3. Mo tung issue va doc:
   - Tieu de loi + stack trace.
   - So luong su kien (`Events`) va so user/may bi anh huong.
   - Tags/extras: `job_id`, `attempts`, `mode_priority`.
4. Phan loai:
   - Loi he thong (crash/unhandled).
   - Loi nghiep vu join Zoom (profile/fallback/retry).
5. Ghi ket luan vao note theo mau (muc 8).

## 4) Cac Bo Loc Tim Nhanh (Search)

Trong o tim kiem cua Sentry, dung cac tu khoa:

- Theo ma loi:
  - `JoinZoomFailed`
  - `APP_NOT_INSTALLED`
  - `INVALID_MEETING_ID`
- Theo version:
  - `release:zoom-auto@1.0.1`
- Theo moi truong:
  - `environment:production`

Goi y:
- Neu can tim loi moi phat sinh sau release: loc theo `release` + `firstSeen`.

## 5) Cach Uu Tien Xu Ly

Uu tien theo thu tu:

1. Anh huong rong:
   - Loi xay ra tren nhieu may/user.
2. Muc do nghiem trong:
   - Crash app > khong join duoc > loi hien thi nhe.
3. Tan suat:
   - Loi lap lai lien tuc trong thoi gian ngan.
4. Regression:
   - Loi moi sau khi len version moi.

## 6) Mapping Nhanh: Loi -> Huong Xu Ly

- `APP_NOT_INSTALLED`:
  - Zoom App khong mo duoc.
  - Xu ly: uu tien fallback Browser, hien huong dan cai Zoom app.

- `INVALID_MEETING_ID`:
  - Du lieu lich thieu/sai ID.
  - Xu ly: tang validate form, kiem tra du lieu cu khi load.

- `BROWSER_OPEN_FAILED`:
  - Trinh duyet khong mo URL.
  - Xu ly: fallback App/raw, kiem tra default browser.

- `INVALID_URL` / `RAW_OPEN_FAILED`:
  - Link Zoom raw sai dinh dang hoac khong mo duoc.
  - Xu ly: validate link khi luu lich, parser an toan hon.

- `UNKNOWN_ERROR`:
  - Chua map duoc.
  - Xu ly: doc stack trace chi tiet va bo sung taxonomy.

## 7) Alert Nen Bat Tren Sentry

Nen tao alert cho:

1. Issue moi thuoc nhom `JoinZoomFailed`.
2. Spike event (tang dot bien trong 1h/24h).
3. Crash/unhandled moi trong production.

Kenh nhan alert:
- Email (de bat dau nhanh).
- Slack/Telegram (neu doi van hanh can phan hoi nhanh).

## 8) Mau Note Moi Ngay (Copy/Paste)

Ngay:
- YYYY-MM-DD

Tong quan:
- So issue moi:
- So issue duoc resolve:
- Top 3 loi:

Chi tiet:
1. [Ten issue]
- Error code:
- Release:
- So event:
- So user/may:
- Anh huong:
- Nguyen nhan du kien:
- Huong fix:
- Muc uu tien: P1/P2/P3

Hanh dong:
- Ticket tao:
- Owner:
- ETA:

## 9) Privacy Va Bao Mat

- Khong dua API token quan tri vao app.
- Neu can dung API, tao token rieng scope toi thieu.
- Khong gui password/meeting id day du len log.
- Chi cho team noi bo co quyen xem Sentry project.

## 10) Checklist Trien Khai Dung

- [ ] Da set `ZOOMAUTO_SENTRY_DSN` tren moi truong build/chay app.
- [ ] Da tao project Sentry dung cho Zoom Auto.
- [ ] Da bat alert co ban (issue moi + spike).
- [ ] Da thong nhat quy trinh triage (hang ngay/2 ngay).
- [ ] Da co mau note va nguoi chiu trach nhiem doc log.

