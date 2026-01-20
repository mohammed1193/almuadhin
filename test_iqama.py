"""
تجربة صوت الإقامة
"""

import pygame
from pathlib import Path
import time

def test_iqama():
    print("=" * 60)
    print("🕌 تجربة صوت الإقامة")
    print("=" * 60)
    print()
    
    sounds_dir = Path(__file__).parent / "resources" / "sounds"
    iqama_file = sounds_dir / "default_iqama.mp3"
    
    if not iqama_file.exists():
        print(f"✗ ملف الإقامة غير موجود: {iqama_file}")
        return
    
    print(f"✓ تم العثور على ملف الإقامة")
    size_kb = iqama_file.stat().st_size / 1024
    print(f"  الحجم: {size_kb:.1f} KB")
    print()
    
    try:
        # تهيئة pygame
        pygame.mixer.init()
        
        print("جاري تشغيل صوت الإقامة...")
        print()
        
        # تحميل وتشغيل الصوت
        pygame.mixer.music.load(str(iqama_file))
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()
        
        print("▶️  يتم الآن تشغيل صوت الإقامة...")
        print()
        print("اضغط Ctrl+C للإيقاف")
        print()
        
        # الانتظار حتى ينتهي الصوت
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
        
        print()
        print("✅ انتهى التشغيل!")
        print()
        
    except KeyboardInterrupt:
        print()
        print("⏹️  تم إيقاف التشغيل")
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"✗ خطأ في التشغيل: {e}")
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    test_iqama()
    print()
