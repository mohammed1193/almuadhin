@echo off
chcp 65001 > nul
echo ========================================
echo    تثبيت المكتبات المطلوبة
echo ========================================
echo.

python --version
if %ERRORLEVEL% NEQ 0 (
    echo خطأ: Python غير مثبت!
    echo يرجى تثبيت Python 3.8 أو أحدث من:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo جاري تثبيت المكتبات...
echo.

pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo تم تثبيت المكتبات بنجاح!
    echo يمكنك الآن تشغيل التطبيق بالضغط على run.bat
    echo ========================================
) else (
    echo.
    echo حدث خطأ أثناء التثبيت!
)

echo.
pause
