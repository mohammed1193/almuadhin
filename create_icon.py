"""
إنشاء أيقونة للبرنامج
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_app_icon():
    """
    ينشئ أيقونة للبرنامج بتصميم إسلامي احترافي عالي الجودة
    """
    print("=" * 60)
    print("🎨 إنشاء أيقونة البرنامج")
    print("=" * 60)
    print()
    
    icons_dir = Path(__file__).parent / "resources" / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    icon_path = icons_dir / "app_icon.ico"
    
    # إنشاء صورة 512x512 (حجم عالي الجودة)
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    import math
    
    # خلفية متدرجة من الأخضر الفاتح إلى الأخضر الداكن
    center = size // 2
    for i in range(center, 0, -1):
        # تدرج من الأخضر الفاتح في الوسط إلى الأخضر الداكن في الأطراف
        ratio = i / center
        r = int(100 + (50 * ratio))
        g = int(180 + (40 * ratio))
        b = int(100 + (30 * ratio))
        draw.ellipse([center - i, center - i, center + i, center + i], fill=(r, g, b, 255))
    
    # رسم مسجد بسيط وأنيق
    white = (255, 255, 255, 255)
    gold = (255, 215, 0, 255)
    
    # القبة المركزية الكبيرة
    dome_center_x = center
    dome_center_y = center - 20
    dome_radius = 70
    
    # قاعدة القبة
    dome_base_y = dome_center_y + dome_radius // 2
    draw.rectangle([dome_center_x - 60, dome_base_y, dome_center_x + 60, dome_base_y + 80], fill=white)
    
    # القبة نفسها (نصف دائرة)
    draw.pieslice([dome_center_x - dome_radius, dome_center_y - dome_radius, 
                   dome_center_x + dome_radius, dome_center_y + dome_radius], 
                  start=0, end=180, fill=gold)
    
    # الهلال فوق القبة
    crescent_y = dome_center_y - dome_radius - 25
    crescent_size = 20
    draw.ellipse([dome_center_x - crescent_size//2, crescent_y, 
                  dome_center_x + crescent_size//2, crescent_y + crescent_size], fill=gold)
    draw.ellipse([dome_center_x - crescent_size//2 + 8, crescent_y, 
                  dome_center_x + crescent_size//2 + 8, crescent_y + crescent_size], fill=(0, 0, 0, 0))
    
    # نجمة صغيرة
    star_x = dome_center_x + 15
    star_y = crescent_y + 8
    star_size = 5
    star_points = []
    for i in range(5):
        angle = math.pi / 2 + (2 * math.pi * i / 5)
        x = star_x + star_size * math.cos(angle)
        y = star_y - star_size * math.sin(angle)
        star_points.append((x, y))
        angle = math.pi / 2 + (2 * math.pi * (i + 0.5) / 5)
        x = star_x + (star_size * 0.4) * math.cos(angle)
        y = star_y - (star_size * 0.4) * math.sin(angle)
        star_points.append((x, y))
    draw.polygon(star_points, fill=gold)
    
    # المئذنتان على الجانبين
    minaret_width = 30
    minaret_height = 120
    
    # المئذنة اليسرى
    left_minaret_x = dome_center_x - 110
    minaret_y = dome_base_y + 20
    draw.rectangle([left_minaret_x, minaret_y, left_minaret_x + minaret_width, minaret_y + minaret_height], fill=white)
    # قبة المئذنة اليسرى
    dome_small_radius = 20
    draw.pieslice([left_minaret_x + minaret_width//2 - dome_small_radius, minaret_y - dome_small_radius,
                   left_minaret_x + minaret_width//2 + dome_small_radius, minaret_y + dome_small_radius],
                  start=0, end=180, fill=gold)
    
    # المئذنة اليمنى
    right_minaret_x = dome_center_x + 80
    draw.rectangle([right_minaret_x, minaret_y, right_minaret_x + minaret_width, minaret_y + minaret_height], fill=white)
    # قبة المئذنة اليمنى
    draw.pieslice([right_minaret_x + minaret_width//2 - dome_small_radius, minaret_y - dome_small_radius,
                   right_minaret_x + minaret_width//2 + dome_small_radius, minaret_y + dome_small_radius],
                  start=0, end=180, fill=gold)
    
    # باب المسجد (قوس)
    door_width = 35
    door_height = 50
    door_x = dome_center_x - door_width // 2
    door_y = dome_base_y + 30
    draw.rectangle([door_x, door_y, door_x + door_width, door_y + door_height], fill=(100, 150, 100, 255))
    # قوس الباب
    draw.pieslice([door_x - 5, door_y - 15, door_x + door_width + 5, door_y + 25],
                  start=0, end=180, fill=(100, 150, 100, 255))
    
    # نوافذ صغيرة
    window_size = 12
    # نافذة يسار
    draw.ellipse([dome_center_x - 40, dome_base_y + 45, dome_center_x - 40 + window_size, dome_base_y + 45 + window_size], 
                 fill=(100, 150, 100, 255))
    # نافذة يمين
    draw.ellipse([dome_center_x + 28, dome_base_y + 45, dome_center_x + 28 + window_size, dome_base_y + 45 + window_size], 
                 fill=(100, 150, 100, 255))
    
    # حفظ كملف ICO بأحجام متعددة عالية الجودة
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    icons = []
    for s in sizes:
        resized = img.resize(s, Image.Resampling.LANCZOS)
        icons.append(resized)
    
    # حفظ الأيقونة
    icons[0].save(
        icon_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in icons]
    )
    
    print(f"✓ تم إنشاء الأيقونة بنجاح!")
    print(f"  المسار: {icon_path}")
    print(f"  الأحجام: {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")
    print(f"  الجودة: عالية (512x512 أصلي)")
    print()
    
    # حفظ نسخة PNG عالية الجودة أيضاً
    png_path = icons_dir / "app_icon.png"
    img.save(png_path, format='PNG')
    print(f"✓ تم حفظ نسخة PNG: {png_path}")
    print()
    
    return icon_path

if __name__ == "__main__":
    try:
        create_app_icon()
        print("=" * 60)
        print("✓ اكتمل!")
        print("=" * 60)
        input("\nاضغط Enter للإغلاق...")
    except Exception as e:
        print(f"\nخطأ: {e}")
        import traceback
        traceback.print_exc()
        input("\nاضغط Enter للإغلاق...")
