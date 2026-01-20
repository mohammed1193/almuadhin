"""
إنشاء ملف صوت إقامة حقيقي - تلقائي
"""

import os
import sys
from pathlib import Path

def create_iqama_with_gtts():
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
        return True
    
    try:
        # تثبيت gTTS
        print("جاري تثبيت مكتبة gTTS...")
        os.system(f'"{sys.executable}" -m pip install gTTS -q')
        
        from gtts import gTTS
        
        print("✓ تم تثبيت المكتبة")
        print()
        print("جاري إنشاء ملف صوت الإقامة...")
        
        # نص الإقامة
        iqama_text = "الله أكبر، الله أكبر. أشهد أن لا إله إلا الله. أشهد أن محمداً رسول الله. حي على الصلاة. حي على الفلاح. قد قامت الصلاة، قد قامت الصلاة. الله أكبر، الله أكبر. لا إله إلا الله."
        
        # إنشاء الصوت
        tts = gTTS(text=iqama_text, lang='ar', slow=True)
        tts.save(str(iqama_file))
        
        print(f"✓ تم إنشاء ملف الإقامة بنجاح!")
        print(f"  المسار: {iqama_file}")
        size_kb = iqama_file.stat().st_size / 1024
        print(f"  الحجم: {size_kb:.1f} KB")
        print()
        print("=" * 60)
        print("✅ اكتمل بنجاح!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ في gTTS: {e}")
        return False

def create_iqama_with_pyttsx3():
    """
    طريقة بديلة باستخدام pyttsx3
    """
    print()
    print("جاري المحاولة بالطريقة البديلة (pyttsx3)...")
    print()
    
    sounds_dir = Path(__file__).parent / "resources" / "sounds"
    
    try:
        print("جاري تثبيت pyttsx3...")
        os.system(f'"{sys.executable}" -m pip install pyttsx3 -q')
        
        import pyttsx3
        
        print("✓ تم تثبيت المكتبة")
        print()
        print("جاري إنشاء ملف صوت الإقامة...")
        
        # إنشاء محرك النطق
        engine = pyttsx3.init()
        engine.setProperty('rate', 100)
        engine.setProperty('volume', 1.0)
        
        # نص الإقامة
        iqama_text = "الله أكبر، الله أكبر. أشهد أن لا إله إلا الله. أشهد أن محمداً رسول الله. حي على الصلاة. حي على الفلاح. قد قامت الصلاة، قد قامت الصلاة. الله أكبر، الله أكبر. لا إله إلا الله."
        
        # حفظ الملف
        iqama_file = sounds_dir / "default_iqama.wav"
        engine.save_to_file(iqama_text, str(iqama_file))
        engine.runAndWait()
        
        print(f"✓ تم إنشاء ملف الإقامة!")
        print(f"  المسار: {iqama_file}")
        size_kb = iqama_file.stat().st_size / 1024
        print(f"  الحجم: {size_kb:.1f} KB")
        print()
        print("=" * 60)
        print("✅ اكتمل بنجاح!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ في pyttsx3: {e}")
        return False

def create_simple_iqama_wav():
    """
    إنشاء ملف إقامة بسيط بنغمات
    """
    print()
    print("جاري إنشاء ملف إقامة بسيط (نغمات)...")
    print()
    
    try:
        import numpy as np
        import wave
        
        sounds_dir = Path(__file__).parent / "resources" / "sounds"
        iqama_file = sounds_dir / "default_iqama.wav"
        
        sample_rate = 44100
        
        # نغمات الإقامة (أقصر من الأذان)
        frequencies = [
            (523, 0.8),  # C5
            (587, 0.8),  # D5
            (659, 1.0),  # E5
            (587, 0.8),  # D5
            (523, 1.0),  # C5
        ]
        
        audio_data = np.array([], dtype=np.float32)
        
        for freq, dur in frequencies:
            t = np.linspace(0, dur, int(sample_rate * dur))
            wave_data = np.sin(2 * np.pi * freq * t)
            
            # تلاشي
            fade_samples = int(sample_rate * 0.05)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            wave_data[:fade_samples] *= fade_in
            wave_data[-fade_samples:] *= fade_out
            
            audio_data = np.concatenate([audio_data, wave_data])
        
        # تطبيع
        audio_data = audio_data / np.max(np.abs(audio_data))
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # حفظ
        with wave.open(str(iqama_file), 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        print(f"✓ تم إنشاء ملف الإقامة!")
        print(f"  المسار: {iqama_file}")
        size_kb = iqama_file.stat().st_size / 1024
        print(f"  الحجم: {size_kb:.1f} KB")
        print()
        print("⚠️ ملاحظة: هذا ملف نغمات بسيط")
        print("للحصول على صوت إقامة حقيقي، حمّل ملف MP3 من الإنترنت")
        print()
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ: {e}")
        return False

if __name__ == "__main__":
    print()
    
    # محاولة الطريقة الأولى (gTTS)
    success = create_iqama_with_gtts()
    
    # إذا فشلت، محاولة الطريقة الثانية
    if not success:
        success = create_iqama_with_pyttsx3()
    
    # إذا فشلت، إنشاء ملف نغمات بسيط
    if not success:
        success = create_simple_iqama_wav()
    
    if not success:
        print()
        print("=" * 60)
        print("⚠️ لم يتم إنشاء ملف الإقامة")
        print("=" * 60)
        print()
        print("الحل البديل:")
        print("1. حمّل ملف إقامة MP3 من:")
        print("   - https://archive.org/search?query=iqama+islamic")
        print("   - YouTube: ابحث 'الإقامة صوت'")
        print()
        print("2. سمّه: default_iqama.mp3")
        print()
        print("3. ضعه في:")
        sounds_dir = Path(__file__).parent / "resources" / "sounds"
        print(f"   {sounds_dir}")
        print()
    
    print()
