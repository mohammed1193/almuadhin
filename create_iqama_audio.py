"""
إنشاء ملف صوت إقامة حقيقي
يستخدم مكتبة gTTS لتحويل النص إلى كلام
"""

import os
from pathlib import Path

def create_iqama_audio():
    """
    ينشئ ملف صوت إقامة باستخدام Google Text-to-Speech
    """
    print("=" * 60)
    print("🕌 إنشاء ملف صوت الإقامة")
    print("=" * 60)
    print()
    
    sounds_dir = Path(__file__).parent / "resources" / "sounds"
    sounds_dir.mkdir(parents=True, exist_ok=True)
    
    iqama_file = sounds_dir / "default_iqama.mp3"
    
    # التحقق من وجود الملف
    if iqama_file.exists() and iqama_file.stat().st_size > 10000:
        print(f"✓ ملف الإقامة موجود بالفعل: {iqama_file}")
        size_kb = iqama_file.stat().st_size / 1024
        print(f"  الحجم: {size_kb:.1f} KB")
        print()
        return True
    
    try:
        print("جاري تثبيت مكتبة gTTS...")
        os.system("pip install gTTS -q")
        print("✓ تم تثبيت المكتبة")
        print()
        
        from gtts import gTTS
        
        print("جاري إنشاء ملف صوت الإقامة...")
        
        # نص الإقامة
        iqama_text = """
        الله أكبر، الله أكبر
        أشهد أن لا إله إلا الله
        أشهد أن محمداً رسول الله
        حي على الصلاة
        حي على الفلاح
        قد قامت الصلاة، قد قامت الصلاة
        الله أكبر، الله أكبر
        لا إله إلا الله
        """
        
        # إنشاء الصوت
        tts = gTTS(text=iqama_text, lang='ar', slow=True)
        tts.save(str(iqama_file))
        
        print(f"✓ تم إنشاء ملف الإقامة بنجاح!")
        print(f"  المسار: {iqama_file}")
        size_kb = iqama_file.stat().st_size / 1024
        print(f"  الحجم: {size_kb:.1f} KB")
        print()
        
        print("=" * 60)
        print("✅ تم الإنشاء بنجاح!")
        print("=" * 60)
        print()
        print("يمكنك الآن:")
        print("1. تشغيل التطبيق")
        print("2. الذهاب للإعدادات > الأذان")
        print("3. تفعيل الإقامة")
        print("4. تجربة الصوت")
        print()
        
        return True
        
    except ImportError:
        print("✗ فشل تثبيت مكتبة gTTS")
        print()
        print("الحل البديل:")
        print("1. حمّل ملف إقامة MP3 من الإنترنت")
        print("2. سمّه: default_iqama.mp3")
        print("3. ضعه في:")
        print(f"   {sounds_dir}")
        print()
        print("مصادر مقترحة:")
        print("- https://archive.org/details/iqama-audio")
        print("- YouTube: ابحث 'الإقامة صوت'")
        print()
        return False
        
    except Exception as e:
        print(f"✗ خطأ: {e}")
        print()
        print("الحل البديل:")
        print("حمّل ملف إقامة MP3 يدوياً وضعه في:")
        print(f"  {sounds_dir}/default_iqama.mp3")
        print()
        return False

def create_iqama_with_pydub():
    """
    طريقة بديلة: إنشاء صوت إقامة باستخدام pydub
    """
    print("=" * 60)
    print("🕌 إنشاء ملف صوت الإقامة (طريقة بديلة)")
    print("=" * 60)
    print()
    
    sounds_dir = Path(__file__).parent / "resources" / "sounds"
    sounds_dir.mkdir(parents=True, exist_ok=True)
    
    iqama_file = sounds_dir / "default_iqama.mp3"
    
    try:
        print("جاري تثبيت المكتبات المطلوبة...")
        os.system("pip install pydub -q")
        os.system("pip install pyttsx3 -q")
        print("✓ تم تثبيت المكتبات")
        print()
        
        import pyttsx3
        
        print("جاري إنشاء ملف صوت الإقامة...")
        
        # إنشاء محرك النطق
        engine = pyttsx3.init()
        
        # ضبط الإعدادات
        engine.setProperty('rate', 120)  # سرعة بطيئة
        engine.setProperty('volume', 1.0)
        
        # نص الإقامة
        iqama_text = """
        الله أكبر، الله أكبر.
        أشهد أن لا إله إلا الله.
        أشهد أن محمداً رسول الله.
        حي على الصلاة.
        حي على الفلاح.
        قد قامت الصلاة، قد قامت الصلاة.
        الله أكبر، الله أكبر.
        لا إله إلا الله.
        """
        
        # حفظ كملف WAV أولاً
        temp_wav = sounds_dir / "temp_iqama.wav"
        engine.save_to_file(iqama_text, str(temp_wav))
        engine.runAndWait()
        
        print(f"✓ تم إنشاء ملف الإقامة!")
        print(f"  المسار: {temp_wav}")
        print()
        
        # تحويل إلى MP3 إذا كان ممكناً
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_wav(str(temp_wav))
            audio.export(str(iqama_file), format="mp3")
            temp_wav.unlink()  # حذف الملف المؤقت
            print(f"✓ تم تحويل الملف إلى MP3")
            print(f"  المسار: {iqama_file}")
        except:
            # إذا فشل التحويل، استخدم WAV
            iqama_file = sounds_dir / "default_iqama.wav"
            temp_wav.rename(iqama_file)
            print(f"✓ تم حفظ الملف بصيغة WAV")
            print(f"  المسار: {iqama_file}")
        
        size_kb = iqama_file.stat().st_size / 1024
        print(f"  الحجم: {size_kb:.1f} KB")
        print()
        
        print("=" * 60)
        print("✅ تم الإنشاء بنجاح!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ: {e}")
        print()
        return False

if __name__ == "__main__":
    try:
        print("اختر الطريقة:")
        print("1. استخدام Google Text-to-Speech (يحتاج إنترنت)")
        print("2. استخدام pyttsx3 (لا يحتاج إنترنت)")
        print()
        
        choice = input("اختر (1 أو 2) أو اضغط Enter للطريقة الأولى: ").strip()
        print()
        
        if choice == "2":
            success = create_iqama_with_pydub()
        else:
            success = create_iqama_audio()
        
        if not success:
            print("\nجاري المحاولة بالطريقة البديلة...")
            create_iqama_with_pydub()
        
        print()
        input("اضغط Enter للإغلاق...")
        
    except KeyboardInterrupt:
        print("\n\nتم الإلغاء.")
    except Exception as e:
        print(f"\nخطأ: {e}")
        import traceback
        traceback.print_exc()
        input("\nاضغط Enter للإغلاق...")
