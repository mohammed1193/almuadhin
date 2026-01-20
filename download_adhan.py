"""
سكريبت لتحميل ملف أذان افتراضي تلقائياً
يحمّل ملف أذان مجاني من Internet Archive
"""

import requests
import os
from pathlib import Path

def download_adhan_file():
    """
    يحمّل ملف أذان افتراضي من مصدر مجاني
    """
    print("=" * 60)
    print("تحميل ملف الأذان الافتراضي...")
    print("=" * 60)
    
    # مسار مجلد الأصوات
    sounds_dir = Path(__file__).parent / "resources" / "sounds"
    sounds_dir.mkdir(parents=True, exist_ok=True)
    
    adhan_file = sounds_dir / "default_adhan.mp3"
    iqama_file = sounds_dir / "default_iqama.mp3"
    
    # التحقق من وجود الملفات
    if adhan_file.exists():
        print(f"✓ ملف الأذان موجود بالفعل: {adhan_file}")
        print(f"  الحجم: {adhan_file.stat().st_size / 1024:.1f} KB")
    else:
        print("✗ ملف الأذان غير موجود")
        print("\nجاري تحميل ملف أذان افتراضي...")
        
        # روابط ملفات أذان مجانية من Internet Archive
        adhan_urls = [
            # أذان قصير (تجريبي)
            "https://archive.org/download/adhan-collection/adhan-makkah-short.mp3",
            # رابط بديل
            "https://ia802707.us.archive.org/9/items/adhan-collection/adhan-makkah.mp3",
        ]
        
        success = False
        for url in adhan_urls:
            try:
                print(f"\nمحاولة التحميل من: {url}")
                response = requests.get(url, timeout=30, stream=True)
                
                if response.status_code == 200:
                    total_size = int(response.headers.get('content-length', 0))
                    
                    with open(adhan_file, 'wb') as f:
                        downloaded = 0
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total_size > 0:
                                    progress = (downloaded / total_size) * 100
                                    print(f"\rالتقدم: {progress:.1f}%", end='')
                    
                    print(f"\n✓ تم تحميل ملف الأذان بنجاح!")
                    print(f"  الحجم: {adhan_file.stat().st_size / 1024:.1f} KB")
                    success = True
                    break
                    
            except Exception as e:
                print(f"✗ فشل التحميل: {e}")
                continue
        
        if not success:
            print("\n" + "=" * 60)
            print("⚠️ لم نتمكن من تحميل ملف الأذان تلقائياً")
            print("=" * 60)
            print("\nالرجاء تحميل ملف أذان يدوياً:")
            print("1. حمّل ملف أذان MP3 من:")
            print("   - https://archive.org/details/adhan-collection")
            print("   - YouTube (حوّله لـ MP3)")
            print("\n2. سمّه: default_adhan.mp3")
            print(f"\n3. ضعه في: {sounds_dir}")
            print("\nراجع ملف: HOW_TO_ADD_ADHAN_FILES.md")
            return False
    
    # ملف الإقامة (اختياري)
    if not iqama_file.exists():
        print(f"\n✗ ملف الإقامة غير موجود (اختياري)")
        print(f"  يمكنك إضافته لاحقاً: {iqama_file}")
    else:
        print(f"\n✓ ملف الإقامة موجود: {iqama_file}")
    
    print("\n" + "=" * 60)
    print("✓ الإعداد مكتمل!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        download_adhan_file()
        input("\nاضغط Enter للإغلاق...")
    except Exception as e:
        print(f"\nخطأ: {e}")
        input("\nاضغط Enter للإغلاق...")
