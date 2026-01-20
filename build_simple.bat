@echo off
chcp 65001 > nul
echo ============================================================
echo 🔨 بناء ملف EXE للمؤذن
echo ============================================================
echo.

echo جاري التحقق من PyInstaller...
pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo تثبيت PyInstaller...
    pip install pyinstaller
)

echo.
echo جاري بناء الملف التنفيذي...
echo.

pyinstaller --name="المؤذن" ^
    --onefile ^
    --windowed ^
    --icon="resources\icons\app_icon.ico" ^
    --add-data="resources;resources" ^
    --hidden-import=pygame ^
    --hidden-import=PyQt6 ^
    --hidden-import=requests ^
    --hidden-import=geocoder ^
    --hidden-import=pytz ^
    --clean ^
    --noconfirm ^
    src\main.py

echo.
echo ============================================================
echo ✅ اكتمل البناء!
echo ============================================================
echo.
echo ملف EXE موجود في: dist\المؤذن.exe
echo.
pause
