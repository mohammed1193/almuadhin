@echo off
chcp 65001 > nul
title بناء تطبيق المؤذن

echo ═══════════════════════════════════════════════════════════
echo 🔨 بناء تطبيق المؤذن
echo ═══════════════════════════════════════════════════════════
echo.

echo الخطوة 1: التحقق من PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ✗ PyInstaller غير مثبت
    echo جاري التثبيت...
    pip install pyinstaller
    echo.
)

echo الخطوة 2: إنشاء الأيقونة...
python create_icon.py
echo.

echo الخطوة 3: بناء ملف EXE...
python build_exe.py

echo.
echo ═══════════════════════════════════════════════════════════
echo ✓ اكتمل!
echo ═══════════════════════════════════════════════════════════
echo.
echo ملف EXE موجود في: dist\المؤذن.exe
echo.
pause
