@echo off
chcp 65001 > nul

cd src
start /B pythonw main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo حدث خطأ أثناء تشغيل التطبيق!
    echo تأكد من تثبيت المكتبات المطلوبة:
    echo pip install -r requirements.txt
    echo.
    pause
)
