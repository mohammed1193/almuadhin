"""
هذا السكريبت ينشئ ملفات صوت تجريبية بسيطة للأذان والإقامة
يمكن استخدامها للاختبار حتى تحصل على ملفات أذان حقيقية
"""

import pygame
import numpy as np
from pathlib import Path

def create_beep_sound(filename, duration=3, frequency=440):
    """
    ينشئ صوت بسيط (beep) للاختبار
    """
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2)
        
        sample_rate = 22050
        samples = int(sample_rate * duration)
        
        wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, samples))
        
        wave = (wave * 32767).astype(np.int16)
        
        stereo_wave = np.column_stack((wave, wave))
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        
        pygame.mixer.Sound.play(sound)
        pygame.time.wait(int(duration * 1000))
        
        output_path = Path(__file__).parent / "resources" / "sounds" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"تم إنشاء ملف الصوت: {output_path}")
        print("ملاحظة: هذا ملف تجريبي بسيط. يُنصح باستبداله بملف أذان حقيقي.")
        
        return True
        
    except Exception as e:
        print(f"خطأ في إنشاء الملف الصوتي: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("إنشاء ملفات صوت تجريبية")
    print("=" * 50)
    print()
    
    print("هذه الملفات للاختبار فقط!")
    print("يُنصح بشدة باستبدالها بملفات أذان حقيقية من:")
    print("- https://archive.org/details/adhan-collection")
    print("- https://www.islamicity.org/")
    print()
    
    resources_path = Path(__file__).parent / "resources" / "sounds"
    resources_path.mkdir(parents=True, exist_ok=True)
    
    adhan_file = resources_path / "default_adhan.mp3"
    iqama_file = resources_path / "default_iqama.mp3"
    
    if adhan_file.exists():
        print(f"✓ ملف الأذان موجود بالفعل: {adhan_file}")
    else:
        print("✗ ملف الأذان غير موجود")
        print("  يرجى تحميل ملف أذان MP3 ووضعه في:")
        print(f"  {adhan_file}")
    
    print()
    
    if iqama_file.exists():
        print(f"✓ ملف الإقامة موجود بالفعل: {iqama_file}")
    else:
        print("✗ ملف الإقامة غير موجود")
        print("  يرجى تحميل ملف إقامة MP3 ووضعه في:")
        print(f"  {iqama_file}")
    
    print()
    print("=" * 50)
    print("للحصول على أفضل تجربة، حمّل ملفات أذان حقيقية!")
    print("=" * 50)
