"""
إنشاء أيقونة للتطبيق
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_icon():
    """
    ينشئ أيقونة للتطبيق بتصميم بسيط وجميل
    """
    print("=" * 60)
    print("🎨 إنشاء أيقونة التطبيق")
    print("=" * 60)
    print()
    
    resources_dir = Path(__file__).parent / "resources" / "icons"
    resources_dir.mkdir(parents=True, exist_ok=True)
    
    icon_path = resources_dir / "app_icon.ico"
    
    # إنشاء صورة 256x256
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # رسم دائرة خضراء (خلفية)
    margin = 20
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=(46, 125, 50, 255),  # أخضر إسلامي
        outline=(27, 94, 32, 255),
        width=4
    )
    
    # رسم هلال (رمز إسلامي)
    # دائرة كبيرة
    moon_center = size // 2
    moon_radius = 60
    draw.ellipse(
        [moon_center - moon_radius, moon_center - moon_radius - 20,
         moon_center + moon_radius, moon_center + moon_radius - 20],
        fill=(255, 255, 255, 255)
    )
    
    # دائرة صغيرة لعمل الهلال
    small_radius = 50
    offset = 15
    draw.ellipse(
        [moon_center - small_radius + offset, moon_center - small_radius - 20,
         moon_center + small_radius + offset, moon_center + small_radius - 20],
        fill=(46, 125, 50, 255)
    )
    
    # رسم نجمة صغيرة
    star_x = moon_center + 35
    star_y = moon_center - 40
    star_size = 15
    
    # نجمة خماسية
    points = []
    import math
    for i in range(5):
        angle = math.pi / 2 + (2 * math.pi * i / 5)
        x = star_x + star_size * math.cos(angle)
        y = star_y - star_size * math.sin(angle)
        points.append((x, y))
        
        angle = math.pi / 2 + (2 * math.pi * (i + 0.5) / 5)
        x = star_x + (star_size * 0.4) * math.cos(angle)
        y = star_y - (star_size * 0.4) * math.sin(angle)
        points.append((x, y))
    
    draw.polygon(points, fill=(255, 255, 255, 255))
    
    # حفظ بأحجام مختلفة لـ ICO
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    images = []
    
    for icon_size in sizes:
        resized = img.resize(icon_size, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # حفظ كملف ICO
    images[0].save(
        str(icon_path),
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    
    print(f"✓ تم إنشاء الأيقونة بنجاح!")
    print(f"  المسار: {icon_path}")
    print()
    
    # حفظ نسخة PNG أيضاً
    png_path = resources_dir / "app_icon.png"
    img.save(str(png_path), 'PNG')
    print(f"✓ تم حفظ نسخة PNG")
    print(f"  المسار: {png_path}")
    print()
    
    print("=" * 60)
    print("✅ اكتمل بنجاح!")
    print("=" * 60)
    
    return icon_path

if __name__ == "__main__":
    try:
        create_icon()
        print()
    except Exception as e:
        print(f"✗ خطأ: {e}")
        import traceback
        traceback.print_exc()
