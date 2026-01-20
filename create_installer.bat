@echo off
chcp 65001 > nul
title إنشاء برنامج تثبيت المؤذن

echo ═══════════════════════════════════════════════════════════
echo 📦 إنشاء برنامج تثبيت المؤذن
echo ═══════════════════════════════════════════════════════════
echo.

echo الخطوة 1: التحقق من وجود ملف EXE...
if not exist "dist\المؤذن.exe" (
    echo ✗ ملف EXE غير موجود!
    echo.
    echo يجب بناء البرنامج أولاً:
    echo   شغّل: build_app.bat
    echo.
    pause
    exit /b 1
)
echo ✓ ملف EXE موجود
echo.

echo الخطوة 2: التحقق من Inno Setup...
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo ✗ Inno Setup غير مثبت!
    echo.
    echo الرجاء تحميل وتثبيت Inno Setup من:
    echo   https://jrsoftware.org/isdl.php
    echo.
    echo بعد التثبيت، شغّل هذا الملف مرة أخرى.
    echo.
    pause
    exit /b 1
)
echo ✓ Inno Setup مثبت
echo.

echo الخطوة 3: بناء برنامج التثبيت...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss

if errorlevel 1 (
    echo.
    echo ✗ فشل إنشاء برنامج التثبيت
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo ✓ تم إنشاء برنامج التثبيت بنجاح!
echo ═══════════════════════════════════════════════════════════
echo.
echo ملف التثبيت موجود في:
echo   installer_output\AlMuadhin_Setup.exe
echo.
echo يمكنك الآن:
echo   1. تشغيل ملف التثبيت
echo   2. توزيعه على أجهزة أخرى
echo   3. مشاركته مع الآخرين
echo.
pause
