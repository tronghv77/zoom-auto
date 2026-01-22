import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Số phút sau hiện tại để tạo lịch test (mặc định 5 phút)
minutes = 5
if len(sys.argv) > 1:
    try:
        minutes = int(sys.argv[1])
    except:
        pass

now = datetime.now()
test_time = now + timedelta(minutes=minutes)

schedule = [
    {
        'hour': test_time.hour,
        'minute': test_time.minute,
        'meeting_id': '123456789',
        'password': '',
        'enabled': True
    }
]

schedule_file = Path(__file__).parent / 'zoom_schedule.json'

# Ghi file JSON mà không có BOM
with open(schedule_file, 'w', encoding='utf-8') as f:
    json.dump(schedule, f, indent=2)

print(f"✓ Lịch test tạo thành công!")
print(f"  Sẽ mở Zoom lúc: {test_time.hour:02d}:{test_time.minute:02d}")
print(f"  Meeting ID: 123456789")
