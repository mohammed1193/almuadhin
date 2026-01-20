# دليل النشر على متجر مايكروسفت - خطوة بخطوة

هذا الدليل الشامل يشرح كيفية نشر تطبيق المؤذن على Microsoft Store.

---

## 📋 المتطلبات الأساسية

### 1. حساب مطور Microsoft
- **التسجيل:** [https://partner.microsoft.com/dashboard](https://partner.microsoft.com/dashboard)
- **الرسوم:** $19 للأفراد (دفعة واحدة) أو $99 للشركات (سنوياً)
- **الوثائق المطلوبة:** بطاقة هوية، معلومات دفع

### 2. الأدوات المطلوبة
- ✅ Visual Studio 2022 (Community Edition مجاني)
- ✅ Windows SDK
- ✅ Windows App Certification Kit (WACK)
- ✅ MSIX Packaging Tool

### 3. شهادة التوقيع الرقمي
- **الخيار 1:** شهادة من Partner Center (مجاناً للتطبيقات المنشورة)
- **الخيار 2:** شراء شهادة Code Signing من DigiCert أو Sectigo (~$200-400/سنة)

---

## 🔧 المرحلة 1: تحضير التطبيق

### الخطوة 1.1: التأكد من جاهزية الكود
```bash
# تأكد من أن جميع الاختبارات تعمل
python -m pytest tests/

# تشغيل التطبيق للتأكد من عدم وجود أخطاء
python src/main.py
```

### الخطوة 1.2: تحديث معلومات الإصدار
تحقق من `version_info.txt`:
- رقم الإصدار صحيح
- معلومات الشركة/المطور كاملة
- حقوق النشر محدثة

### الخطوة 1.3: إنشاء ملف EXE
```bash
# استخدم السكريبت الموجود
python build_exe.py

# أو استخدم PyInstaller مباشرة
pyinstaller المؤذن.spec
```

---

## 📦 المرحلة 2: تحويل إلى MSIX

### لماذا MSIX؟
- صيغة التطبيقات الحديثة لـ Windows
- مطلوبة للنشر على Microsoft Store
- توفر تثبيت وإلغاء تثبيت نظيف
- دعم التحديثات التلقائية

### الخطوة 2.1: تثبيت MSIX Packaging Tool
```powershell
# من Microsoft Store
# ابحث عن "MSIX Packaging Tool" وثبته
```

### الخطوة 2.2: تحويل EXE إلى MSIX

#### الطريقة 1: باستخدام MSIX Packaging Tool (GUI)

1. **افتح MSIX Packaging Tool**
2. **اختر "Application package"**
3. **اختر "Create package on this computer"**
4. **اختر ملف EXE:** `dist\المؤذن.exe`
5. **املأ معلومات التطبيق:**
   - Package name: `AlMuadhin`
   - Publisher: `CN=YourName`
   - Version: `1.0.0.0`
   - Package display name: `المؤذن - مواقيت الصلاة`
   - Publisher display name: `محمد الدخيل`

6. **اختر موقع الحفظ**
7. **اتبع معالج التثبيت:**
   - قم بتثبيت التطبيق
   - سجل جميع التغييرات
   - أغلق التطبيق عند الانتهاء

8. **احفظ الحزمة**

#### الطريقة 2: باستخدام Desktop App Converter (CLI)

```powershell
# تثبيت Desktop App Converter
# من: https://aka.ms/converter

# تحويل EXE إلى MSIX
DesktopAppConverter.exe `
    -Installer "dist\المؤذن.exe" `
    -AppExecutable "المؤذن.exe" `
    -Destination "output" `
    -PackageName "AlMuadhin" `
    -Publisher "CN=Mohammed Al-Dakheel" `
    -Version "1.0.0.0" `
    -MakeAppx `
    -Sign `
    -Verbose
```

#### الطريقة 3: إنشاء Manifest يدوياً

إنشاء ملف `AppxManifest.xml`:

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
    <PublisherDisplayName>محمد الدخيل</PublisherDisplayName>
    <Logo>Assets\StoreLogo.png</Logo>
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
        <uap:SplashScreen Image="Assets\SplashScreen.png" />
      </uap:VisualElements>
    </Application>
  </Applications>
  
  <Capabilities>
    <rescap:Capability Name="runFullTrust" />
    <Capability Name="internetClient" />
  </Capabilities>
  
</Package>
```

ثم استخدم MakeAppx:
```powershell
# إنشاء الحزمة
MakeAppx.exe pack /d "PackageFiles" /p "AlMuadhin.msix"

# توقيع الحزمة
SignTool.exe sign /fd SHA256 /a /f "certificate.pfx" /p "password" "AlMuadhin.msix"
```

---

## 🔐 المرحلة 3: التوقيع الرقمي

### الخيار 1: استخدام شهادة Partner Center (موصى به)

1. **ارفع الحزمة غير الموقعة إلى Partner Center**
2. **سيتم التوقيع تلقائياً عند النشر**

### الخيار 2: التوقيع المحلي

```powershell
# إنشاء شهادة اختبار (للتطوير فقط)
New-SelfSignedCertificate -Type Custom `
    -Subject "CN=Mohammed Al-Dakheel" `
    -KeyUsage DigitalSignature `
    -FriendlyName "Al-Muadhin Test Certificate" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

# تصدير الشهادة
$cert = Get-ChildItem -Path Cert:\CurrentUser\My | Where-Object {$_.Subject -match "Mohammed"}
Export-PfxCertificate -Cert $cert -FilePath "TestCertificate.pfx" -Password (ConvertTo-SecureString -String "password" -Force -AsPlainText)

# التوقيع
SignTool.exe sign /fd SHA256 /a /f "TestCertificate.pfx" /p "password" "AlMuadhin.msix"
```

---

## ✅ المرحلة 4: اختبار التطبيق

### الخطوة 4.1: تثبيت محلي
```powershell
# تثبيت الحزمة للاختبار
Add-AppxPackage -Path "AlMuadhin.msix"

# تشغيل التطبيق
# ابحث عن "المؤذن" في قائمة Start
```

### الخطوة 4.2: Windows App Certification Kit (WACK)

```powershell
# تشغيل WACK
# ابحث عن "Windows App Cert Kit" في قائمة Start

# أو من سطر الأوامر
"C:\Program Files (x86)\Windows Kits\10\App Certification Kit\appcert.exe" test -appxpackagepath "AlMuadhin.msix" -reportoutputpath "WACKReport.xml"
```

**يجب أن يجتاز التطبيق جميع الاختبارات:**
- ✅ Security tests
- ✅ Performance tests
- ✅ Supported API test
- ✅ Windows security features test
- ✅ App manifest compliance test

---

## 🚀 المرحلة 5: الرفع على Partner Center

### الخطوة 5.1: إنشاء تطبيق جديد

1. **سجل الدخول:** [https://partner.microsoft.com/dashboard](https://partner.microsoft.com/dashboard)
2. **اذهب إلى "Apps and games"**
3. **اضغط "New product" > "App"**
4. **احجز اسم التطبيق:** "المؤذن - مواقيت الصلاة" أو "Al-Muadhin"

### الخطوة 5.2: ملء معلومات التطبيق

#### Properties (الخصائص)
- **Category:** Productivity
- **Sub-category:** Lifestyle
- **Age rating:** Everyone
- **Privacy policy URL:** [رابط سياسة الخصوصية]

#### Pricing and availability (السعر والتوفر)
- **Pricing:** Free
- **Markets:** اختر الدول (السعودية، الإمارات، مصر، إلخ)
- **Visibility:** Public

#### App properties
- **Application category:** Productivity
- **Support info:** [بريدك الإلكتروني]

### الخطوة 5.3: رفع الحزمة

1. **اذهب إلى "Packages"**
2. **اسحب وأفلت ملف `.msix`**
3. **انتظر التحقق من الحزمة**
4. **تأكد من ظهور علامة ✅**

### الخطوة 5.4: Store listings (معلومات المتجر)

#### اللغة العربية (ar-SA)
- **Description:** [انسخ من STORE_LISTING.md]
- **Release notes:** "الإصدار الأول من تطبيق المؤذن"
- **Screenshots:** ارفع 4-10 صور (1366x768 أو أعلى)
- **Store logos:** 300x300 بكسل
- **App tile icon:** 1240x600 بكسل (اختياري)
- **Keywords:** مواقيت الصلاة، أذان، إسلام، مسلم، صلاة

#### اللغة الإنجليزية (en-US)
- كرر نفس الخطوات بالإنجليزية

### الخطوة 5.5: المراجعة والنشر

1. **راجع جميع المعلومات**
2. **اضغط "Submit to the Store"**
3. **انتظر المراجعة (3-7 أيام عادة)**

---

## 📊 المرحلة 6: بعد النشر

### مراقبة الأداء
- **Analytics:** راقب التحميلات والتقييمات
- **Health:** راقب الأخطاء والتعطلات
- **Reviews:** رد على تعليقات المستخدمين

### التحديثات
```powershell
# عند إصدار تحديث جديد:
# 1. زد رقم الإصدار في version_info.txt
# 2. أعد بناء EXE
# 3. أعد إنشاء MSIX
# 4. ارفع على Partner Center
# 5. اضغط "Submit update"
```

---

## ⚠️ مشاكل شائعة وحلولها

### مشكلة: فشل WACK Test
**الحل:**
- تأكد من عدم استخدام APIs غير مدعومة
- تأكد من توقيع الحزمة بشكل صحيح
- راجع تقرير WACK للتفاصيل

### مشكلة: رفض التطبيق من المراجعة
**الأسباب الشائعة:**
- سياسة الخصوصية غير موجودة أو غير واضحة
- لقطات الشاشة غير كافية
- الوصف غير واضح
- مشاكل في الأداء أو الاستقرار

**الحل:**
- راجع ملاحظات المراجعين بعناية
- أصلح المشاكل المذكورة
- أعد التقديم

### مشكلة: التطبيق لا يعمل بعد التثبيت من المتجر
**الحل:**
- تأكد من تضمين جميع المكتبات المطلوبة
- تأكد من المسارات النسبية للموارد
- اختبر على جهاز نظيف

---

## 📚 موارد إضافية

### وثائق Microsoft
- [Windows App Certification Kit](https://docs.microsoft.com/windows/uwp/debug-test-perf/windows-app-certification-kit)
- [MSIX Packaging](https://docs.microsoft.com/windows/msix/)
- [Partner Center Guide](https://docs.microsoft.com/windows/uwp/publish/)

### أدوات مفيدة
- [MSIX Hero](https://msixhero.net/) - أداة مجانية لإدارة MSIX
- [Advanced Installer](https://www.advancedinstaller.com/) - أداة متقدمة للتحزيم

---

## ✅ قائمة التحقق النهائية

قبل التقديم:

- [ ] التطبيق يعمل بدون أخطاء
- [ ] تم اجتياز WACK بنجاح
- [ ] سياسة الخصوصية منشورة على الويب
- [ ] لقطات الشاشة عالية الجودة (4-10 صور)
- [ ] الأيقونات بجميع الأحجام المطلوبة
- [ ] الوصف كامل بالعربي والإنجليزي
- [ ] معلومات الاتصال صحيحة
- [ ] رقم الإصدار صحيح
- [ ] الحزمة موقعة رقمياً
- [ ] تم الاختبار على Windows 10 و 11
- [ ] لا توجد محتويات محظورة
- [ ] التطبيق يحترم إرشادات المتجر

---

**ملاحظة:** هذا الدليل محدث حتى يناير 2026. قد تتغير بعض الخطوات مع تحديثات Microsoft.

**حظاً موفقاً في نشر تطبيقك! 🚀**
