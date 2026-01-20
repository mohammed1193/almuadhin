@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo تعديل أسماء لقطات الشاشة...
echo.

ren "Screenshot 2026-01-20 191916.png" "01_main.png"
ren "Screenshot 2026-01-20 191924.png" "02_adhan.png"
ren "Screenshot 2026-01-20 191932.png" "03_settings.png"
ren "Screenshot 2026-01-20 191937.png" "04_adhan_settings.png"
ren "Screenshot 2026-01-20 191941.png" "05_location.png"
ren "Screenshot 2026-01-20 191945.png" "06_notifications.png"
ren "Screenshot 2026-01-20 191951.png" "07_tray.png"

echo.
echo ✅ تم تعديل الأسماء بنجاح!
echo.
pause
