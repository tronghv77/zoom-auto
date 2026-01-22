@echo off
REM Chạy Zoom Auto Scheduler bằng Python
cd /d %~dp0
call .venv\Scripts\activate.bat
python main.py
pause
