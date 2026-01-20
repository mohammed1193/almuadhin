"""
سكريبت لتحويل الأيقونة الحالية إلى 512x512 بكسل
مطلوب لمتجر مايكروسفت
"""

from PIL import Image
import os

def create_512_icon():
    """تحويل الأيقونة إلى 512x512"""
    
    # المسارات
    input_icon = "resources/icons/app_icon.png"
    output_icon = "resources/icons/app_icon_512.png"
    
    # التحقق من وجود الملف
    if not os.path.exists(input_icon):
        print(f"❌ الملف غير موجود: {input_icon}")
        print("جرب استخدام app_icon.ico بدلاً منه...")
        input_icon = "resources/icons/app_icon.ico"
        
        if not os.path.exists(input_icon):
            print(f"❌ الملف غير موجود أيضاً: {input_icon}")
            return False
    
    try:
        # فتح الصورة
        print(f"📂 فتح الملف: {input_icon}")
        img = Image.open(input_icon)
        
        # عرض المعلومات الحالية
        print(f"📏 الحجم الحالي: {img.size}")
        print(f"📋 الصيغة: {img.format}")
        
        # تحويل إلى RGBA إذا لزم الأمر
        if img.mode != 'RGBA':
            print("🔄 تحويل إلى RGBA...")
            img = img.convert('RGBA')
        
        # تغيير الحجم إلى 512x512 مع الحفاظ على الجودة
        print("🔄 تغيير الحجم إلى 512x512...")
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        
        # حفظ الصورة الجديدة
        print(f"💾 حفظ الأيقونة الجديدة: {output_icon}")
        img_512.save(output_icon, 'PNG', optimize=True)
        
        # التحقق من النتيجة
        saved_img = Image.open(output_icon)
        print(f"\n✅ تم بنجاح!")
        print(f"📏 الحجم الجديد: {saved_img.size}")
        print(f"📁 الموقع: {os.path.abspath(output_icon)}")
        
        # إنشاء أحجام إضافية للمتجر
        create_additional_sizes(img)
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def create_additional_sizes(original_img):
    """إنشاء أحجام إضافية مطلوبة للمتجر"""
    
    sizes = {
        'app_icon_300.png': (300, 300),  # Store Logo
        'app_icon_150.png': (150, 150),  # Square 150x150
        'app_icon_44.png': (44, 44),     # Square 44x44
    }
    
    print("\n📦 إنشاء أحجام إضافية...")
    
    for filename, size in sizes.items():
        try:
            output_path = f"resources/icons/{filename}"
            resized = original_img.resize(size, Image.Resampling.LANCZOS)
            resized.save(output_path, 'PNG', optimize=True)
            print(f"✅ تم إنشاء: {filename} ({size[0]}x{size[1]})")
        except Exception as e:
            print(f"⚠️ فشل إنشاء {filename}: {e}")

def verify_icon():
    """التحقق من جودة الأيقونة"""
    
    icon_path = "resources/icons/app_icon_512.png"
    
    if not os.path.exists(icon_path):
        print("❌ الأيقونة 512x512 غير موجودة")
        return False
    
    img = Image.open(icon_path)
    
    print("\n🔍 التحقق من الأيقونة:")
    print(f"✅ الحجم: {img.size}")
    print(f"✅ الصيغة: {img.format}")
    print(f"✅ النمط: {img.mode}")
    
    # التحقق من الشفافية
    if img.mode == 'RGBA':
        print("✅ تدعم الشفافية")
    else:
        print("⚠️ لا تدعم الشفافية")
    
    # التحقق من الحجم
    if img.size == (512, 512):
        print("✅ الحجم صحيح (512x512)")
    else:
        print(f"❌ الحجم غير صحيح: {img.size}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 تحويل الأيقونة إلى 512x512 لمتجر مايكروسفت")
    print("=" * 60)
    print()
    
    # إنشاء الأيقونة
    if create_512_icon():
        print()
        # التحقق من النتيجة
        verify_icon()
        print()
        print("=" * 60)
        print("✅ اكتمل! الأيقونة جاهزة للاستخدام في المتجر")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("❌ فشل إنشاء الأيقونة")
        print("=" * 60)
