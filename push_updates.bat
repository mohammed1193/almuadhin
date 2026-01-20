@echo off
chcp 65001 >nul
echo ========================================
echo رفع التحديثات على GitHub
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] إضافة الملفات الجديدة...
git add .

echo [2/4] إنشاء commit...
git commit -m "Complete store readiness - Icons optimized and guides updated"

echo [3/4] رفع على GitHub...
git push

if errorlevel 1 (
    echo.
    echo ❌ فشل الرفع!
    echo.
    echo قد تحتاج إلى:
    echo 1. تسجيل الدخول: git config credential.helper store
    echo 2. إدخال Username: mohammed1193
    echo 3. إدخال Password: استخدم Personal Access Token
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ تم رفع التحديثات بنجاح!
echo ========================================
echo.
echo يمكنك الآن زيارة:
echo https://github.com/mohammed1193/almuadhin
echo.
pause
