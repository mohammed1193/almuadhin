"""
إنشاء ملف أذان افتراضي بسيط
يستخدم مكتبة pydub لإنشاء نغمة إسلامية
"""

from pydub import AudioSegment
from pydub.generators import Sine
from pathlib import Path
import os

def create_adhan_tone():
    """
    ينشئ نغمة بسيطة تشبه الأذان
    """
    print("=" * 60)
    print("🕌 إنشاء ملف أذان افتراضي")
    print("=" * 60)
    print()
    
    sounds_dir = Path(__file__).parent / "resources" / "sounds"
    sounds_dir.mkdir(parents=True, exist_ok=True)
    
    adhan_file = sounds_dir / "default_adhan.mp3"
    iqama_file = sounds_dir / "default_iqama.mp3"
    
    # التحقق من وجود الملفات
    if adhan_file.exists():
        print(f"✓ ملف الأذان موجود بالفعل: {adhan_file}")
        size_mb = adhan_file.stat().st_size / (1024 * 1024)
        print(f"  الحجم: {size_mb:.2f} MB")
        print()
        return True
    
    try:
        print("جاري إنشاء ملف أذان تجريبي...")
        print()
        
        # إنشاء نغمة إسلامية بسيطة
        # نستخدم تردد 440 Hz (نوتة A) و 523 Hz (نوتة C)
        
        # النغمة الأولى (2 ثانية)
        tone1 = Sine(440).to_audio_segment(duration=2000)
        
        # النغمة الثانية (2 ثانية)
        tone2 = Sine(523).to_audio_segment(duration=2000)
        
        # النغمة الثالثة (2 ثانية)
        tone3 = Sine(392).to_audio_segment(duration=2000)
        
        # دمج النغمات
        adhan_sound = tone1 + tone2 + tone3 + tone1
        
        # تقليل مستوى الصوت قليلاً
        adhan_sound = adhan_sound - 10
        
        # حفظ الملف
        adhan_sound.export(str(adhan_file), format="mp3", bitrate="128k")
        
        print(f"✓ تم إنشاء ملف الأذان بنجاح!")
        print(f"  المسار: {adhan_file}")
        size_mb = adhan_file.stat().st_size / (1024 * 1024)
        print(f"  الحجم: {size_mb:.2f} MB")
        print()
        
        # إنشاء ملف إقامة (نغمة أقصر)
        if not iqama_file.exists():
            print("جاري إنشاء ملف إقامة تجريبي...")
            iqama_sound = tone2 + tone1
            iqama_sound = iqama_sound - 10
            iqama_sound.export(str(iqama_file), format="mp3", bitrate="128k")
            print(f"✓ تم إنشاء ملف الإقامة!")
            print(f"  المسار: {iqama_file}")
            print()
        
        print("=" * 60)
        print("⚠️ ملاحظة مهمة:")
        print("=" * 60)
        print("هذه ملفات تجريبية بسيطة (نغمات فقط)")
        print("للحصول على أذان حقيقي:")
        print()
        print("1. حمّل ملف أذان MP3 من:")
        print("   - https://archive.org/details/adhan-collection")
        print("   - YouTube (ابحث: أذان مكة المكرمة)")
        print()
        print("2. سمّه: default_adhan.mp3")
        print()
        print("3. ضعه في:")
        print(f"   {sounds_dir}")
        print()
        print("4. استبدل الملف الحالي")
        print()
        print("راجع: HOW_TO_ADD_ADHAN_FILES.md للتفاصيل")
        print("=" * 60)
        
        return True
        
    except ImportError:
        print("✗ خطأ: مكتبة pydub غير مثبتة")
        print()
        print("لتثبيتها:")
        print("  pip install pydub")
        print()
        print("أو حمّل ملف أذان يدوياً من:")
        print("  https://archive.org/details/adhan-collection")
        print()
        return False
        
    except Exception as e:
        print(f"✗ خطأ في إنشاء الملف: {e}")
        print()
        print("الحل البديل:")
        print("حمّل ملف أذان MP3 يدوياً:")
        print(f"  ضعه في: {sounds_dir}")
        print(f"  سمّه: default_adhan.mp3")
        print()
        return False

if __name__ == "__main__":
    try:
        create_adhan_tone()
        input("\nاضغط Enter للإغلاق...")
    except Exception as e:
        print(f"\nخطأ: {e}")
        input("\nاضغط Enter للإغلاق...")
