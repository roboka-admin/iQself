# 🔐 راهنمای کامل ایجاد Session String برای Telegram Self-Bot

## 📋 روش‌های موجود

### 🔒 روش اول (امنیت بالا): Script محلی Python

#### مرحله 1: نصب Python و Package ها
```bash
# نصب Python (اگر نصب نیست)
# از python.org دانلود کنید

# نصب telethon
pip install telethon
```

#### مرحله 2: اجرای Script
```bash
python session_generator.py
```

#### مرحله 3: وارد کردن اطلاعات
- API_ID: `514739`
- API_HASH: `6cdd4549556212c69109c70cf30e30e2`
- شماره تلفن خود (با کد کشور)

#### مرحله 4: دریافت Session String
- کد تأیید را از تلگرام وارد کنید
- اگر 2FA دارید، رمز عبور را وارد کنید
- Session string نمایش داده می‌شود

---

### 🚀 روش دوم (سریع): Telegram Bot

#### گزینه A: @ForwardMsgOfficialBot
1. به [ForwardMsgOfficialBot](https://t.me/ForwardMsgOfficialBot) بروید
2. "Generate Telegram Session" را انتخاب کنید
3. اطلاعات زیر را وارد کنید:
   - API_ID: `514739`
   - API_HASH: `6cdd4549556212c69109c70cf30e30e2`
   - شماره تلفن شما

#### گزینه B: @SessionStringGeneratorZBot
1. به [SessionStringGeneratorZBot](https://t.me/SessionStringGeneratorZBot) بروید
2. دستورالعمل‌های bot را دنبال کنید

---

### 🌐 روش سوم (آنلاین): Replit

#### ⚠️ توجه امنیتی
این روش **کمتر امن** است زیرا کد شما در سرورهای خارجی اجرا می‌شود.

#### استفاده:
1. به [Replit Generator](https://replit.com/@ErichDaniken/Generate-Telegram-String-Session) بروید
2. "Run" را بزنید
3. اطلاعات API را وارد کنید
4. Session string را کپی کنید

---

## ⚙️ تنظیم در Render

بعد از دریافت session string، در Render:

### 1. Self-Bot Service
- به Environment Variables بروید
- متغیر جدید ایجاد کنید:
  - **Name**: `TELEGRAM_SESSION_STRING`
  - **Value**: (Session string خود را اینجا قرار دهید)
- Deploy را انجام دهید

### 2. Helper-Bot Service
نیاز به session string ندارد (فقط bot token استفاده می‌کند).

---

## 🔒 نکات امنیتی

1. **Session String را هرگز عمومی نکنید**
2. **در کدها یا فایل‌های public قرار ندهید**
3. **فقط در Environment Variables امن ذخیره کنید**
4. **اگر فکر می‌کنید leakage شده، session را revoke کنید**

---

## 🆘 رفع مشکلات

### خطای شماره تلفن
- مطمئن شوید با کد کشور وارد می‌کنید (مثال: +98912...)
- مطمئن شوید شماره در تلگرام فعال است

### خطای کد تأیید
- چند دقیقه صبر کنید
- کد جدید درخواست کنید

### خطای 2FA
- رمز عبور دوم تلگرام خود را وارد کنید
- اگر فراموش کرده‌اید، باید reset کنید

### خطای API
- API_ID و API_HASH را چک کنید
- مطمئن شوید credentials درست است

---

## 📞 پشتیبانی

اگر مشکلی دارید، با اطلاعات زیر تماس بگیرید:
- شماره خطا
- مرحله‌ای که خطا رخ داده
- پیام خطای کامل

## 🎯 مراحل بعد از دریافت Session String

1. ✅ Session string را دریافت کنید
2. ⚙️ در Render environment variables تنظیم کنید
3. 🚀 هر دو service را deploy کنید
4. 🧪 عملکرد را تست کنید
5. 🔍 لاگ‌ها را چک کنید

---

**توجه**: برای امنیت حداکثری، استفاده از **روش اول (Script محلی)** توصیه می‌شود.