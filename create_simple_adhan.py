"""
إنشاء ملف أذان بسيط باستخدام pygame
"""

import pygame
import numpy as np
from pathlib import Path
import wave
import struct

def create_simple_adhan():
    """
    ينشئ ملف أذان بسيط (نغمة موسيقية)
    """
    print("=" * 60)
    print("🕌 إنشاء ملف أذان افتراضي")
    print("=" * 60)
    print()
    
    sounds_dir = Path(__file__).parent / "resources" / "sounds"
    sounds_dir.mkdir(parents=True, exist_ok=True)
    
    adhan_file = sounds_dir / "default_adhan.wav"
    iqama_file = sounds_dir / "default_iqama.wav"
    
    # التحقق من وجود ملف MP3
    adhan_mp3 = sounds_dir / "default_adhan.mp3"
    if adhan_mp3.exists():
        print(f"✓ ملف الأذان MP3 موجود بالفعل: {adhan_mp3}")
        size_kb = adhan_mp3.stat().st_size / 1024
        print(f"  الحجم: {size_kb:.1f} KB")
        print()
        return True
    
    # التحقق من وجود ملف WAV
    if adhan_file.exists():
        print(f"✓ ملف الأذان WAV موجود بالفعل: {adhan_file}")
        size_kb = adhan_file.stat().st_size / 1024
        print(f"  الحجم: {size_kb:.1f} KB")
        print()
        return True
    
    try:
        print("جاري إنشاء ملف أذان تجريبي...")
        print()
        
        # إعدادات الصوت
        sample_rate = 44100
        duration = 8  # 8 ثواني
        
        # إنشاء نغمات إسلامية
        # نستخدم مقام الحجاز (تقريباً)
        frequencies = [
            (440, 1.5),  # A4
            (493, 1.5),  # B4
            (523, 2.0),  # C5
            (587, 1.5),  # D5
            (523, 1.5),  # C5
            (440, 2.0),  # A4
        ]
        
        # إنشاء الموجة الصوتية
        audio_data = np.array([], dtype=np.float32)
        
        for freq, dur in frequencies:
            t = np.linspace(0, dur, int(sample_rate * dur))
            # موجة جيبية مع تلاشي
            wave = np.sin(2 * np.pi * freq * t)
            # إضافة تلاشي في البداية والنهاية
            fade_samples = int(sample_rate * 0.1)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            wave[:fade_samples] *= fade_in
            wave[-fade_samples:] *= fade_out
            audio_data = np.concatenate([audio_data, wave])
        
        # تطبيع الصوت
        audio_data = audio_data / np.max(np.abs(audio_data))
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # حفظ كملف WAV
        with wave.open(str(adhan_file), 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        print(f"✓ تم إنشاء ملف الأذان بنجاح!")
        print(f"  المسار: {adhan_file}")
        size_kb = adhan_file.stat().st_size / 1024
        print(f"  الحجم: {size_kb:.1f} KB")
        print()
        
        # إنشاء ملف إقامة (نغمة أقصر)
        if not iqama_file.exists():
            print("جاري إنشاء ملف إقامة تجريبي...")
            
            # نغمة أقصر للإقامة
            iqama_data = np.array([], dtype=np.float32)
            for freq, dur in [(523, 1.0), (440, 1.0)]:
                t = np.linspace(0, dur, int(sample_rate * dur))
                wave = np.sin(2 * np.pi * freq * t)
                fade_samples = int(sample_rate * 0.1)
                fade_in = np.linspace(0, 1, fade_samples)
                fade_out = np.linspace(1, 0, fade_samples)
                wave[:fade_samples] *= fade_in
                wave[-fade_samples:] *= fade_out
                iqama_data = np.concatenate([iqama_data, wave])
            
            iqama_data = iqama_data / np.max(np.abs(iqama_data))
            iqama_data = (iqama_data * 32767).astype(np.int16)
            
            with wave.open(str(iqama_file), 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(iqama_data.tobytes())
            
            print(f"✓ تم إنشاء ملف الإقامة!")
            print(f"  المسار: {iqama_file}")
            print()
        
        # تحديث config لاستخدام WAV
        print("تحديث الإعدادات لاستخدام ملفات WAV...")
        update_config_for_wav()
        
        print("=" * 60)
        print("⚠️ ملاحظة مهمة:")
        print("=" * 60)
        print("تم إنشاء ملفات صوتية تجريبية (نغمات بسيطة)")
        print()
        print("للحصول على أذان حقيقي:")
        print()
        print("1. حمّل ملف أذان MP3 من:")
        print("   - https://archive.org/details/adhan-collection")
        print("   - YouTube: ابحث 'أذان مكة المكرمة'")
        print()
        print("2. سمّه: default_adhan.mp3")
        print()
        print("3. ضعه في:")
        print(f"   {sounds_dir}")
        print()
        print("راجع: HOW_TO_ADD_ADHAN_FILES.md")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ: {e}")
        print()
        print("الحل البديل:")
        print("حمّل ملف أذان MP3 يدوياً وضعه في:")
        print(f"  {sounds_dir}/default_adhan.mp3")
        print()
        return False

def update_config_for_wav():
    """
    يحدث ملف الإعدادات لاستخدام WAV بدلاً من MP3
    """
    try:
        import json
        from pathlib import Path
        
        config_path = Path.home() / ".almuadhin" / "config.json"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # تحديث مسارات الملفات
            sounds_dir = Path(__file__).parent / "resources" / "sounds"
            config['sounds']['adhan_file'] = str(sounds_dir / "default_adhan.wav")
            config['sounds']['iqama_file'] = str(sounds_dir / "default_iqama.wav")
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            print("✓ تم تحديث الإعدادات")
    except:
        pass

if __name__ == "__main__":
    try:
        create_simple_adhan()
        print()
        input("اضغط Enter للإغلاق...")
    except Exception as e:
        print(f"\nخطأ: {e}")
        import traceback
        traceback.print_exc()
        input("\nاضغط Enter للإغلاق...")
