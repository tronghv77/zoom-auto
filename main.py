import sys
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QTimeEdit, QSpinBox, QMessageBox, QDialog, QFormLayout, QCheckBox,
    QHeaderView, QDateTimeEdit, QRadioButton, QButtonGroup, QDateEdit,
    QComboBox, QDialogButtonBox, QSpinBox, QCheckBox, QGroupBox, QScrollArea,
    QTabWidget, QTextBrowser, QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import QTime, Qt, QThread, pyqtSignal, QDateTime, QDate

# Mapping thứ trong tuần
WEEKDAYS_MAP = {
    0: "T2", 1: "T3", 2: "T4", 3: "T5", 4: "T6", 5: "T7", 6: "CN"
}

def format_meeting_id(id_str):
    """Định dạng Meeting ID từ '83738062598' thành '837 3806 2598'."""
    if not id_str or not id_str.isdigit():
        return id_str
    
    # Định dạng cho ID 11 số theo chuẩn mới
    if len(id_str) == 11:
        return f"{id_str[0:3]} {id_str[3:7]} {id_str[7:11]}"
    
    # Trả về nguyên bản nếu không phải 11 số (có thể là ID cũ hơn)
    return id_str

class CustomRecurrenceDialog(QDialog):
    """Dialog tùy chỉnh lặp lại"""
    def __init__(self, parent=None, current_date=None):
        super().__init__(parent)
        self.setWindowTitle("Lặp lại tùy chỉnh")
        self.resize(520, 560)
        
        # Modern styling - Cyan/Blue theme for better visibility
        self.setStyleSheet("""
            QDialog {
                background: white;
            }
            
            QWidget#headerWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #06b6d4,
                    stop:1 #0891b2
                );
                border-radius: 0px;
            }
            
            QLabel#headerTitle {
                font-size: 20px;
                font-weight: bold;
                color: white;
                background: transparent;
            }
            
            QLabel#headerSubtitle {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.95);
                background: transparent;
            }
            
            QLabel {
                color: #0f172a;
                font-size: 13px;
                font-weight: 600;
            }
            
            QSpinBox, QComboBox, QDateEdit {
                padding: 10px 12px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                background: #f9fafb;
                font-size: 13px;
                color: #0f172a;
            }
            
            QSpinBox:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #06b6d4;
                background: white;
            }
            
            QSpinBox { min-width: 70px; }
            QComboBox { min-width: 100px; }
            
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            
            QPushButton#dayBtn {
                border: 2px solid #e5e7eb;
                border-radius: 20px;
                width: 40px;
                height: 40px;
                background-color: white;
                color: #64748b;
                font-weight: 600;
                font-size: 12px;
            }
            
            QPushButton#dayBtn:checked {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #06b6d4,
                    stop:1 #0891b2
                );
                color: #0f172a;
                border: 2px solid #0891b2;
            }
            
            QPushButton#dayBtn:hover:!checked {
                background-color: #f3f4f6;
                border-color: #06b6d4;
            }
            
            QRadioButton {
                spacing: 10px;
                font-size: 13px;
                color: #0f172a;
                font-weight: 500;
            }
            
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #d1d5db;
                border-radius: 9px;
                background-color: white;
            }
            
            QRadioButton::indicator:hover {
                border: 2px solid #06b6d4;
            }
            
            QRadioButton::indicator:checked {
                background-color: #06b6d4;
                border: 2px solid #06b6d4;
                border-radius: 9px;
            }
            
            QRadioButton::indicator:checked::after {
                content: "✓";
                color: white;
            }
            
            QPushButton#cancelBtn {
                background-color: #f3f4f6;
                color: #374151;
                padding: 10px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #d1d5db;
            }
            
            QPushButton#cancelBtn:hover {
                background-color: #e5e7eb;
            }
            
            QPushButton#saveBtn {
                background-color: white;
                color: #06b6d4;
                padding: 10px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #06b6d4;
            }
            
            QPushButton#saveBtn:hover {
                background-color: #f0f9ff;
                border: 2px solid #0891b2;
                color: #0891b2;
            }
        """)
        
        self.current_date = current_date or QDate.currentDate()
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === HEADER ===
        header = QWidget()
        header.setObjectName("headerWidget")
        header.setFixedHeight(80)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)
        header_layout.setSpacing(4)
        
        title = QLabel("🔁 Lặp lại tùy chỉnh")
        title.setObjectName("headerTitle")
        
        subtitle = QLabel("Tạo chu kỳ lặp lại linh hoạt theo nhu cầu")
        subtitle.setObjectName("headerSubtitle")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addStretch()
        
        # === CONTENT ===
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setSpacing(25)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # 1. Lặp lại mỗi...
        layout.addWidget(QLabel("📅 Lặp lại mỗi:"))
        freq_container = QWidget()
        freq_layout = QHBoxLayout(freq_container)
        freq_layout.setContentsMargins(0, 0, 0, 0)
        freq_layout.setSpacing(10)
        
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 99)
        self.interval_spin.setValue(1)
        self.interval_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["ngày", "tuần", "tháng", "năm"])
        self.unit_combo.setCurrentIndex(1) # Default tuần
        self.unit_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        
        freq_layout.addWidget(self.interval_spin)
        freq_layout.addWidget(self.unit_combo)
        freq_layout.addStretch()
        
        layout.addWidget(freq_container)
        
        # 2. Lặp lại vào (chỉ hiện khi chọn tuần)
        self.days_group = QWidget()
        days_layout = QVBoxLayout(self.days_group)
        days_layout.setContentsMargins(0, 5, 0, 5)
        days_layout.setSpacing(12)
        days_layout.addWidget(QLabel("🗓️ Lặp lại vào:"))
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.day_buttons = []
        for i in range(7):
            btn = QPushButton(WEEKDAYS_MAP[i])
            btn.setCheckable(True)
            btn.setObjectName("dayBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            # Default check ngày hiện tại
            if i == self.current_date.dayOfWeek() - 1:
                btn.setChecked(True)
            self.day_buttons.append(btn)
            btn_layout.addWidget(btn)
        
        days_layout.addLayout(btn_layout)
        layout.addWidget(self.days_group)
        
        # 3. Kết thúc
        layout.addWidget(QLabel("⏱️ Kết thúc:"))
        
        end_layout = QVBoxLayout()
        end_layout.setSpacing(15)
        
        self.end_group = QButtonGroup()
        
        # Không bao giờ
        self.radio_never = QRadioButton("Không bao giờ ✓")
        self.radio_never.setChecked(True)
        self.radio_never.setCursor(Qt.CursorShape.PointingHandCursor)
        end_layout.addWidget(self.radio_never)
        self.end_group.addButton(self.radio_never)
        
        # Vào ngày
        date_container = QWidget()
        date_layout = QHBoxLayout(date_container)
        date_layout.setContentsMargins(0, 0, 0, 0)
        date_layout.setSpacing(12)
        
        self.radio_date = QRadioButton("Vào ngày")
        self.radio_date.setCursor(Qt.CursorShape.PointingHandCursor)
        date_layout.addWidget(self.radio_date)
        self.end_group.addButton(self.radio_date)
        
        # Connect to update checkmark
        self.radio_never.toggled.connect(self.update_radio_text)
        self.radio_date.toggled.connect(self.update_radio_text)
        
        self.end_date_edit = QDateEdit(self.current_date.addMonths(1))
        self.end_date_edit.setDisplayFormat("dd/MM/yyyy")
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setEnabled(False)
        self.end_date_edit.setMinimumWidth(160)
        date_layout.addWidget(self.end_date_edit)
        date_layout.addStretch()
        
        end_layout.addWidget(date_container)
        layout.addLayout(end_layout)
        
        layout.addStretch()
        
        # === FOOTER ===
        footer = QWidget()
        footer.setStyleSheet("background-color: white; border-top: 1px solid #e5e7eb;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(25, 15, 25, 15)
        footer_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setFixedWidth(100)
        
        save_btn = QPushButton("✓ Xong")
        save_btn.setObjectName("saveBtn")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.accept)
        save_btn.setFixedWidth(100)
        
        footer_layout.addStretch()
        footer_layout.addWidget(cancel_btn)
        footer_layout.addWidget(save_btn)
        
        # Assemble all
        main_layout.addWidget(header)
        main_layout.addWidget(content, 1)
        main_layout.addWidget(footer)
        
        # Events
        self.unit_combo.currentIndexChanged.connect(self.update_ui)
        self.radio_date.toggled.connect(self.update_ui)
        self.radio_never.toggled.connect(self.update_ui)
        
        self.setLayout(main_layout)
        self.update_ui()
    
    def update_radio_text(self):
        """Update radio button text with checkmark for checked state"""
        if self.radio_never.isChecked():
            self.radio_never.setText("Không bao giờ ✓")
            self.radio_date.setText("Vào ngày")
        else:
            self.radio_never.setText("Không bao giờ")
            self.radio_date.setText("Vào ngày ✓")

    def update_ui(self):
        # Hiện/ẩn chọn thứ trong tuần
        is_week = self.unit_combo.currentText() == "tuần"
        self.days_group.setVisible(is_week)
        
        # Enable date edit
        self.end_date_edit.setEnabled(self.radio_date.isChecked())

    def get_data(self):
        days_of_week = []
        if self.unit_combo.currentText() == "tuần":
            for i, btn in enumerate(self.day_buttons):
                if btn.isChecked():
                    days_of_week.append(i)
        
        end_date = None
        if self.radio_date.isChecked():
            end_date = self.end_date_edit.date().toString(Qt.DateFormat.ISODate)

        return {
            'interval': self.interval_spin.value(),
            'unit': self.unit_combo.currentText(),
            'days_of_week': days_of_week,
            'end_date': end_date
        }
    
    def set_data(self, data):
        if not data: return
        self.interval_spin.setValue(data.get('interval', 1))
        self.unit_combo.setCurrentText(data.get('unit', 'tuần'))
        
        days = data.get('days_of_week', [])
        for i, btn in enumerate(self.day_buttons):
            btn.setChecked(i in days)
            
        end_date = data.get('end_date')
        if end_date:
            self.radio_date.setChecked(True)
            self.end_date_edit.setDate(QDate.fromString(end_date, Qt.DateFormat.ISODate))
        else:
            self.radio_never.setChecked(True)

from PyQt6.QtGui import QIcon, QColor, QAction
from apscheduler.schedulers.background import BackgroundScheduler
import webbrowser
import subprocess
import uuid
from version import __version__ as APP_VERSION
import updater

# Đường dẫn lưu trữ dữ liệu (AppData hoặc cùng EXE)
# Ưu tiên: %AppData%\ZoomAuto (Windows best practice)
# Fallback: Cùng thư mục chứa EXE nếu AppData không khả dụng
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    BASE_DIR = Path(sys.executable).parent
else:
    # Running as script - lưu vào AppData
    BASE_DIR = Path.home() / "AppData" / "Local" / "ZoomAuto"

# Tạo thư mục nếu không tồn tại
BASE_DIR.mkdir(parents=True, exist_ok=True)

SCHEDULE_FILE = BASE_DIR / "zoom_schedule.json"

class ZoomOpener(QThread):
    """Thread để mở Zoom"""
    status_signal = pyqtSignal(str)
    
    def __init__(self, meeting_id, meeting_password=""):
        super().__init__()
        self.meeting_id = meeting_id
        self.meeting_password = meeting_password
        self.finished.connect(self.deleteLater)
    
    def run(self):
        try:
            print(f"[DEBUG] ZoomOpener.run() started")
            
            # Cách 1: Thử URL scheme
            zoom_url = f"zoommtg://join?confno={self.meeting_id}"
            if self.meeting_password:
                zoom_url += f"&pwd={self.meeting_password}"
            
            print(f"[DEBUG] Mở URL: {zoom_url}")
            webbrowser.open(zoom_url)
            
            # Emit signal nếu được kết nối
            try:
                self.status_signal.emit(f"✓ Mở Zoom {self.meeting_id} thành công")
            except:
                pass
            
            print(f"[DEBUG] Zoom đã được trigger")
            
        except Exception as e:
            print(f"[ERROR] Lỗi mở Zoom: {e}")
            import traceback
            traceback.print_exc()
            try:
                self.status_signal.emit(f"✗ Lỗi: {str(e)}")
            except:
                pass

class SchedulerManager:
    """Quản lý lập lịch"""
    def __init__(self, callback=None, parent_window=None):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.callback = callback
        self.jobs = {}
        self.active_threads = [] # Danh sách giữ các thread đang chạy
        self.parent_window = parent_window # Thêm parent_window
    
    def add_schedule(self, job_id, hour, minute, meeting_id, password="", enabled=True, name="", recurrence=None, zoom_link=""):
        """Thêm hoặc cập nhật lịch"""
        try:
            # Nếu job_id chưa có (thêm mới), tạo UUID
            if not job_id:
                job_id = str(uuid.uuid4())
            
            # Lưu thông tin
            self.jobs[job_id] = {
                'id': job_id,
                'name': name,
                'hour': hour,
                'minute': minute,
                'meeting_id': meeting_id,
                'password': password,
                'zoom_link': zoom_link,
                'enabled': enabled,
                'recurrence': recurrence
            }
            
            if enabled and recurrence:
                rec_type = recurrence.get('type', 'daily')
                details = recurrence.get('details', {})
                
                trigger_args = {'hour': hour, 'minute': minute}
                trigger_type = 'cron'
                
                # Setup End Date
                end_date = None
                if details and details.get('end_date'):
                    end_date = datetime.fromisoformat(details.get('end_date'))
                    trigger_args['end_date'] = end_date
                
                # Logic Trigger
                if rec_type == 'once':
                    trigger_type = 'date'
                    run_date_iso = recurrence.get('run_date')
                    if run_date_iso:
                         trigger_args = {'run_date': datetime.fromisoformat(run_date_iso)}
                    else:
                         return # Invalid once config
                         
                elif rec_type == 'daily':
                    pass # cron hour/min default
                    
                elif rec_type == 'weekly':
                    dow = details.get('days_of_week', [0])
                    dow_str = ",".join([str(d) for d in dow])
                    trigger_args['day_of_week'] = dow_str
                    
                elif rec_type == 'weekdays':
                    trigger_args['day_of_week'] = '0-4'
                    
                elif rec_type == 'custom':
                    unit = details.get('unit', 'tuần')
                    interval = details.get('interval', 1)
                    
                    if unit == 'ngày':
                        trigger_type = 'interval'
                        trigger_args = {
                            'days': interval, 
                            'start_date': datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
                        }
                        if end_date: trigger_args['end_date'] = end_date
                        
                    elif unit == 'tuần':
                        days = details.get('days_of_week', [])
                        if days:
                            dow_str = ",".join([str(d) for d in days])
                            trigger_args['day_of_week'] = dow_str
                        
                    elif unit == 'tháng':
                        pass

                # Add Job
                self.scheduler.add_job(
                    self._open_zoom,
                    trigger_type,
                    id=job_id,
                    args=[meeting_id, password, zoom_link],
                    replace_existing=True,
                    **trigger_args
                )
                
            else:
                try:
                    self.scheduler.remove_job(job_id)
                except: pass
            
            if self.callback:
                self.callback(f"✓ Cập nhật lịch thành công")
            return job_id

        except Exception as e:
            if self.callback:
                self.callback(f"✗ Lỗi: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _open_zoom(self, meeting_id, password, zoom_link=""):
        """Mở Zoom"""
        print(f"[LOG] Scheduler trigger: Mở Zoom lúc {datetime.now().strftime('%H:%M:%S')}")
        
        # Ưu tiên Link nếu có
        if zoom_link:
             url = zoom_link
             print(f"[LOG] Opening Zoom Link: {url}")
        else:
            # Tạo URL HTTPS từ ID/Pass
            if password:
                url = f"https://us06web.zoom.us/j/{meeting_id}?pwd={password}"
            else:
                url = f"https://us06web.zoom.us/j/{meeting_id}"
            print(f"[LOG] Opening HTTPS URL: {url}")
            
        webbrowser.open(url)
        if self.callback:
            self.callback(f"✓ Đã mở Zoom: {meeting_id if meeting_id else 'Link'}")
        if self.parent_window:
            try:
                name = meeting_id if meeting_id else (zoom_link if zoom_link else "Zoom")
                self.parent_window.show_tray_notification("Đã mở Zoom", name)
            except Exception:
                pass
    
    def _cleanup_thread(self, thread):
        """Dọn dẹp thread đã xong"""
        if thread in self.active_threads:
            self.active_threads.remove(thread)
            print(f"[DEBUG] Thread cleanup completed. Remaining: {len(self.active_threads)}")
    
    def remove_schedule(self, job_id):
        """Xóa lịch"""
        try:
            if job_id in self.jobs:
                # Xóa khỏi scheduler
                try:
                    self.scheduler.remove_job(job_id)
                except:
                    pass
                try:
                    self.scheduler.remove_job(f"remind_{job_id}")
                except:
                    pass
                    
                del self.jobs[job_id]
                return True
        except Exception as e:
            print(f"Lỗi xóa lịch: {e}")
        return False
    
    def toggle_schedule(self, job_id, enabled):
        """Bật/tắt lịch"""
        try:
            if job_id in self.jobs:
                self.jobs[job_id]['enabled'] = enabled
                job_data = self.jobs[job_id]
                
                # Gọi lại add_schedule để cập nhật trạng thái trong scheduler
                self.add_schedule(
                    job_id,
                    job_data['hour'],
                    job_data['minute'],
                    job_data['meeting_id'],
                    job_data['password'],
                    enabled,
                    job_data.get('name', ''),
                    recurrence=job_data.get('recurrence'),
                    zoom_link=job_data.get('zoom_link', '')
                )
                
                if self.callback:
                    status = "Kích hoạt" if enabled else "Vô hiệu hóa"
                    self.callback(f"✓ {status} lịch thành công")
                
                return True
        except Exception as e:
            print(f"Lỗi toggle lịch: {e}")
            if self.callback:
                self.callback(f"✗ Lỗi: {str(e)}")
        return False
    
    def get_all_jobs(self):
        """Lấy tất cả lịch"""
        return self.jobs

    def get_next_run_info(self):
        """Trả về (job_id, thời_gian_chạy_kế_tiếp) nếu có."""
        try:
            jobs = self.scheduler.get_jobs()
            next_job = None
            for job in jobs:
                if job.id.startswith("remind_"):
                    continue
                if not job.next_run_time:
                    continue
                if not next_job or job.next_run_time < next_job[1]:
                    next_job = (job.id, job.next_run_time)
            return next_job
        except Exception:
            return None
    
    def stop(self):
        """Dừng scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()

    def _show_reminder(self, meeting_id, hour, minute):
        msg = f"Sắp đến giờ mở Zoom: {meeting_id} vào lúc {hour:02d}:{minute:02d}"
        try:
            if self.parent_window:
                QMessageBox.information(self.parent_window, "Nhắc nhở Zoom", msg)
            else:
                print(f"[REMINDER] {msg}")
        except Exception as e:
            print(f"[REMINDER-ERROR] {msg} ({e})")

class TestZoomDialog(QDialog):
    """Dialog để test mở Zoom"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🧪 Test Mở Zoom")
        self.resize(500, 300)
        
        layout = QFormLayout()
        
        # URL hoặc Meeting ID
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Nhập URL HTTPS hoặc Meeting ID")
        layout.addRow("URL/Meeting ID:", self.url_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("(Tùy chọn)")
        layout.addRow("Mật khẩu:", self.password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        open_url_btn = QPushButton("🔗 Mở URL HTTPS")
        open_url_btn.clicked.connect(self.open_https_url)
        button_layout.addWidget(open_url_btn)
        
        open_zoom_btn = QPushButton("📱 Mở zoommtg://")
        open_zoom_btn.clicked.connect(self.open_zoom_scheme)
        button_layout.addWidget(open_zoom_btn)
        
        close_btn = QPushButton("Đóng")
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)
        
        layout.addRow(button_layout)
        
        self.setLayout(layout)
    
    def open_https_url(self):
        """Mở URL HTTPS"""
        url = self.url_input.text().strip()
        if not url:
            return
        
        # Nếu là URL hoặc Meeting ID
        if url.startswith('http'):
            webbrowser.open(url)
        else:
            # Nếu là Meeting ID, tạo URL
            pwd = self.password_input.text().strip()
            if pwd:
                url = f"https://us06web.zoom.us/j/{url}?pwd={pwd}"
            else:
                url = f"https://us06web.zoom.us/j/{url}"
            webbrowser.open(url)
        
        print(f"[DEBUG] Mở HTTPS: {url}")
    
    def open_zoom_scheme(self):
        """Mở zoommtg://"""
        meeting_id = self.url_input.text().strip()
        password = self.password_input.text().strip()
        
        if not meeting_id:
            return
        
        url = f"zoommtg://join?confno={meeting_id}"
        if password:
            url += f"&pwd={password}"
        
        webbrowser.open(url)
        print(f"[DEBUG] Mở zoommtg: {url}")


class HelpDialog(QDialog):
    """Dialog hướng dẫn sử dụng với giao diện chuyên nghiệp"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hướng dẫn sử dụng")
        self.resize(800, 600)
        self.setModal(True)
        
        # Layout chính
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === HEADER ===
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #059669,
                    stop:1 #047857
                );
            }
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(30, 20, 30, 20)
        
        title = QLabel("📚 Hướng Dẫn Sử Dụng")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: white;
            background: transparent;
        """)
        
        subtitle = QLabel("Tìm hiểu cách sử dụng Zoom Auto Scheduler hiệu quả")
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: rgba(255, 255, 255, 0.9);
            background: transparent;
            margin-top: 5px;
        """)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addStretch()
        
        # === TAB WIDGET ===
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f1f5f9;
                color: #475569;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #059669;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e2e8f0;
            }
        """)
        
        # Tab 1: Bắt đầu nhanh
        quick_start = self.create_quick_start_tab()
        tab_widget.addTab(quick_start, "🚀 Bắt đầu nhanh")
        
        # Tab 2: Quản lý lịch
        manage_tab = self.create_manage_tab()
        tab_widget.addTab(manage_tab, "📅 Quản lý lịch")
        
        # Tab 3: Cài đặt Zoom
        zoom_settings = self.create_zoom_settings_tab()
        tab_widget.addTab(zoom_settings, "⚙️ Cài đặt Zoom")
        
        # Tab 4: FAQ
        faq_tab = self.create_faq_tab()
        tab_widget.addTab(faq_tab, "❓ Câu hỏi thường gặp")
        
        # === FOOTER ===
        footer = QWidget()
        footer.setStyleSheet("background-color: #f8fafc; border-top: 1px solid #e2e8f0;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(30, 15, 30, 15)
        
        close_btn = QPushButton("Đóng")
        close_btn.setFixedSize(100, 36)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #047857; }
            QPushButton:pressed { background-color: #065f46; }
        """)
        close_btn.clicked.connect(self.accept)
        
        footer_layout.addStretch()
        footer_layout.addWidget(close_btn)
        footer_layout.addStretch()
        
        # Assemble
        main_layout.addWidget(header)
        main_layout.addWidget(tab_widget, 1)
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
    
    def create_quick_start_tab(self):
        """Tab bắt đầu nhanh"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)
        
        content = QTextBrowser()
        content.setOpenExternalLinks(True)
        content.setStyleSheet("""
            QTextBrowser {
                border: none;
                background-color: transparent;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        
        html = """
        <style>
            body { font-family: 'Segoe UI', sans-serif; color: #1e293b; }
            h2 { color: #059669; margin-top: 20px; font-size: 20px; }
            .step { 
                background: #f0fdf4; 
                padding: 15px 20px; 
                border-left: 4px solid #059669;
                margin: 15px 0;
                border-radius: 6px;
            }
            .step-title { font-weight: bold; color: #047857; font-size: 16px; margin-bottom: 8px; }
            ul { margin: 10px 0; padding-left: 25px; }
            li { margin: 6px 0; line-height: 1.5; }
            .highlight { background-color: #fef3c7; padding: 2px 6px; border-radius: 3px; font-weight: 600; }
        </style>
        
        <h2>🎯 Bắt đầu trong 3 bước đơn giản</h2>
        
        <div class="step">
            <div class="step-title">Bước 1: Thêm lịch mới</div>
            <ul>
                <li>Nhấn nút <span class="highlight">➕ Thêm lịch</span> ở góc trên bên phải</li>
                <li>Nhập <b>Tên phòng Zoom</b> (ví dụ: "Họp team buổi sáng")</li>
                <li>Dán <b>Link Zoom</b> vào ô tương ứng (cách khuyên dùng) <b>HOẶC</b> nhập Meeting ID + Mật khẩu</li>
                <li>Chọn <b>Giờ</b> muốn tự động vào phòng</li>
                <li>Chọn <b>Lặp lại</b>: Không lặp, Hàng ngày, Hàng tuần, hoặc Tùy chỉnh</li>
            </ul>
        </div>
        
        <div class="step">
            <div class="step-title">Bước 2: Bật lịch hẹn</div>
            <ul>
                <li>Đảm bảo nút gạt ở cột <span class="highlight">Bật/Tắt</span> đang ở trạng thái BẬT (màu xanh)</li>
                <li>Lịch hẹn chỉ hoạt động khi được bật</li>
                <li>Bạn có thể tắt tạm thời mà không cần xóa lịch</li>
            </ul>
        </div>
        
        <div class="step">
            <div class="step-title">Bước 3: Để phần mềm chạy ngầm</div>
            <ul>
                <li>Giữ phần mềm <b>mở</b> (có thể thu nhỏ cửa sổ)</li>
                <li>Khi đến giờ, phần mềm sẽ tự động mở Zoom trong trình duyệt</li>
                <li>Bạn sẽ nghe thông báo âm thanh khi lịch được kích hoạt</li>
            </ul>
        </div>
        
        <h2>💡 Lưu ý quan trọng</h2>
        <ul>
            <li>⏰ <b>Độ chính xác:</b> Lịch sẽ được kiểm tra mỗi 30 giây</li>
            <li>🌐 <b>Link Zoom:</b> Ưu tiên dùng link thay vì Meeting ID để vào phòng nhanh nhất</li>
            <li>🔐 <b>Tự động hoàn toàn:</b> Xem tab "Cài đặt Zoom" để tắt phòng chờ</li>
            <li>💻 <b>Giữ máy mở:</b> Máy tính cần ở trạng thái bật và không sleep khi đến giờ hẹn</li>
        </ul>
        """
        
        content.setHtml(html)
        layout.addWidget(content)
        
        return widget
    
    def create_manage_tab(self):
        """Tab quản lý lịch"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)
        
        content = QTextBrowser()
        content.setOpenExternalLinks(True)
        content.setStyleSheet("""
            QTextBrowser { border: none; background: transparent; font-size: 14px; }
        """)
        
        html = """
        <style>
            body { font-family: 'Segoe UI', sans-serif; color: #1e293b; }
            h2 { color: #059669; margin-top: 20px; font-size: 20px; }
            .feature {
                background: #f8fafc;
                padding: 15px;
                margin: 12px 0;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            }
            .feature-title {
                font-weight: bold;
                color: #0f172a;
                font-size: 15px;
                margin-bottom: 8px;
            }
            .btn-example {
                display: inline-block;
                padding: 4px 12px;
                background: #e0f2fe;
                color: #0369a1;
                border-radius: 4px;
                font-weight: 600;
                font-size: 13px;
            }
        </style>
        
        <h2>🎛️ Các chức năng quản lý</h2>
        
        <div class="feature">
            <div class="feature-title">🔄 Bật/Tắt lịch</div>
            Sử dụng nút gạt ở cột đầu tiên để bật/tắt lịch hẹn mà không cần xóa.
            <br>• <b>Màu xanh:</b> Lịch đang hoạt động
            <br>• <b>Màu xám:</b> Lịch bị tắt tạm thời
        </div>
        
        <div class="feature">
            <div class="feature-title">✏️ Chỉnh sửa lịch</div>
            Nhấn nút <span class="btn-example">Sửa</span> để thay đổi thông tin:
            <br>• Đổi tên phòng họp
            <br>• Cập nhật link, Meeting ID, hoặc mật khẩu
            <br>• Thay đổi giờ hoặc tần suất lặp lại
        </div>
        
        <div class="feature">
            <div class="feature-title">📋 Nhân bản lịch</div>
            Nhấn nút <span class="btn-example">Nhân bản</span> để tạo bản sao của lịch hiện tại.
            <br>Tiện lợi khi bạn cần tạo nhiều lịch tương tự nhau.
        </div>
        
        <div class="feature">
            <div class="feature-title">🧪 Test Zoom</div>
            Nhấn nút <span class="btn-example">Test</span> để kiểm tra link/ID có hoạt động không.
            <br>Phần mềm sẽ mở Zoom ngay lập tức để bạn xác nhận.
        </div>
        
        <div class="feature">
            <div class="feature-title">🗑️ Xóa lịch</div>
            Nhấn nút <span class="btn-example" style="background:#fee2e2;color:#991b1b;">Xóa</span> để xóa vĩnh viễn lịch hẹn.
            <br><b>Lưu ý:</b> Hành động này không thể hoàn tác!
        </div>
        
        <h2>🔁 Các loại lặp lại</h2>
        <div class="feature">
            <b>• Không lặp:</b> Chỉ chạy một lần duy nhất
            <br><b>• Hàng ngày:</b> Lặp lại mỗi ngày
            <br><b>• Hàng tuần:</b> Lặp lại mỗi tuần vào cùng thứ
            <br><b>• Tùy chỉnh:</b> Tự định nghĩa chu kỳ (mỗi X ngày/tuần/tháng/năm)
        </div>
        
        <h2>👁️ Xem chi tiết</h2>
        <div class="feature">
            Nhấn vào một dòng trong bảng để xem thông tin chi tiết ở khung bên phải:
            <br>• Thời gian kế tiếp lịch sẽ chạy
            <br>• Các lần chạy trong tương lai
            <br>• Thông tin đầy đủ về phòng họp
        </div>
        """
        
        content.setHtml(html)
        layout.addWidget(content)
        
        return widget
    
    def create_zoom_settings_tab(self):
        """Tab cài đặt Zoom"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)
        
        content = QTextBrowser()
        content.setOpenExternalLinks(True)
        content.setStyleSheet("""
            QTextBrowser { border: none; background: transparent; font-size: 14px; }
        """)
        
        html = """
        <style>
            body { font-family: 'Segoe UI', sans-serif; color: #1e293b; }
            h2 { color: #dc2626; margin-top: 20px; font-size: 20px; }
            h3 { color: #059669; margin-top: 15px; }
            .warning {
                background: #fef2f2;
                border-left: 4px solid #dc2626;
                padding: 15px;
                margin: 15px 0;
                border-radius: 6px;
            }
            .success {
                background: #f0fdf4;
                border-left: 4px solid #059669;
                padding: 15px;
                margin: 15px 0;
                border-radius: 6px;
            }
            .step-number {
                display: inline-block;
                background: #059669;
                color: white;
                width: 28px;
                height: 28px;
                border-radius: 50%;
                text-align: center;
                line-height: 28px;
                font-weight: bold;
                margin-right: 8px;
            }
            ol { counter-reset: item; list-style: none; padding-left: 0; }
            ol > li { counter-increment: item; margin: 20px 0; }
            ol > li::before {
                content: counter(item);
                background: #059669;
                color: white;
                width: 28px;
                height: 28px;
                border-radius: 50%;
                display: inline-block;
                text-align: center;
                line-height: 28px;
                font-weight: bold;
                margin-right: 12px;
            }
            .link { color: #0ea5e9; text-decoration: none; font-weight: 600; }
            .link:hover { text-decoration: underline; }
        </style>
        
        <h2>⚙️ Cài đặt Zoom để tự động hoàn toàn</h2>
        
        <div class="warning">
            <b>⚠️ Quan trọng:</b> Để phần mềm có thể tự động vào phòng họp mà <b>không cần bạn nhấn nút "Join"</b> hay chờ duyệt, bạn cần cấu hình trong tài khoản Zoom của mình.
        </div>
        
        <h3>🔧 Các bước cài đặt:</h3>
        
        <ol>
            <li>
                Đăng nhập vào tài khoản Zoom tại:<br>
                <a href="https://zoom.us/profile/setting" class="link">https://zoom.us/profile/setting</a>
            </li>
            
            <li>
                Tìm đến mục <b>"Security" (Bảo mật)</b>
            </li>
            
            <li>
                <b>TẮT</b> tính năng <b>"Waiting Room" (Phòng chờ)</b><br>
                Khi tắt, mọi người có link sẽ vào thẳng phòng họp mà không cần chờ duyệt.
            </li>
            
            <li>
                <b>Đăng nhập sẵn trên trình duyệt:</b><br>
                Mở trình duyệt web mặc định → Truy cập <a href="https://zoom.us" class="link">zoom.us</a> → Đăng nhập vào tài khoản của bạn.<br>
                Điều này giúp Zoom nhận diện bạn khi phần mềm tự động mở link.
            </li>
            
            <li>
                (Tùy chọn) Nếu bạn là người tạo phòng:<br>
                BẬT <b>"Allow participants to join before host"</b> để người khác có thể vào trước bạn.
            </li>
        </ol>
        
        <div class="success">
            <b>✅ Hoàn tất!</b> Sau khi cài đặt, phần mềm sẽ tự động đưa bạn vào phòng họp mà không cần thao tác thủ công.
        </div>
        
        <div class="warning">
            <b>🔒 Lưu ý bảo mật:</b> Việc tắt Phòng chờ có thể làm giảm tính bảo mật. Chỉ chia sẻ link/ID với người tin tưởng.
        </div>
        
        <h3>🌐 Tại sao nên dùng Link thay vì Meeting ID?</h3>
        <div class="success">
            • Link Zoom chứa đầy đủ Meeting ID + Password<br>
            • Tự động điền thông tin, không cần nhập tay<br>
            • Nhanh hơn và ít lỗi hơn<br>
            • Được Zoom khuyến nghị sử dụng
        </div>
        """
        
        content.setHtml(html)
        layout.addWidget(content)
        
        return widget
    
    def create_faq_tab(self):
        """Tab câu hỏi thường gặp"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)
        
        content = QTextBrowser()
        content.setOpenExternalLinks(True)
        content.setStyleSheet("""
            QTextBrowser { border: none; background: transparent; font-size: 14px; }
        """)
        
        html = """
        <style>
            body { font-family: 'Segoe UI', sans-serif; color: #1e293b; }
            h2 { color: #059669; margin-top: 20px; font-size: 20px; }
            .faq {
                background: #f8fafc;
                padding: 15px 20px;
                margin: 12px 0;
                border-radius: 8px;
                border-left: 4px solid #0ea5e9;
            }
            .question {
                font-weight: bold;
                color: #0f172a;
                font-size: 15px;
                margin-bottom: 8px;
            }
            .answer { color: #475569; line-height: 1.6; }
        </style>
        
        <h2>❓ Câu hỏi thường gặp (FAQ)</h2>
        
        <div class="faq">
            <div class="question">Q: Phần mềm có tự động bật Zoom app không?</div>
            <div class="answer">
                <b>A:</b> Không. Phần mềm sẽ mở link Zoom trong trình duyệt web mặc định. 
                Trình duyệt sẽ hỏi bạn có muốn mở bằng Zoom app hay không. 
                Bạn có thể chọn "Luôn cho phép" để lần sau tự động mở.
            </div>
        </div>
        
        <div class="faq">
            <div class="question">Q: Tôi có thể đóng phần mềm sau khi thêm lịch không?</div>
            <div class="answer">
                <b>A:</b> Không được. Phần mềm cần <b>luôn chạy</b> (có thể thu nhỏ) để kiểm tra và kích hoạt lịch đúng giờ.
            </div>
        </div>
        
        <div class="faq">
            <div class="question">Q: Nếu máy tính đang sleep/tắt màn hình thì sao?</div>
            <div class="answer">
                <b>A:</b> Phần mềm sẽ không thể kích hoạt lịch khi máy đang sleep. 
                Đảm bảo máy tính ở trạng thái bật và không sleep vào giờ họp.
            </div>
        </div>
        
        <div class="faq">
            <div class="question">Q: Độ chính xác của lịch là bao nhiêu?</div>
            <div class="answer">
                <b>A:</b> Phần mềm kiểm tra lịch mỗi 30 giây. Lịch có thể được kích hoạt 
                muộn tối đa 30 giây so với giờ đã hẹn.
            </div>
        </div>
        
        <div class="faq">
            <div class="question">Q: Tôi có thể đặt lịch cho quá khứ không?</div>
            <div class="answer">
                <b>A:</b> Không. Phần mềm chỉ cho phép đặt lịch từ thời điểm hiện tại trở đi.
            </div>
        </div>
        
        <div class="faq">
            <div class="question">Q: Lịch lặp lại sẽ dừng khi nào?</div>
            <div class="answer">
                <b>A:</b> Bạn có thể chọn:
                <br>• <b>Không bao giờ:</b> Lặp vô thời hạn
                <br>• <b>Sau X lần:</b> Dừng sau số lần chạy nhất định
                <br>• <b>Vào ngày:</b> Dừng vào một ngày cụ thể
            </div>
        </div>
        
        <div class="faq">
            <div class="question">Q: Dữ liệu lịch của tôi được lưu ở đâu?</div>
            <div class="answer">
                <b>A:</b> Lịch được lưu trong file <b>zoom_schedule.json</b> cùng thư mục với phần mềm. 
                Bạn có thể sao lưu file này để giữ dữ liệu.
            </div>
        </div>
        
        <div class="faq">
            <div class="question">Q: Phần mềm có gửi dữ liệu về máy chủ không?</div>
            <div class="answer">
                <b>A:</b> <b>Không.</b> Mọi dữ liệu đều được lưu trữ cục bộ trên máy tính của bạn. 
                Phần mềm không kết nối internet ngoài việc mở link Zoom.
            </div>
        </div>
        
        <div class="faq">
            <div class="question">Q: Làm sao để liên hệ hỗ trợ?</div>
            <div class="answer">
                <b>A:</b> Bạn có thể liên hệ:
                <br>📱 SĐT: 0936 099 625
                <br>📧 Email: tronghv77@gmail.com
            </div>
        </div>
        """
        
        content.setHtml(html)
        layout.addWidget(content)
        
        return widget


class AboutDialog(QDialog):
    """Dialog giới thiệu phần mềm với giao diện chuyên nghiệp"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Giới thiệu")
        self.setFixedSize(500, 520)
        self.setModal(True)
        
        # Tạo layout chính
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === HEADER SECTION (Gradient background) ===
        header = QWidget()
        header.setFixedHeight(160)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2563eb,
                    stop:1 #1e40af
                );
                border-radius: 0px;
            }
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(30, 30, 30, 20)
        header_layout.setSpacing(10)
        
        # Icon và tiêu đề
        title_label = QLabel("🎥 Zoom Auto Scheduler")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: white;
            background: transparent;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("Công cụ tự động vào Zoom thông minh")
        subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: rgba(255, 255, 255, 0.9);
            background: transparent;
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        version_label = QLabel("Version 1.0.0 • January 2026")
        version_label.setStyleSheet("""
            font-size: 12px;
            color: rgba(255, 255, 255, 0.7);
            background: transparent;
            margin-top: 5px;
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addWidget(version_label)
        header_layout.addStretch()
        
        # === CONTENT SECTION ===
        content = QWidget()
        content.setStyleSheet("background-color: white;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(35, 30, 35, 30)
        content_layout.setSpacing(20)
        
        # Developer info
        dev_label = QLabel("👨‍💻 Thông tin nhà phát triển")
        dev_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #1e293b;
            margin-bottom: 10px;
        """)
        content_layout.addWidget(dev_label)
        
        # Info cards với style card hiện đại
        info_style = """
            QLabel {
                background-color: #f8fafc;
                padding: 12px 15px;
                border-left: 3px solid #2563eb;
                border-radius: 6px;
                color: #334155;
                font-size: 13px;
            }
        """
        
        name_label = QLabel("👤  <b>Họ tên:</b> Hồ Văn Trọng")
        name_label.setStyleSheet(info_style)
        content_layout.addWidget(name_label)
        
        phone_label = QLabel("📱  <b>Điện thoại:</b> 0936 099 625")
        phone_label.setStyleSheet(info_style)
        content_layout.addWidget(phone_label)
        
        email_label = QLabel("📧  <b>Email:</b> tronghv77@gmail.com")
        email_label.setStyleSheet(info_style)
        email_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        email_label.setCursor(Qt.CursorShape.IBeamCursor)
        content_layout.addWidget(email_label)
        
        # Divider line
        line = QLabel()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #e2e8f0; margin: 10px 0;")
        content_layout.addWidget(line)
        
        # Thank you message
        thank_msg = QLabel("💙 Cảm ơn bạn đã sử dụng sản phẩm!\nChúc bạn có những buổi họp hiệu quả!")
        thank_msg.setStyleSheet("""
            font-size: 13px;
            color: #475569;
            line-height: 1.6;
            background: transparent;
        """)
        thank_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thank_msg.setWordWrap(True)
        content_layout.addWidget(thank_msg)
        
        content_layout.addStretch()
        
        # === FOOTER SECTION ===
        footer = QWidget()
        footer.setStyleSheet("background-color: #f8fafc; border-top: 1px solid #e2e8f0;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(30, 20, 30, 20)
        
        ok_button = QPushButton("Đóng")
        ok_button.setFixedSize(120, 40)
        ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        ok_button.clicked.connect(self.accept)
        
        footer_layout.addStretch()
        footer_layout.addWidget(ok_button)
        footer_layout.addStretch()
        
        # Thêm các section vào layout chính
        main_layout.addWidget(header)
        main_layout.addWidget(content, 1)
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
        
        # Style tổng thể cho dialog
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 12px;
            }
        """)


class ScheduleDialog(QDialog):
    """Dialog để thêm lịch mới"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm lịch Zoom")
        self.resize(550, 600)
        
        self.custom_recurrence_data = None # Store custom data
        
        # Modern styling
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f9ff,
                    stop:1 #e0f2fe
                );
            }
            
            QWidget#headerWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9,
                    stop:1 #0284c7
                );
                border-radius: 10px;
            }
            
            QLabel#headerTitle {
                font-size: 22px;
                font-weight: bold;
                color: white;
                background: transparent;
            }
            
            QLabel#headerSubtitle {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.95);
                background: transparent;
            }
            
            QLabel {
                color: #1e293b;
                font-size: 13px;
                font-weight: 600;
            }
            
            QLabel#noteLabel {
                color: #64748b;
                font-size: 11px;
                font-style: italic;
                font-weight: 400;
            }
            
            QLineEdit, QDateEdit, QComboBox {
                padding: 10px 12px;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                background-color: white;
                font-size: 13px;
                color: #0f172a;
            }
            
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border: 2px solid #0ea5e9;
                background-color: white;
            }
            
            QLineEdit::placeholder {
                color: #94a3b8;
            }
            
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            
            QPushButton#cancelBtn {
                background-color: #f1f5f9;
                color: #475569;
                padding: 11px 28px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #cbd5e1;
            }
            
            QPushButton#cancelBtn:hover {
                background-color: #e2e8f0;
            }
            
            QPushButton#saveBtn {
                background-color: white;
                color: #0ea5e9;
                padding: 11px 28px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #0ea5e9;
            }
            
            QPushButton#saveBtn:hover {
                background-color: #f0f9ff;
                border: 2px solid #0284c7;
                color: #0284c7;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === HEADER ===
        header = QWidget()
        header.setObjectName("headerWidget")
        header.setFixedHeight(90)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(25, 15, 25, 15)
        header_layout.setSpacing(5)
        
        title = QLabel("➕ Thêm lịch Zoom")
        title.setObjectName("headerTitle")
        
        subtitle = QLabel("Tạo lịch hẹn tự động cho phòng họp Zoom")
        subtitle.setObjectName("headerSubtitle")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addStretch()
        
        # === CONTENT ===
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        layout = QFormLayout(content_widget)
        layout.setSpacing(18)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        # Tên phòng Zoom
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ví dụ: Họp lớp, Họp công ty...")
        self.name_input.setToolTip("Đặt tên cho phòng Zoom này để dễ nhận biết")
        label_name = QLabel("Tên phòng Zoom <font color='#dc2626'>*</font>:")
        layout.addRow(label_name, self.name_input)
        
        # Link Zoom (Mới)
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("https://us06web.zoom.us/j/...")
        self.link_input.setToolTip("Nhập link Zoom trực tiếp (nếu có)")
        layout.addRow("Link Zoom:", self.link_input)
        
        # Note
        note_label = QLabel("• Vui lòng nhập <b>Link Zoom</b> HOẶC <b>Meeting ID</b>")
        note_label.setObjectName("noteLabel")
        layout.addRow("", note_label)

        # Meeting ID
        self.meeting_id_input = QLineEdit()
        self.meeting_id_input.setToolTip("Nhập Meeting ID (11 chữ số)")
        self.meeting_id_input.setInputMask("000 0000 0000;_")
        layout.addRow("Meeting ID:", self.meeting_id_input)
        
        # Meeting Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("(Tùy chọn)")
        self.password_input.setToolTip("Nhập mật khẩu phòng Zoom (nếu có)")
        layout.addRow("Mật khẩu:", self.password_input)

        # Chọn giờ (Combo boxes)
        time_layout = QHBoxLayout()
        
        self.hour_combo = QComboBox()
        self.hour_combo.addItems([f"{i:02d}" for i in range(24)])
        self.hour_combo.setCurrentText("08")
        self.hour_combo.setMaxVisibleItems(10)
        
        self.minute_combo = QComboBox()
        self.minute_combo.addItems([f"{i:02d}" for i in range(60)])
        self.minute_combo.setCurrentText("00")
        self.minute_combo.setMaxVisibleItems(10)
        
        time_layout.addWidget(self.hour_combo)
        time_layout.addWidget(QLabel(":"))
        time_layout.addWidget(self.minute_combo)
        time_layout.addStretch()
        
        layout.addRow("Giờ:", time_layout)

        # Chế độ lặp lại (ComboBox)
        self.recurrence_combo = QComboBox()
        today_dow = QDate.currentDate().dayOfWeek() - 1 # 0=Mon
        today_name = WEEKDAYS_MAP[today_dow]
        
        self.recurrence_options = [
            "Không lặp lại",
            "Hàng ngày",
            f"Hàng tuần vào thứ {today_name}",
            "Mọi ngày trong tuần (từ thứ Hai tới thứ Sáu)",
            "Tùy chỉnh..."
        ]
        self.recurrence_combo.addItems(self.recurrence_options)
        layout.addRow("Lặp lại:", self.recurrence_combo)
        
        # Chọn ngày (Chỉ hiện khi chọn "Không lặp lại")
        self.date_label = QLabel("Ngày:")
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumDate(QDate.currentDate())
        
        # Calendar styling
        self.date_edit.calendarWidget().setStyleSheet("""
            QCalendarWidget QToolButton {
                color: black;
                icon-size: 20px;
            }
            QCalendarWidget QMenu {
                width: 150px;
                left: 20px;
                color: white;
            }
            QCalendarWidget QSpinBox { 
                width: 50px; 
                font-size: 14px; 
                color: black; 
            }
            QCalendarWidget QWidget { alternate-background-color: #f0f0f0; }
            QCalendarWidget QAbstractItemView:enabled {
                color: black;
                selection-background-color: #0ea5e9;
                selection-color: white;
            }
        """)
        
        layout.addRow(self.date_label, self.date_edit)
        
        # Event update format
        self.recurrence_combo.currentIndexChanged.connect(self.on_recurrence_changed)
        
        # Init state
        self.on_recurrence_changed()
        
        # === FOOTER ===
        footer = QWidget()
        footer.setStyleSheet("background-color: white; border-top: 1px solid #e2e8f0;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(30, 15, 30, 15)
        footer_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setFixedWidth(110)
        
        save_btn = QPushButton("💾 Lưu")
        save_btn.setObjectName("saveBtn")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.accept)
        save_btn.setFixedWidth(110)
        
        footer_layout.addStretch()
        footer_layout.addWidget(cancel_btn)
        footer_layout.addWidget(save_btn)
        
        # Assemble all
        main_layout.addWidget(header)
        main_layout.addWidget(content_widget, 1)
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)

    def accept(self):
        """Xác thực dữ liệu trước khi đóng"""
        # Xóa khoảng trắng để lấy chuỗi số thực
        meeting_id_digits = self.meeting_id_input.text().replace(" ", "")

        # Chỉ kiểm tra nếu người dùng đã bắt đầu nhập ID
        if meeting_id_digits:
            # hasAcceptableInput() kiểm tra xem mask đã được điền đầy đủ chưa
            if not self.meeting_id_input.hasAcceptableInput():
                QMessageBox.warning(self, "Lỗi Meeting ID", "Meeting ID phải có đủ 11 chữ số.")
                return # Ngăn không cho đóng dialog
            
            if meeting_id_digits.startswith('0') or meeting_id_digits.startswith('1'):
                QMessageBox.warning(self, "Lỗi Meeting ID", "Meeting ID không được bắt đầu bằng số 0 hoặc 1.")
                return # Ngăn không cho đóng dialog

        # Nếu hợp lệ, gọi phương thức accept gốc
        super().accept()
    
    def on_recurrence_changed(self):
        text = self.recurrence_combo.currentText()
        
        # Show/Hide date picker
        is_once = text == "Không lặp lại"
        self.date_label.setVisible(is_once)
        self.date_edit.setVisible(is_once)
        
        # Handle Custom
        if text == "Tùy chỉnh...":
            dialog = CustomRecurrenceDialog(self)
            if self.custom_recurrence_data:
                dialog.set_data(self.custom_recurrence_data)
                
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.custom_recurrence_data = dialog.get_data()
            else:
                # If cancelled, revert to Daily or whatever
                self.recurrence_combo.setCurrentIndex(1) 

    def get_data(self):
        hour = int(self.hour_combo.currentText())
        minute = int(self.minute_combo.currentText())
        
        recurrence_type = "daily"
        text = self.recurrence_combo.currentText()
        
        dt_iso = None
        recurrence_details = {}
        
        if text == "Không lặp lại":
            recurrence_type = "once"
            date = self.date_edit.date()
            dt = datetime(date.year(), date.month(), date.day(), hour, minute)
            dt_iso = dt.isoformat()
        elif text == "Hàng ngày":
            recurrence_type = "daily"
        elif text.startswith("Hàng tuần"):
            recurrence_type = "weekly"
            # Auto detect current day of week
            dow = QDate.currentDate().dayOfWeek() - 1
            recurrence_details = {'days_of_week': [dow]}
        elif text.startswith("Mọi ngày"):
            recurrence_type = "weekdays"
            recurrence_details = {'days_of_week': [0, 1, 2, 3, 4]}
        elif text == "Tùy chỉnh...":
            recurrence_type = "custom"
            recurrence_details = self.custom_recurrence_data

        return {
            'name': self.name_input.text(),
            'meeting_id': self.meeting_id_input.text().replace(" ", ""),
            'password': self.password_input.text(),
            'zoom_link': self.link_input.text(),
            'hour': hour,
            'minute': minute,
            'recurrence': {
                'type': recurrence_type,
                'run_date': dt_iso,
                'details': recurrence_details
            }
        }

    def set_data(self, data):
        """Điền dữ liệu có sẵn vào dialog (dùng cho việc chỉnh sửa)"""
        self.name_input.setText(data.get('name', ''))
        self.link_input.setText(data.get('zoom_link', ''))
        self.meeting_id_input.setText(data.get('meeting_id', ''))
        self.password_input.setText(data.get('password', ''))
        
        self.hour_combo.setCurrentText(f"{data.get('hour', 8):02d}")
        self.minute_combo.setCurrentText(f"{data.get('minute', 0):02d}")
        
        recurrence = data.get('recurrence', {})
        rec_type = recurrence.get('type')
        details = recurrence.get('details', {})
        
        # Mặc định là hàng ngày
        combo_index = 1 

        if rec_type == 'once':
            combo_index = 0
            if recurrence.get('run_date'):
                # Chuyển đổi an toàn sang QDateTime
                try:
                    dt = QDateTime.fromString(recurrence.get('run_date'), Qt.DateFormat.ISODate)
                    self.date_edit.setDate(dt.date())
                except:
                    pass
        elif rec_type == 'daily':
            combo_index = 1
        elif rec_type == 'weekdays':
            combo_index = 3
        elif rec_type in ['weekly', 'custom']:
            combo_index = 4 # Chuyển sang Tùy chỉnh
            
            # Nếu là weekly, chuyển đổi sang format của custom
            if rec_type == 'weekly':
                 self.custom_recurrence_data = {
                    'interval': 1, 'unit': 'tuần',
                    'days_of_week': details.get('days_of_week', []),
                    'end_date': details.get('end_date')
                }
            else: # custom
                self.custom_recurrence_data = details

        self.recurrence_combo.setCurrentIndex(combo_index)
        self.on_recurrence_changed()

class ZoomAutoApp(QMainWindow):
    """Ứng dụng chính"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"🎯 Zoom Auto Scheduler v{APP_VERSION} - Hẹn Giờ Tự Động")
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowIcon(QIcon(str(Path(__file__).parent / "app.ico")))
        # Khởi tạo scheduler (trước khi UI để tránh lỗi callback)
        self.scheduler = SchedulerManager(callback=self.show_message, parent_window=self)
        self.tray_icon = None
        self.exit_requested = False
        # Tạo UI trước
        self.init_ui()
        # Tải lịch SAU khi UI sẵn sàng
        self.load_schedules()
        self.refresh_table()
        self.init_tray()
        self.update_tray_tooltip()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        self.current_selected_job_id = None
        
        APP_STYLE = """
            QMainWindow { 
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f9ff,
                    stop:1 #e0f2fe
                );
            }
            
            QWidget#headerWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9,
                    stop:1 #0284c7
                );
                border-radius: 12px;
            }
            
            QLabel#titleMain {
                font-size: 24px; 
                font-weight: bold; 
                color: white;
                background: transparent;
            }
            
            QLabel#subtitleMain {
                font-size: 13px;
                color: rgba(255, 255, 255, 0.95);
                background: transparent;
            }
            
            /* Status Label */
            QLabel#status {
                color: #0284c7;
                font-weight: 600;
                font-size: 13px;
                padding: 8px 12px;
                background-color: #e0f2fe;
                border-radius: 6px;
            }
            
            /* Main Add Button */
            QPushButton#addBtn {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0ea5e9,
                    stop:1 #0284c7
                );
                color: white;
                padding: 12px 28px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton#addBtn:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0284c7,
                    stop:1 #0369a1
                );
            }
            QPushButton#addBtn:pressed {
                background: #075985;
            }
            
            /* Table Styling */
            QTableWidget {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                gridline-color: #e2e8f0;
                selection-background-color: #dbeafe;
                font-size: 13px;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
            }
            
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #0f172a;
            }
            
            /* Table Header */
            QHeaderView::section {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8fafc,
                    stop:1 #f1f5f9
                );
                color: #475569;
                padding: 10px 8px;
                border: none;
                border-bottom: 2px solid #cbd5e1;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }
            
            QHeaderView::section:first {
                border-top-left-radius: 10px;
            }
            
            QHeaderView::section:last {
                border-top-right-radius: 10px;
            }
            
            /* Table Buttons */
            QTableWidget QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                padding: 6px 12px;
            }
            
            QTableWidget QPushButton:hover {
                background-color: #e2e8f0;
                border-color: #94a3b8;
            }
            
            QTableWidget QPushButton:pressed {
                background-color: #cbd5e1;
            }
            
            /* Edit Button */
            QPushButton#editBtn {
                background-color: #dbeafe;
                color: #0369a1;
                border-color: #7dd3fc;
            }
            QPushButton#editBtn:hover {
                background-color: #bfdbfe;
            }
            
            /* Delete Button */
            QPushButton#deleteBtn {
                background-color: #fee2e2;
                color: #dc2626;
                border-color: #fca5a5;
            }
            QPushButton#deleteBtn:hover {
                background-color: #fecaca;
            }
            
            /* Test Button */
            QPushButton#testBtn {
                background-color: #fef3c7;
                color: #d97706;
                border-color: #fcd34d;
            }
            QPushButton#testBtn:hover {
                background-color: #fde68a;
            }
            
            /* Clone Button */
            QPushButton#cloneBtn {
                background-color: #e0e7ff;
                color: #4f46e5;
                border-color: #a5b4fc;
            }
            QPushButton#cloneBtn:hover {
                background-color: #c7d2fe;
            }
            
            /* Menu Bar */
            QMenuBar {
                background-color: white;
                border-bottom: 1px solid #e2e8f0;
                padding: 4px;
            }
            
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                color: #475569;
                font-size: 13px;
            }
            
            QMenuBar::item:selected {
                background-color: #f1f5f9;
                color: #0f172a;
                border-radius: 4px;
            }
            
            QMenu {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 4px;
            }
            
            QMenu::item {
                padding: 8px 24px;
                color: #475569;
                font-size: 13px;
            }
            
            QMenu::item:selected {
                background-color: #dbeafe;
                color: #0369a1;
                border-radius: 4px;
            }
        """
        self.setStyleSheet(APP_STYLE)
        
        # Create Menu Bar
        menu_bar = self.menuBar()
        help_menu = menu_bar.addMenu("Trợ giúp")

        about_action = help_menu.addAction("Giới thiệu")
        about_action.triggered.connect(self.show_about)

        help_action = help_menu.addAction("Hướng dẫn sử dụng")
        help_action.triggered.connect(self.show_help)

        update_action = help_menu.addAction("Kiểm tra cập nhật…")
        update_action.triggered.connect(self.check_updates)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        top_level_layout = QVBoxLayout(central_widget)
        top_level_layout.setContentsMargins(20, 20, 20, 20)
        top_level_layout.setSpacing(20)

        # === HEADER SECTION ===
        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_widget.setFixedHeight(100)
        
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(25, 15, 25, 15)
        header_layout.setSpacing(5)
        
        title = QLabel("🎯 Zoom Auto Scheduler")
        title.setObjectName("titleMain")
        
        subtitle = QLabel("Quản lý lịch họp Zoom thông minh và tự động")
        subtitle.setObjectName("subtitleMain")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addStretch()
        
        top_level_layout.addWidget(header_widget)

        # Main content area
        content_layout = QHBoxLayout()
        
        # Bảng lịch (bên trái)
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Bật/Tắt", "Giờ", "Tên phòng Zoom", "Meeting ID", "Link Zoom"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        content_layout.addWidget(self.table, 3) # Table takes 3/5 space

        # Khung chi tiết (bên phải)
        self.create_detail_pane()
        content_layout.addWidget(self.detail_pane, 2) # Detail pane takes 2/5 space
        
        top_level_layout.addLayout(content_layout)
        
        # Button layout
        button_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Thêm lịch")
        add_btn.setObjectName("addBtn")
        add_btn.setToolTip("Thêm lịch Zoom mới")
        add_btn.clicked.connect(self.add_schedule)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(add_btn)
        button_layout.addStretch()
        top_level_layout.addLayout(button_layout)
        
        # Status
        self.status_label = QLabel("✓ Ứng dụng đang chạy...")
        self.status_label.setObjectName("status")
        top_level_layout.addWidget(self.status_label)
        
        # Connect signals
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.itemDoubleClicked.connect(self.handle_double_click)
        
        # Kiểm tra cập nhật nền (không chặn UI)
        try:
            updater.maybe_check_on_startup(self)
        except Exception as _e:
            pass

    def init_tray(self):
        """Khởi tạo icon khay + menu nhanh."""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        icon = QIcon(str(Path(__file__).parent / "app.ico"))
        self.tray_icon = QSystemTrayIcon(icon, self)

        tray_menu = QMenu(self)

        show_action = QAction("Mở cửa sổ", self)
        show_action.triggered.connect(self.restore_from_tray)
        tray_menu.addAction(show_action)

        update_action = QAction("Kiểm tra cập nhật…", self)
        update_action.triggered.connect(self.check_updates)
        tray_menu.addAction(update_action)

        exit_action = QAction("Thoát", self)
        exit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip(self.build_tray_tooltip())
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
        self.show_tray_notification("Zoom Auto Scheduler", "Đang chạy nền và sẵn sàng mở Zoom.")

    def on_tray_activated(self, reason):
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, QSystemTrayIcon.ActivationReason.DoubleClick):
            self.restore_from_tray()

    def restore_from_tray(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def build_tray_tooltip(self):
        jobs = self.scheduler.get_all_jobs()
        enabled = sum(1 for v in jobs.values() if v.get('enabled'))
        total = len(jobs)

        next_info = self.scheduler.get_next_run_info()
        next_text = "Chưa có lịch" if not next_info else ""
        if next_info:
            job_id, dt = next_info
            job_data = jobs.get(job_id, {})
            name = job_data.get('name') or job_data.get('meeting_id') or "Zoom"
            try:
                local_dt = dt.astimezone() if dt.tzinfo else dt
                next_text = f"Lịch gần nhất: {name} @ {local_dt.strftime('%d/%m %H:%M')}"
            except Exception:
                next_text = f"Lịch gần nhất: {name}"

        return f"Zoom Auto Scheduler\nĐang bật: {enabled}/{total}\n{next_text}"

    def update_tray_tooltip(self):
        if self.tray_icon:
            self.tray_icon.setToolTip(self.build_tray_tooltip())

    def show_tray_notification(self, title, message, icon=QSystemTrayIcon.MessageIcon.Information, msecs=5000):
        if self.tray_icon and self.tray_icon.supportsMessages():
            self.tray_icon.showMessage(title, message, icon, msecs)

    def quit_app(self):
        """Đóng hẳn ứng dụng (qua menu khay)."""
        self.exit_requested = True
        self.close()

    def prompt_close_action(self):
        """Hiện hộp thoại khi nhấn X để chọn Ẩn xuống khay hoặc Đóng."""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return "exit"

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Đóng cửa sổ Zoom Auto")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText("""
    <div style='font-size:13px;'><b>Bạn muốn làm gì?</b></div>
    <div style='color:#475569; margin-top:6px;'>Ẩn xuống khay để tiếp tục chạy nền, hoặc đóng hẳn để dừng toàn bộ lịch.</div>
    """)
        msg.setInformativeText("Ẩn xuống khay: Lịch vẫn chạy.  |  Đóng ứng dụng: Dừng mọi lịch đã hẹn.")
        msg.setStyleSheet("""
            QMessageBox { background: #f8fafc; }
            QLabel { color: #0f172a; } 
            QPushButton { padding: 8px 14px; font-weight: 600; }
        """)

        hide_btn = msg.addButton("Ẩn xuống khay (khuyến nghị)", QMessageBox.ButtonRole.AcceptRole)
        exit_btn = msg.addButton("Đóng ứng dụng (dừng lịch)", QMessageBox.ButtonRole.DestructiveRole)

        msg.setDefaultButton(hide_btn)
        msg.exec()

        clicked = msg.clickedButton()
        if clicked == hide_btn:
            return "hide"
        if clicked == exit_btn:
            return "exit"
        return None

    def handle_double_click(self, item):
        """Xử lý double-click để chỉnh sửa"""
        self.edit_selected_schedule()
    
    def add_schedule(self):
        """Thêm lịch mới"""
        dialog = ScheduleDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            if not data['name']:
                 QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Tên phòng Zoom!")
                 return

            if not data['meeting_id'] and not data['zoom_link']:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Meeting ID HOẶC Link Zoom!")
                return
            
            # Thêm vào scheduler
            new_job_id = self.scheduler.add_schedule(
                None, # ID mới sẽ tự tạo
                data['hour'],
                data['minute'],
                data['meeting_id'],
                data['password'],
                True,
                data['name'], # Thêm tên lịch
                recurrence=data['recurrence'],
                zoom_link=data['zoom_link']
            )
            if new_job_id:
                self.save_schedules() # Lưu ngay
                self.refresh_table()
                self.find_and_select_row(new_job_id) # CHỌN lịch vừa thêm
    
    def test_zoom(self):
        """Test mở Zoom"""
        try:
            dialog = TestZoomDialog(self)
            dialog.exec()
        except Exception as e:
            print(f"[ERROR] test_zoom error: {e}")
            import traceback
            traceback.print_exc()
            self.show_message(f"✗ Lỗi: {str(e)}")

    def show_about(self):
        """Hiển thị thông tin giới thiệu"""
        dialog = AboutDialog(self)
        dialog.exec()

    def show_help(self):
        """Hiển thị hướng dẫn sử dụng"""
        dialog = HelpDialog(self)
        dialog.exec()

    def check_updates(self):
        try:
            updater.check_and_update_ui(self)
        except Exception as e:
            QMessageBox.warning(self, "Cập nhật", f"Lỗi kiểm tra cập nhật: {e}")

    def create_detail_pane(self):
        """Tạo khung hiển thị chi tiết bên phải"""
        self.detail_pane = QGroupBox("📋 Chi tiết lịch hẹn")
        self.detail_pane.setStyleSheet("""
            QGroupBox { 
                font-weight: 600;
                font-size: 15px;
                color: #0f172a;
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 12px;
                margin-top: 8px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                background-color: white;
            }
            QLabel#detailLabel {
                font-weight: 600;
                color: #64748b;
                font-size: 12px;
            }
            QLabel#detailValue {
                font-size: 13px;
                color: #1e293b;
                padding: 8px;
                background-color: #f8fafc;
                border-radius: 6px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        detail_layout = QVBoxLayout()
        # Thêm khoảng đệm (trái, trên, phải, dưới) để tạo khoảng trống với tiêu đề
        detail_layout.setContentsMargins(15, 25, 15, 15)
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_layout.setSpacing(10)
        
        self.detail_name = QLabel()
        self.detail_name.setObjectName("detailValue")
        self.detail_name.setWordWrap(True)
        form_layout.addRow(QLabel("Tên:", objectName="detailLabel"), self.detail_name)
        
        self.detail_time = QLabel()
        self.detail_time.setObjectName("detailValue")
        form_layout.addRow(QLabel("Thời gian:", objectName="detailLabel"), self.detail_time)

        self.detail_id = QLabel()
        self.detail_id.setObjectName("detailValue")
        self.detail_id.setWordWrap(True) # Cho phép xuống dòng
        form_layout.addRow(QLabel("Meeting ID:", objectName="detailLabel"), self.detail_id)
        
        self.detail_pass = QLabel()
        self.detail_pass.setObjectName("detailValue")
        form_layout.addRow(QLabel("Mật khẩu:", objectName="detailLabel"), self.detail_pass)

        self.detail_link = QLabel()
        self.detail_link.setWordWrap(True)
        self.detail_link.setOpenExternalLinks(True)
        self.detail_link.setObjectName("detailValue")
        form_layout.addRow(QLabel("Link Zoom:", objectName="detailLabel"), self.detail_link)

        self.detail_recurrence = QLabel()
        self.detail_recurrence.setObjectName("detailValue")
        form_layout.addRow(QLabel("Lặp lại:", objectName="detailLabel"), self.detail_recurrence)
        
        detail_layout.addLayout(form_layout)
        detail_layout.addStretch()
        
        # Nút chức năng với style mới
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        self.edit_button = QPushButton("✏️ Sửa")
        self.edit_button.setObjectName("editBtn")
        self.edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_button.setToolTip("Chỉnh sửa lịch này")
        
        self.duplicate_button = QPushButton("📋 Nhân bản")
        self.duplicate_button.setObjectName("cloneBtn")
        self.duplicate_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.duplicate_button.setToolTip("Tạo bản sao lịch này")
        
        self.delete_button = QPushButton("🗑️ Xóa")
        self.delete_button.setObjectName("deleteBtn")
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.setToolTip("Xóa lịch này")
        
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.duplicate_button)
        button_layout.addWidget(self.delete_button)
        
        self.edit_button.clicked.connect(self.edit_selected_schedule)
        self.duplicate_button.clicked.connect(self.duplicate_selected_schedule)
        self.delete_button.clicked.connect(self.delete_selected_schedule)
        
        detail_layout.addLayout(button_layout)
        
        self.detail_pane.setLayout(detail_layout)
        self.detail_pane.setVisible(False)

    def on_selection_changed(self):
        """Xử lý khi một dòng được chọn trong bảng"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            self.detail_pane.setVisible(False)
            self.current_selected_job_id = None
            return

        selected_row = self.table.row(selected_items[0])
        item = self.table.item(selected_row, 1) # Column 1 for job id
        
        if not item: return

        job_id = item.data(Qt.ItemDataRole.UserRole)
        self.current_selected_job_id = job_id
        
        jobs = self.scheduler.get_all_jobs()
        job_data = jobs.get(job_id)
        
        if job_data:
            self.update_detail_pane(job_data)
            self.detail_pane.setVisible(True)

    def update_detail_pane(self, job_data):
        """Cập nhật thông tin trong khung chi tiết"""
        self.detail_name.setText(job_data.get('name', 'N/A'))
        
        hour, minute = job_data.get('hour', 0), job_data.get('minute', 0)
        self.detail_time.setText(f"{hour:02d}:{minute:02d}")
        
        meeting_id_raw = job_data.get('meeting_id')
        self.detail_id.setText(format_meeting_id(meeting_id_raw) if meeting_id_raw else "Không có")
        self.detail_pass.setText(job_data.get('password') or "Không có")
        
        link = job_data.get('zoom_link')
        if link:
            MAX_LEN = 50 
            display_link = link
            if len(link) > MAX_LEN:
                display_link = link[:MAX_LEN] + "..."
            self.detail_link.setText(f"<a href='{link}'>{display_link}</a>")
        else:
            self.detail_link.setText("Không có")

        rec = job_data.get('recurrence', {})
        rec_type = rec.get('type', 'daily')
        details = rec.get('details', {})
        
        display_str = "Hàng ngày"
        if rec_type == 'once':
            dt = datetime.fromisoformat(rec.get('run_date'))
            display_str = f"Một lần vào {dt.strftime('%d/%m/%Y')}"
        elif rec_type == 'weekly':
            days = ", ".join([WEEKDAYS_MAP.get(d, '') for d in details.get('days_of_week', [])])
            display_str = f"Hàng tuần vào các thứ: {days}"
        elif rec_type == 'weekdays':
            display_str = "Các ngày trong tuần (T2-T6)"
        elif rec_type == 'custom':
            unit = details.get('unit', '')
            interval = details.get('interval', 1)
            if unit == 'tuần':
                days = ", ".join([WEEKDAYS_MAP.get(d, '') for d in details.get('days_of_week', [])])
                display_str = f"Mỗi {interval} tuần vào: {days}"
            else:
                display_str = f"Mỗi {interval} {unit}"
        
        self.detail_recurrence.setText(display_str)

    def edit_selected_schedule(self):
        """Chỉnh sửa lịch đã chọn"""
        if not self.current_selected_job_id: return
        
        job_id = self.current_selected_job_id  # Lưu job_id vào biến tạm
        job_data = self.scheduler.get_all_jobs().get(job_id)
        if not job_data: return
        
        dialog = ScheduleDialog(self)
        dialog.set_data(job_data)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            self.scheduler.add_schedule(
                job_id,
                new_data['hour'], new_data['minute'],
                new_data['meeting_id'], new_data['password'],
                job_data.get('enabled', True),
                new_data['name'],
                recurrence=new_data['recurrence'],
                zoom_link=new_data['zoom_link']
            )
            self.save_schedules()
            self.refresh_table()
            self.find_and_select_row(job_id) # CHỌN lịch vừa chỉnh sửa

    def delete_selected_schedule(self):
        """Xóa lịch đã chọn"""
        if not self.current_selected_job_id: return
        
        job_data = self.scheduler.get_all_jobs().get(self.current_selected_job_id)
        if not job_data: return

        reply = QMessageBox.question(self, 'Xác nhận xóa', 
                                     f"Bạn có chắc muốn xóa lịch '{job_data.get('name')}' không?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.scheduler.remove_schedule(self.current_selected_job_id):
                self.save_schedules()
                self.refresh_table()
                self.detail_pane.setVisible(False)
                self.current_selected_job_id = None
                self.show_message("✓ Đã xóa lịch thành công")

    def duplicate_selected_schedule(self):
        """Nhân bản lịch đã chọn"""
        if not self.current_selected_job_id: return
        
        job_data = self.scheduler.get_all_jobs().get(self.current_selected_job_id)
        if not job_data: return
        
        new_name = f"{job_data.get('name', '')} (Bản sao)"
        
        new_job_id = self.scheduler.add_schedule(
            None, # ID mới
            job_data['hour'], job_data['minute'],
            job_data['meeting_id'], job_data['password'],
            job_data.get('enabled', True),
            new_name,
            recurrence=job_data.get('recurrence'),
            zoom_link=job_data.get('zoom_link')
        )
        if new_job_id:
            self.save_schedules()
            self.refresh_table()
            self.find_and_select_row(new_job_id)  # Chọn lịch vừa nhân bản
            self.current_selected_job_id = new_job_id  # Cập nhật current_selected_job_id
            self.edit_selected_schedule()  # Mở màn hình chỉnh sửa ngay

    def find_and_select_row(self, job_id):
        """Tìm và chọn dòng trong bảng dựa trên job_id"""
        if not job_id: return
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)  # job_id lưu ở cột 1
            if item and item.data(Qt.ItemDataRole.UserRole) == job_id:
                self.table.selectRow(row)
                self.table.scrollToItem(item, QTableWidget.ScrollHint.PositionAtCenter)
                break

    def refresh_table(self):
        """Cập nhật bảng"""
        self.table.setRowCount(0)
        jobs = self.scheduler.get_all_jobs()
        
        # Sắp xếp công việc theo giờ và phút
        sorted_jobs = sorted(jobs.items(), key=lambda item: (item[1]['hour'], item[1]['minute']))

        for idx, (job_id, job_data) in enumerate(sorted_jobs):
            self.table.insertRow(idx)

            # --- Cột 0: Bật/Tắt ---
            toggle_switch = QCheckBox()
            toggle_switch.setChecked(job_data.get('enabled', False))
            toggle_switch.setProperty("job_id", job_id)
            toggle_switch.toggled.connect(
                lambda checked, jid=job_id, row=idx: self.on_toggle_schedule(jid, checked, row)
            )
            
            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)
            layout.addWidget(toggle_switch)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0,0,0,0)
            self.table.setCellWidget(idx, 0, cell_widget)
            
            # --- Cột 1: Giờ ---
            rec = job_data.get('recurrence', {})
            rec_type = rec.get('type', 'daily')
            hour, minute = job_data.get('hour', 0), job_data.get('minute', 0)
            time_str = f"{hour:02d}:{minute:02d}"
            
            display_str = time_str
            if rec_type == 'once':
                run_date = rec.get('run_date')
                if run_date:
                    try:
                        dt = datetime.fromisoformat(run_date)
                        display_str = dt.strftime("%d/%m %H:%M")
                    except: pass
            
            item_time = QTableWidgetItem(display_str)
            item_time.setData(Qt.ItemDataRole.UserRole, job_id)
            self.table.setItem(idx, 1, item_time)
            
            # --- Cột 2: Tên phòng Zoom ---
            self.table.setItem(idx, 2, QTableWidgetItem(job_data.get('name', '')))
            
            # --- Cột 3: Meeting ID ---
            meeting_id = job_data.get('meeting_id', '')
            self.table.setItem(idx, 3, QTableWidgetItem(format_meeting_id(meeting_id)))

            # --- Cột 4: Link Zoom ---
            self.table.setItem(idx, 4, QTableWidgetItem(job_data.get('zoom_link', '')))
        
        self.table.resizeRowsToContents()
        self.update_tray_tooltip()

    def on_toggle_schedule(self, job_id, is_enabled, row):
        """Xử lý khi công tắc bật/tắt được gạt"""
        if self.scheduler.toggle_schedule(job_id, is_enabled):
            self.save_schedules()
            self.table.selectRow(row)
            # Không cần refresh toàn bộ bảng, chỉ cần cập nhật trạng thái
            status = "bật" if is_enabled else "tắt"
            self.show_message(f"✓ Đã {status} lịch")
            self.update_tray_tooltip()
    
    def save_schedules(self):
        """Lưu lịch vào file JSON"""
        try:
            with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.scheduler.get_all_jobs(), f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.show_message(f"✗ Lỗi khi lưu: {str(e)}")
            
    def load_schedules(self):
        """Tải lịch từ file JSON"""
        if not SCHEDULE_FILE.exists():
            return
            
        try:
            with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
                schedules = json.load(f)
                for job_id, data in schedules.items():
                    self.scheduler.add_schedule(
                        job_id,
                        data['hour'],
                        data['minute'],
                        data.get('meeting_id', ''),
                        data.get('password', ''),
                        data.get('enabled', True),
                        data.get('name', ''),
                        recurrence=data.get('recurrence'),
                        zoom_link=data.get('zoom_link', '')
                    )
        except json.JSONDecodeError:
            self.show_message(f"✗ Lỗi: Tệp zoom_schedule.json bị hỏng.")
            # (Tùy chọn) Backup file hỏng
            try:
                os.rename(SCHEDULE_FILE, f"{SCHEDULE_FILE}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak")
                self.show_message(f"✗ Lỗi: zoom_schedule.json bị hỏng. Đã tạo file backup.")
            except Exception as e:
                self.show_message(f"✗ Lỗi nghiêm trọng với file schedule: {e}")
        except Exception as e:
            self.show_message(f"✗ Lỗi khi tải: {str(e)}")
            
    def show_message(self, message):
        """Hiển thị thông báo trên thanh trạng thái"""
        self.status_label.setText(message)
        
    def closeEvent(self, event):
        """Đóng cửa sổ: hỏi người dùng Ẩn xuống khay hoặc Đóng hẳn."""
        if not self.exit_requested:
            choice = self.prompt_close_action()
            if choice == "hide":
                event.ignore()
                self.hide()
                self.show_message("Ứng dụng đang chạy ngầm ở khay hệ thống")
                self.show_tray_notification("Zoom Auto Scheduler", "Ứng dụng đang chạy nền tại khay.")
                return
            if choice != "exit":
                event.ignore()
                return

        # Lưu lịch trước khi đóng
        self.save_schedules()
        self.scheduler.stop()
        super().closeEvent(event)
    
def main():
    app = QApplication(sys.argv)
    window = ZoomAutoApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
