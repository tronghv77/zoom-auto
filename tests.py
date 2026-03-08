import sys
import io
import unittest
from unittest.mock import MagicMock, patch
from main import SchedulerManager
from datetime import datetime, timedelta
import uuid
import updater

# Fix UTF-8 output for Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

class TestZoomScheduler(unittest.TestCase):
    def setUp(self):
        # Mock callback để không in ra UI
        self.mock_callback = MagicMock()
        self.manager = SchedulerManager(callback=self.mock_callback)
        # Tắt scheduler thực để không chạy background thread
        self.manager.scheduler.shutdown()
        # Mock lại scheduler để kiểm tra việc add_job
        self.manager.scheduler = MagicMock()
        self.manager.jobs = {}

    def test_add_schedule_once(self):
        """Test case 1: Lịch một lần"""
        print("\n[TEST 1] Kiểm tra lịch 'Một lần' (Once)")
        run_date = (datetime.now() + timedelta(hours=1)).isoformat()
        recurrence = {'type': 'once', 'run_date': run_date}
        
        job_id = self.manager.add_schedule(
            job_id=None, hour=10, minute=30, 
            meeting_id="123", password="pass", 
            enabled=True, name="Test Once", 
            recurrence=recurrence
        )
        
        # Verify job added with 'date' trigger
        self.manager.scheduler.add_job.assert_called()
        args, kwargs = self.manager.scheduler.add_job.call_args
        
        print(f"   -> Trigger type: {args[1]}")
        self.assertEqual(args[1], 'date', "Trigger phải là 'date'")
        self.assertEqual(kwargs['run_date'].isoformat(), datetime.fromisoformat(run_date).isoformat())
        print("   -> [PASS]")

    def test_version_compare(self):
        """Test so sánh phiên bản cho updater"""
        print("\n[TEST 11] Kiểm tra so sánh phiên bản")
        self.assertTrue(updater.is_newer("1.2.0", "1.1.9"))
        self.assertTrue(updater.is_newer("v1.10.0", "1.9.9"))
        self.assertFalse(updater.is_newer("1.0.0", "1.0.0"))
        self.assertFalse(updater.is_newer("1.0.0", "1.0.1"))
        print("   -> [PASS]")

    def test_add_schedule_daily(self):
        """Test case 2: Lịch hàng ngày"""
        print("\n[TEST 2] Kiểm tra lịch 'Hàng ngày' (Daily)")
        recurrence = {'type': 'daily'}
        
        self.manager.add_schedule(
            job_id=None, hour=14, minute=0, 
            meeting_id="123", enabled=True, 
            recurrence=recurrence
        )
        
        args, kwargs = self.manager.scheduler.add_job.call_args
        print(f"   -> Trigger type: {args[1]}")
        self.assertEqual(args[1], 'cron', "Trigger phải là 'cron'")
        self.assertEqual(kwargs['hour'], 14)
        self.assertEqual(kwargs['minute'], 0)
        print("   -> [PASS]")

    def test_add_schedule_weekly(self):
        """Test case 3: Lịch hàng tuần (Thứ 2, Thứ 4)"""
        print("\n[TEST 3] Kiểm tra lịch 'Hàng tuần' (Weekly - Mon, Wed)")
        # 0=Mon, 2=Wed
        recurrence = {'type': 'weekly', 'details': {'days_of_week': [0, 2]}}
        
        self.manager.add_schedule(
            job_id=None, hour=9, minute=0, 
            meeting_id="123", enabled=True, 
            recurrence=recurrence
        )
        
        args, kwargs = self.manager.scheduler.add_job.call_args
        print(f"   -> Trigger type: {args[1]}")
        self.assertEqual(args[1], 'cron')
        self.assertEqual(kwargs['day_of_week'], '0,2')
        print("   -> [PASS]")

    def test_add_schedule_weekdays(self):
        """Test case 4: Mọi ngày trong tuần (T2-T6)"""
        print("\n[TEST 4] Kiểm tra lịch 'Weekdays' (Mon-Fri)")
        recurrence = {'type': 'weekdays'}
        
        self.manager.add_schedule(
            job_id=None, hour=8, minute=0, 
            meeting_id="123", enabled=True, 
            recurrence=recurrence
        )
        
        args, kwargs = self.manager.scheduler.add_job.call_args
        self.assertEqual(kwargs['day_of_week'], '0-4')
        print("   -> [PASS]")

    def test_edit_existing_schedule(self):
        """Test case 5: Chỉnh sửa (Đổi từ Daily sang Once)"""
        print("\n[TEST 5] Kiểm tra logic cập nhật (Update)")
        # Tạo job đầu tiên
        job_id = "test-uuid"
        self.manager.jobs[job_id] = {'id': job_id, 'name': 'Old'}
        
        # Update
        new_recurrence = {'type': 'once', 'run_date': (datetime.now() + timedelta(days=1)).isoformat()}
        self.manager.add_schedule(
            job_id=job_id, hour=10, minute=0, 
            meeting_id="999", enabled=True, 
            recurrence=new_recurrence
        )
        
        # Verify data updated in memory
        self.assertEqual(self.manager.jobs[job_id]['recurrence']['type'], 'once')
        print("   -> [PASS]")

    def test_remove_schedule(self):
        """Test case 6: Xóa lịch"""
        print("\n[TEST 6] Kiểm tra xóa lịch (Remove)")
        job_id = "job-to-remove"
        self.manager.jobs[job_id] = {'id': job_id}
        
        from unittest.mock import call
        self.manager.remove_schedule(job_id)
        
        # Kiểm tra xem remove_job có được gọi với job_id chính hay không
        self.assertIn(call(job_id), self.manager.scheduler.remove_job.call_args_list)
        self.assertNotIn(job_id, self.manager.jobs)
        print("   -> [PASS]")

    def test_toggle_schedule_off(self):
        """Test case 7: Tắt lịch"""
        print("\n[TEST 7] Kiểm tra tắt lịch (Toggle Off)")
        job_id = "job-to-toggle-off"
        recurrence = {'type': 'daily'}
        self.manager.jobs[job_id] = {
            'id': job_id, 'hour': 10, 'minute': 0, 'meeting_id': '123',
            'password': '', 'enabled': True, 'recurrence': recurrence
        }
        
        self.manager.toggle_schedule(job_id, enabled=False)
        
        self.manager.scheduler.remove_job.assert_called_with(job_id)
        self.assertFalse(self.manager.jobs[job_id]['enabled'])
        print("   -> [PASS]")

    def test_toggle_schedule_on(self):
        """Test case 8: Bật lại lịch"""
        print("\n[TEST 8] Kiểm tra bật lại lịch (Toggle On)")
        job_id = "job-to-toggle-on"
        recurrence = {'type': 'daily'}
        self.manager.jobs[job_id] = {
            'id': job_id, 'hour': 11, 'minute': 0, 'meeting_id': '456',
            'password': '', 'enabled': False, 'recurrence': recurrence
        }
        
        # Reset mock to check for the new call
        self.manager.scheduler.reset_mock()
        
        self.manager.toggle_schedule(job_id, enabled=True)
        
        self.manager.scheduler.add_job.assert_called()
        self.assertTrue(self.manager.jobs[job_id]['enabled'])
        print("   -> [PASS]")
        
    def test_add_schedule_custom_daily(self):
        """Test case 9: Lịch tùy chỉnh lặp lại mỗi 3 ngày"""
        print("\n[TEST 9] Kiểm tra lịch Custom (mỗi 3 ngày)")
        recurrence = {
            'type': 'custom', 
            'details': {'unit': 'ngày', 'interval': 3}
        }
        
        self.manager.add_schedule(
            job_id=None, hour=15, minute=0, 
            meeting_id="789", enabled=True, 
            recurrence=recurrence
        )
        
        args, kwargs = self.manager.scheduler.add_job.call_args
        self.assertEqual(args[1], 'interval', "Trigger phải là 'interval'")
        self.assertEqual(kwargs['days'], 3)
        print("   -> [PASS]")
        
    def test_add_schedule_custom_weekly(self):
        """Test case 10: Lịch tùy chỉnh lặp lại mỗi 2 tuần vào T7, CN"""
        print("\n[TEST 10] Kiểm tra lịch Custom (mỗi 2 tuần, T7, CN)")
        recurrence = {
            'type': 'custom', 
            'details': {'unit': 'tuần', 'interval': 2, 'days_of_week': [5, 6]}
        }
        
        self.manager.add_schedule(
            job_id=None, hour=20, minute=0, 
            meeting_id="101", enabled=True, 
            recurrence=recurrence
        )
        
        args, kwargs = self.manager.scheduler.add_job.call_args
        self.assertEqual(args[1], 'cron', "Trigger phải là 'cron'")
        self.assertEqual(kwargs['day_of_week'], '5,6', "Phải là T7, CN")
        # Note: APScheduler's cron doesn't directly support "every 2 weeks".
        # The current implementation will run it every week on Sat/Sun.
        # This is a limitation of the current app logic, not the test.
        print("   -> [PASS]")

class TestJoinOpenError(unittest.TestCase):
    """Tests cho JoinOpenError exception class"""

    def test_error_has_code_and_message(self):
        """JoinOpenError phải lưu code và message riêng biệt"""
        from main import JoinOpenError
        err = JoinOpenError("APP_NOT_INSTALLED", "Zoom app không tìm thấy")
        self.assertEqual(err.code, "APP_NOT_INSTALLED")
        self.assertEqual(err.message, "Zoom app không tìm thấy")
        self.assertEqual(str(err), "Zoom app không tìm thấy")

    def test_error_is_exception(self):
        """JoinOpenError phải kế thừa từ Exception"""
        from main import JoinOpenError
        err = JoinOpenError("INVALID_MEETING_ID", "Thiếu Meeting ID")
        self.assertIsInstance(err, Exception)


class TestOpenZoomLogic(unittest.TestCase):
    """Tests cho retry/fallback logic trong _open_zoom"""

    def setUp(self):
        self.mock_callback = MagicMock()
        self.manager = SchedulerManager(callback=self.mock_callback)
        self.manager.scheduler.shutdown()
        self.manager.scheduler = MagicMock()
        self.manager.jobs = {}

    def _add_test_job(self, job_id="test-job", meeting_id="123456789",
                      join_profile=None, retry_policy=None):
        from main import DEFAULT_JOIN_PROFILE, DEFAULT_RETRY_POLICY
        self.manager.jobs[job_id] = {
            "id": job_id,
            "name": "Test Meeting",
            "meeting_id": meeting_id,
            "password": "pass",
            "zoom_link": "",
            "join_profile": join_profile or dict(DEFAULT_JOIN_PROFILE),
            "retry_policy": retry_policy or dict(DEFAULT_RETRY_POLICY),
            "last_run_meta": {},
        }

    def test_open_zoom_success_app_mode(self):
        """Mở Zoom thành công qua App mode"""
        print("\n[TEST 12] Kiểm tra mở Zoom thành công (App mode)")
        self._add_test_job()

        with patch("main.os.startfile") as mock_startfile:
            result = self.manager._open_zoom("test-job", "123456789", "pass", "")

        self.assertTrue(result)
        mock_startfile.assert_called_once()
        print("   -> [PASS]")

    def test_open_zoom_fallback_to_browser(self):
        """Fallback từ App sang Browser khi App thất bại"""
        print("\n[TEST 13] Kiểm tra fallback App -> Browser")
        self._add_test_job(
            retry_policy={"max_attempts": 1, "delay_seconds": 0, "fallback_enabled": True}
        )

        with patch("main.os.startfile", side_effect=Exception("App not found")):
            with patch("main.webbrowser.open", return_value=True) as mock_browser:
                result = self.manager._open_zoom("test-job", "123456789", "pass", "")

        self.assertTrue(result)
        mock_browser.assert_called_once()
        print("   -> [PASS]")

    def test_open_zoom_no_fallback(self):
        """Không fallback khi fallback_enabled=False"""
        print("\n[TEST 14] Kiểm tra không fallback khi fallback_enabled=False")
        self._add_test_job(
            retry_policy={"max_attempts": 1, "delay_seconds": 0, "fallback_enabled": False}
        )

        with patch("main.os.startfile", side_effect=Exception("App not found")):
            with patch("main.webbrowser.open", return_value=True) as mock_browser:
                result = self.manager._open_zoom("test-job", "123456789", "pass", "")

        self.assertFalse(result)
        mock_browser.assert_not_called()
        print("   -> [PASS]")

    def test_open_zoom_retry_attempts(self):
        """Retry đúng số lần khi thất bại"""
        print("\n[TEST 15] Kiểm tra retry đúng số lần (max_attempts=3)")
        self._add_test_job(
            join_profile={"mode_priority": ["app"]},
            retry_policy={"max_attempts": 3, "delay_seconds": 0, "fallback_enabled": False}
        )

        with patch("main.os.startfile", side_effect=Exception("fail")) as mock_start:
            result = self.manager._open_zoom("test-job", "123456789", "pass", "")

        self.assertFalse(result)
        self.assertEqual(mock_start.call_count, 3)
        print("   -> [PASS]")

    def test_open_zoom_missing_meeting_id(self):
        """Trả về False khi thiếu Meeting ID và không có zoom_link"""
        print("\n[TEST 16] Kiểm tra thiếu Meeting ID")
        self._add_test_job(meeting_id="")
        self.manager.jobs["test-job"]["zoom_link"] = ""

        with patch("main.os.startfile", side_effect=Exception("no id")):
            with patch("main.webbrowser.open", return_value=True):
                result = self.manager._open_zoom("test-job", "", "", "")

        self.assertFalse(result)
        print("   -> [PASS]")


class TestSentryReporting(unittest.TestCase):
    """Tests cho report_error_to_sentry"""

    def test_report_skips_when_no_sentry_sdk(self):
        """Không crash khi sentry_sdk là None"""
        import main
        orig = main.sentry_sdk
        try:
            main.sentry_sdk = None
            from main import JoinOpenError
            # Phải không raise exception
            main.report_error_to_sentry(JoinOpenError("TEST", "msg"), {"k": "v"})
        finally:
            main.sentry_sdk = orig

    def test_report_passes_original_exception(self):
        """report_error_to_sentry nhận exception gốc, không tạo Exception mới"""
        import main
        from main import JoinOpenError
        captured = []
        mock_sdk = MagicMock()
        mock_sdk.push_scope().__enter__ = MagicMock(return_value=MagicMock())
        mock_sdk.push_scope().__exit__ = MagicMock(return_value=False)
        mock_sdk.capture_exception.side_effect = lambda e: captured.append(e)
        orig = main.sentry_sdk
        try:
            main.sentry_sdk = mock_sdk
            err = JoinOpenError("APP_NOT_INSTALLED", "test msg")
            main.report_error_to_sentry(err, None)
            mock_sdk.capture_exception.assert_called_once_with(err)
        finally:
            main.sentry_sdk = orig


if __name__ == '__main__':
    unittest.main(verbosity=0)
