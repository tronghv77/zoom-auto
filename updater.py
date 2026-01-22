import hashlib
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

import requests


def _resource_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).parent


def _app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(os.path.dirname(sys.executable))
    return Path(__file__).parent


def load_config() -> Dict:
    # Prefer config next to app (overridden when user edits deployed file)
    candidates = [
        _app_dir() / "update_config.json",
        _resource_dir() / "update_config.json",
    ]
    for p in candidates:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    return {
        "provider": "github",
        "repo": "owner/repo",
        "asset_regex": r"^ZoomAuto.*\\.exe$",
        "require_sha256": True,
        "check_on_startup": True,
        "check_interval_hours": 24,
    }


def get_current_version() -> str:
    try:
        from version import __version__
        return __version__
    except Exception:
        return "0.0.0"


def _normalize_version(v: str) -> str:
    v = v.strip()
    if v.lower().startswith("v"):
        v = v[1:]
    return v


def is_newer(remote: str, local: str) -> bool:
    """Basic semver-ish compare without extra deps.
    Returns True if remote > local.
    """
    ra = [int(p) if p.isdigit() else 0 for p in _normalize_version(remote).split(".")]
    la = [int(p) if p.isdigit() else 0 for p in _normalize_version(local).split(".")]
    # pad to same length
    n = max(len(ra), len(la))
    ra += [0] * (n - len(ra))
    la += [0] * (n - len(la))
    return ra > la


def _github_latest_release(repo: str) -> Dict:
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"Accept": "application/vnd.github+json"}
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.json()


def _find_asset(assets: list, pattern: str) -> Optional[Dict]:
    rx = re.compile(pattern)
    for a in assets:
        name = a.get("name", "")
        if rx.search(name):
            return a
    return None


def _extract_sha256(release: Dict, asset_name: str) -> Optional[str]:
    # 1) Look for a sibling .sha256 asset
    want = f"{asset_name}.sha256"
    for a in release.get("assets", []):
        if a.get("name") == want:
            url = a.get("browser_download_url")
            if url:
                text = requests.get(url, timeout=20).text.strip()
                # file can be: "<sha256>  <filename>" or just hash
                m = re.search(r"([a-fA-F0-9]{64})", text)
                if m:
                    return m.group(1).lower()

    # 2) Try to parse from release body e.g., "SHA256: <hash>"
    body = release.get("body") or ""
    m = re.search(r"sha256\s*[:=]\s*([a-fA-F0-9]{64})", body, re.IGNORECASE)
    if m:
        return m.group(1).lower()
    return None


def check_latest(config: Dict) -> Optional[Dict]:
    if config.get("provider") != "github":
        return None
    repo = config.get("repo")
    if not repo or repo == "owner/repo":
        return None
    rel = _github_latest_release(repo)
    tag = rel.get("tag_name") or ""
    latest_version = _normalize_version(tag)
    asset_regex = config.get("asset_regex", r"^ZoomAuto.*\\.exe$")
    asset = _find_asset(rel.get("assets", []), asset_regex)
    if not asset:
        return None
    sha256 = _extract_sha256(rel, asset.get("name", ""))
    return {
        "version": latest_version,
        "asset_name": asset.get("name"),
        "download_url": asset.get("browser_download_url"),
        "sha256": sha256,
        "notes": rel.get("body") or "",
    }


def download(url: str, dest: Path, progress_cb: Optional[Callable[[int, int], None]] = None) -> None:
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", 0))
        done = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 128):
                if not chunk:
                    continue
                f.write(chunk)
                done += len(chunk)
                if progress_cb:
                    try:
                        progress_cb(done, total)
                    except Exception:
                        pass


def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _write_apply_batch(current_exe: Path, new_exe: Path) -> Path:
    # Create a temporary .bat to replace the exe after this process exits
    bat = Path(tempfile.gettempdir()) / f"apply_update_{int(time.time())}.bat"
    content = f"""
@echo off
setlocal enableextensions
set CURR="{str(current_exe)}"
set NEW="{str(new_exe)}"
set PID={os.getpid()}

:waitloop
timeout /t 1 /nobreak >nul
tasklist /fi "PID eq %PID%" | find "%PID%" >nul
if %ERRORLEVEL%==0 goto waitloop

copy /y %NEW% %CURR% >nul
if %ERRORLEVEL% NEQ 0 (
  echo Failed to replace file.
  exit /b 1
)

start "" %CURR%
del /q %NEW% >nul 2>&1
start "" cmd /c del /q "%~f0" >nul 2>&1
"""
    with open(bat, "w", encoding="utf-8") as f:
        f.write(content)
    return bat


def apply_update(downloaded_file: Path) -> Tuple[bool, Optional[str]]:
    if not getattr(sys, "frozen", False):
        return False, "Chỉ hỗ trợ tự cập nhật cho bản đóng gói (.exe)."
    current_exe = Path(sys.executable)
    bat = _write_apply_batch(current_exe, downloaded_file)
    try:
        os.startfile(str(bat))  # Launch the batch (non-blocking)
        return True, None
    except Exception as e:
        return False, str(e)


def check_and_update_ui(parent) -> None:
    """Qt-based update flow: check → prompt → download → verify → apply.
    This is UI-bound; import Qt only here.
    """
    from PyQt6.QtWidgets import QMessageBox, QProgressDialog
    from PyQt6.QtCore import Qt

    cfg = load_config()
    if not cfg.get("repo") or cfg.get("repo") == "owner/repo":
        QMessageBox.information(parent, "Cập nhật", "Chưa cấu hình GitHub repo trong update_config.json.")
        return

    current = get_current_version()
    try:
        info = check_latest(cfg)
    except Exception as e:
        QMessageBox.warning(parent, "Cập nhật", f"Không kiểm tra được phiên bản: {e}")
        return

    if not info:
        QMessageBox.information(parent, "Cập nhật", "Không tìm thấy bản phát hành mới.")
        return

    latest = info["version"]
    if not is_newer(latest, current):
        QMessageBox.information(parent, "Cập nhật", f"Bạn đang ở phiên bản mới nhất ({current}).")
        return

    notes = info.get("notes", "")
    reply = QMessageBox.question(
        parent,
        "Có bản cập nhật",
        f"Có phiên bản mới v{latest} (hiện tại v{current}).\nBạn có muốn tải và cập nhật ngay?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.Yes,
    )
    if reply != QMessageBox.StandardButton.Yes:
        return

    # Download
    url = info["download_url"]
    tmp_file = Path(tempfile.gettempdir()) / info["asset_name"]
    progress = QProgressDialog("Đang tải bản cập nhật...", "Hủy", 0, 100, parent)
    progress.setWindowModality(Qt.WindowModality.WindowModal)
    progress.setMinimumDuration(0)

    def on_prog(done: int, total: int) -> None:
        if total > 0:
            progress.setValue(min(100, int(done * 100 / total)))
        else:
            progress.setValue(0)
        if progress.wasCanceled():
            raise RuntimeError("Đã hủy tải về")

    try:
        download(url, tmp_file, on_prog)
        progress.setValue(100)
    except Exception as e:
        progress.cancel()
        QMessageBox.warning(parent, "Cập nhật", f"Tải về thất bại: {e}")
        return

    # Verify sha256 if required
    if cfg.get("require_sha256", True):
        expected = info.get("sha256")
        if not expected:
            QMessageBox.warning(parent, "Cập nhật", "Thiếu SHA256 trong phát hành, không thể xác minh.")
            return
        actual = sha256sum(tmp_file)
        if actual.lower() != expected.lower():
            QMessageBox.critical(parent, "Cập nhật", "Sai checksum SHA256, hủy cập nhật.")
            try:
                tmp_file.unlink(missing_ok=True)
            except Exception:
                pass
            return

    ok, err = apply_update(tmp_file)
    if not ok:
        QMessageBox.critical(parent, "Cập nhật", f"Không thể áp dụng cập nhật: {err}")
        try:
            tmp_file.unlink(missing_ok=True)
        except Exception:
            pass
        return

    # Close app to allow batch to replace and restart
    QMessageBox.information(parent, "Cập nhật", "Ứng dụng sẽ khởi động lại để hoàn tất cập nhật.")
    os._exit(0)


def maybe_check_on_startup(parent) -> None:
    """Schedule a background check on startup if enabled and not too frequent."""
    from PyQt6.QtCore import QTimer
    cfg = load_config()
    if not cfg.get("check_on_startup", True):
        return

    # Simple throttle using a stamp file under app dir
    stamp = _app_dir() / ".update_last_check"
    interval_h = int(cfg.get("check_interval_hours", 24) or 24)
    now = time.time()
    if stamp.exists():
        try:
            last = float(stamp.read_text(encoding="utf-8"))
            if now - last < interval_h * 3600:
                return
        except Exception:
            pass

    def do_check():
        try:
            stamp.write_text(str(now), encoding="utf-8")
        except Exception:
            pass
        # Non-blocking: only notify if newer
        try:
            info = check_latest(load_config())
            if not info:
                return
            if is_newer(info["version"], get_current_version()):
                # soft prompt
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(parent, "Cập nhật", f"Có bản mới v{info['version']}. Vào Trợ giúp → Kiểm tra cập nhật để cập nhật.")
        except Exception:
            pass

    QTimer.singleShot(2000, do_check)
