# متطلبات تحويل التطبيق إلى MSIX 📦

## نظرة عامة

MSIX هو تنسيق الحزم الحديث من Microsoft المطلوب للنشر على متجر مايكروسفت.

---

## 🛠️ الأدوات المطلوبة

### 1. MSIX Packaging Tool (إلزامي)
**التحميل:** من Microsoft Store  
**الرابط:** https://www.microsoft.com/store/productId/9N5LW3JBCXKF

**الميزات:**
- تحويل EXE إلى MSIX
- واجهة سهلة الاستخدام
- اختبار تلقائي

### 2. Windows App Certification Kit (إلزامي)
**التحميل:** جزء من Windows SDK  
**الرابط:** https://developer.microsoft.com/windows/downloads/windows-sdk/

**الاستخدام:**
- اختبار التوافق
- التحقق من المتطلبات
- تقرير الأخطاء

### 3. Visual Studio 2022 (اختياري لكن موصى به)
**التحميل:** Community Edition (مجاني)  
**الرابط:** https://visualstudio.microsoft.com/

**الميزات:**
- Windows Application Packaging Project
- تحكم متقدم
- تصحيح الأخطاء

---

## 📋 المتطلبات الأساسية

### 1. ملف EXE جاهز
```bash
# بناء التطبيق أولاً
python build_exe.py
# أو
build_simple.bat
```

**الموقع:** `dist/المؤذن.exe`

### 2. الموارد المطلوبة
- ✅ الأيقونات (512x512, 300x300, 150x150, 44x44)
- ✅ ملفات الصوت
- ✅ الخطوط (إذا كانت مخصصة)
- ✅ أي ملفات إضافية

### 3. معلومات التطبيق
- **اسم التطبيق:** المؤذن - مواقيت الصلاة
- **اسم الحزمة:** AlMuadhin
- **الناشر:** CN=Mohammed Al-Dakheel
- **الإصدار:** 1.0.0.0
- **المعرف:** com.mohammed.almuadhin

---

## 🔧 خطوات التحويل

### الطريقة 1: MSIX Packaging Tool (الأسهل)

#### الخطوة 1: تثبيت الأداة
1. افتح Microsoft Store
2. ابحث عن "MSIX Packaging Tool"
3. ثبت الأداة

#### الخطوة 2: إنشاء حزمة جديدة
1. افتح MSIX Packaging Tool
2. اختر "Application package"
3. اختر "Create package on this computer"

#### الخطوة 3: اختيار المثبت
1. اختر "Select installer"
2. تصفح إلى: `dist/المؤذن.exe`
3. اختر الملف

#### الخطوة 4: معلومات الحزمة
```
Package name: AlMuadhin
Package display name: المؤذن - مواقيت الصلاة
Publisher name: CN=Mohammed Al-Dakheel
Publisher display name: Mohammed Al-Dakheel
Version: 1.0.0.0
Install location: C:\Program Files\AlMuadhin
```

#### الخطوة 5: التثبيت
1. اضغط "Next"
2. انتظر التثبيت التجريبي
3. **مهم:** لا تشغل التطبيق الآن
4. اضغط "Next"

#### الخطوة 6: الخدمات والمهام
1. اختر "No" للخدمات
2. اختر "No" للمهام المجدولة
3. اضغط "Next"

#### الخطوة 7: إنشاء الحزمة
1. اختر موقع الحفظ
2. اضغط "Create"
3. انتظر الإنشاء (2-5 دقائق)

---

### الطريقة 2: Visual Studio (متقدم)

#### الخطوة 1: إنشاء مشروع جديد
1. افتح Visual Studio
2. File > New > Project
3. اختر "Windows Application Packaging Project"

#### الخطوة 2: إضافة التطبيق
1. Right-click على Applications
2. Add > Existing Project
3. أو Add > Reference (للـ EXE)

#### الخطوة 3: تكوين Manifest
عدّل `Package.appxmanifest`:
```xml
<Identity Name="AlMuadhin"
          Publisher="CN=Mohammed Al-Dakheel"
          Version="1.0.0.0" />

<Properties>
  <DisplayName>المؤذن - مواقيت الصلاة</DisplayName>
  <PublisherDisplayName>Mohammed Al-Dakheel</PublisherDisplayName>
  <Logo>Assets\StoreLogo.png</Logo>
</Properties>
```

#### الخطوة 4: البناء
1. Build > Build Solution
2. أو اضغط Ctrl+Shift+B

---

## 🔐 التوقيع الرقمي

### الخيار 1: شهادة من Microsoft (موصى به)
عند النشر على المتجر، Microsoft توقع تلقائياً.

### الخيار 2: شهادة مؤقتة للاختبار
```powershell
# إنشاء شهادة للاختبار
New-SelfSignedCertificate -Type Custom -Subject "CN=Mohammed Al-Dakheel" `
    -KeyUsage DigitalSignature -FriendlyName "AlMuadhin Test Cert" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

# التوقيع
SignTool sign /fd SHA256 /a /f MyCert.pfx /p Password AlMuadhin.msix
```

---

## ✅ اختبار الحزمة

### 1. التثبيت المحلي
```powershell
# تثبيت
Add-AppxPackage -Path "AlMuadhin.msix"

# التحقق
Get-AppxPackage -Name "*AlMuadhin*"

# إلغاء التثبيت
Remove-AppxPackage -Package "AlMuadhin_1.0.0.0_x64__xxxxx"
```

### 2. Windows App Certification Kit
```powershell
# تشغيل الاختبار
appcert.exe test -appxpackagepath "AlMuadhin.msix" -reportoutputpath "report.xml"
```

**يجب أن تمر جميع الاختبارات!**

---

## 📝 ملف AppxManifest.xml

نموذج كامل:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities">
  
  <Identity Name="AlMuadhin"
            Publisher="CN=Mohammed Al-Dakheel"
            Version="1.0.0.0" />
  
  <Properties>
    <DisplayName>المؤذن - مواقيت الصلاة</DisplayName>
    <PublisherDisplayName>Mohammed Al-Dakheel</PublisherDisplayName>
    <Logo>Assets\StoreLogo.png</Logo>
    <Description>تطبيق مواقيت الصلاة مع الأذان والإشعارات</Description>
  </Properties>
  
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.22000.0" />
  </Dependencies>
  
  <Resources>
    <Resource Language="ar-SA" />
    <Resource Language="en-US" />
  </Resources>
  
  <Applications>
    <Application Id="AlMuadhin" Executable="المؤذن.exe" EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements DisplayName="المؤذن"
                          Description="تطبيق مواقيت الصلاة"
                          BackgroundColor="transparent"
                          Square150x150Logo="Assets\Square150x150Logo.png"
                          Square44x44Logo="Assets\Square44x44Logo.png">
        <uap:DefaultTile Wide310x150Logo="Assets\Wide310x150Logo.png" />
      </uap:VisualElements>
    </Application>
  </Applications>
  
  <Capabilities>
    <rescap:Capability Name="runFullTrust" />
    <Capability Name="internetClient" />
  </Capabilities>
</Package>
```

---

## ⚠️ مشاكل شائعة وحلولها

### المشكلة: "Publisher name doesn't match"
**الحل:** تأكد من تطابق اسم الناشر في الشهادة والـ manifest

### المشكلة: "Package validation failed"
**الحل:** شغل WACK واقرأ التقرير

### المشكلة: "App doesn't launch"
**الحل:** تحقق من:
- المسارات النسبية للموارد
- التبعيات المفقودة
- الأذونات المطلوبة

### المشكلة: "Missing dependencies"
**الحل:** أضف جميع DLLs المطلوبة في الحزمة

---

## 📊 قائمة التحقق النهائية

قبل الرفع على المتجر:

- [ ] ملف MSIX تم إنشاؤه بنجاح
- [ ] التثبيت المحلي يعمل
- [ ] التطبيق يعمل بعد التثبيت
- [ ] WACK اجتاز جميع الاختبارات
- [ ] الأيقونات تظهر بشكل صحيح
- [ ] المعلومات في Manifest صحيحة
- [ ] الإصدار 1.0.0.0 أو أعلى
- [ ] الحجم معقول (< 500 MB)

---

## 🚀 الخطوة التالية

بعد إنشاء MSIX:
1. اختبر الحزمة محلياً
2. شغل WACK
3. أصلح أي أخطاء
4. ارفع على Partner Center
5. انتظر المراجعة

---

**الوقت المتوقع:** 2-4 ساعات للمرة الأولى  
**الصعوبة:** متوسطة

**تذكر:** Microsoft توفر دعم فني ممتاز إذا واجهت مشاكل!
