"""
سكريبت لبناء ملف EXE من التطبيق
"""

import PyInstaller.__main__
from pathlib import Path
import shutil

def build_exe():
    """
    يبني ملف EXE للتطبيق
    """
    print("=" * 60)
    print("🔨 بناء ملف EXE للتطبيق")
    print("=" * 60)
    print()
    
    # المسارات
    project_root = Path(__file__).parent
    src_dir = project_root / "src"
    main_file = src_dir / "main.py"
    icon_file = project_root / "resources" / "icons" / "app_icon.ico"
    
    # التحقق من وجود الملفات
    if not main_file.exists():
        print(f"✗ خطأ: ملف main.py غير موجود في {main_file}")
        return False
    
    if not icon_file.exists():
        print(f"⚠️ تحذير: ملف الأيقونة غير موجود في {icon_file}")
        print("  سيتم البناء بدون أيقونة")
        icon_file = None
    
    print("جاري بناء ملف EXE...")
    print()
    
    # إعدادات PyInstaller
    args = [
        str(main_file),
        '--name=المؤذن',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        f'--distpath={project_root / "dist"}',
        f'--workpath={project_root / "build"}',
        f'--specpath={project_root}',
        f'--paths={src_dir}',
        '--version-file=version_info.txt',
    ]
    
    # إضافة الأيقونة إذا كانت موجودة
    if icon_file:
        args.append(f'--icon={icon_file}')
    
    # إضافة الموارد
    resources_dir = project_root / "resources"
    if resources_dir.exists():
        args.append(f'--add-data={resources_dir};resources')
    
    # إضافة المكتبات المخفية
    hidden_imports = [
        'pygame',
        'PyQt6',
        'requests',
        'geocoder',
        'pytz',
        'ui',
        'ui.main_window',
        'ui.settings_window',
        'ui.adhan_window',
        'ui.tray_icon',
        'core',
        'core.api_client',
        'core.prayer_times',
        'core.scheduler',
        'core.audio_player',
        'core.notifier',
        'utils',
        'utils.config',
        'utils.location',
        'utils.startup',
        'utils.theme_manager',
        'utils.font_loader',
        'utils.saudi_cities',
    ]
    
    for module in hidden_imports:
        args.append(f'--hidden-import={module}')
    
    try:
        # تشغيل PyInstaller
        PyInstaller.__main__.run(args)
        
        print()
        print("=" * 60)
        print("✓ تم بناء ملف EXE بنجاح!")
        print("=" * 60)
        print()
        
        exe_path = project_root / "dist" / "المؤذن.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 ملف EXE:")
            print(f"   المسار: {exe_path}")
            print(f"   الحجم: {size_mb:.1f} MB")
            print()
            print("يمكنك الآن:")
            print("  1. تشغيل الملف مباشرة")
            print("  2. نسخه إلى أي مكان")
            print("  3. إنشاء اختصار على سطح المكتب")
            print()
            return True
        else:
            print("✗ خطأ: لم يتم إنشاء ملف EXE")
            return False
            
    except Exception as e:
        print(f"✗ خطأ في البناء: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        build_exe()
        input("\nاضغط Enter للإغلاق...")
    except Exception as e:
        print(f"\nخطأ: {e}")
        import traceback
        traceback.print_exc()
        input("\nاضغط Enter للإغلاق...")
