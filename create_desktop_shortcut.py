"""
إنشاء اختصار على سطح المكتب
"""

import os
import winshell
from pathlib import Path
from win32com.client import Dispatch

def create_desktop_shortcut():
    """
    ينشئ اختصار للبرنامج على سطح المكتب
    """
    print("=" * 60)
    print("🔗 إنشاء اختصار على سطح المكتب")
    print("=" * 60)
    print()
    
    # المسارات
    project_root = Path(__file__).parent
    exe_path = project_root / "dist" / "المؤذن.exe"
    icon_path = project_root / "resources" / "icons" / "app_icon.ico"
    
    # التحقق من وجود ملف EXE
    if not exe_path.exists():
        print("✗ خطأ: ملف EXE غير موجود")
        print(f"  المسار المتوقع: {exe_path}")
        print()
        print("الرجاء بناء البرنامج أولاً باستخدام:")
        print("  python build_exe.py")
        print("  أو: build_app.bat")
        return False
    
    try:
        # الحصول على مسار سطح المكتب
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "المؤذن.lnk")
        
        # إنشاء الاختصار
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = str(exe_path)
        shortcut.WorkingDirectory = str(exe_path.parent)
        
        # إضافة الأيقونة إذا كانت موجودة
        if icon_path.exists():
            shortcut.IconLocation = str(icon_path)
        
        shortcut.Description = "تطبيق المؤذن - مواقيت الصلاة والأذان"
        shortcut.save()
        
        print("✓ تم إنشاء الاختصار بنجاح!")
        print(f"  المسار: {shortcut_path}")
        print()
        print("يمكنك الآن:")
        print("  - تشغيل البرنامج من سطح المكتب")
        print("  - تثبيت الاختصار في شريط المهام")
        print("  - نقل الاختصار إلى أي مكان")
        print()
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ في إنشاء الاختصار: {e}")
        print()
        print("حل بديل:")
        print("  1. انقر بالزر الأيمن على ملف EXE")
        print(f"     {exe_path}")
        print("  2. اختر 'إرسال إلى' > 'سطح المكتب (إنشاء اختصار)'")
        print()
        return False

if __name__ == "__main__":
    try:
        create_desktop_shortcut()
        input("\nاضغط Enter للإغلاق...")
    except Exception as e:
        print(f"\nخطأ: {e}")
        import traceback
        traceback.print_exc()
        input("\nاضغط Enter للإغلاق...")
