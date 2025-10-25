# ⚡ راهنمای مرحله به مرحله تنظیم Render

## 1️⃣ Self-Bot Service (اصلی)

### Environment Variables:
```bash
TELEGRAM_API_ID=514739
TELEGRAM_API_HASH=6cdd4549556212c69109c70cf30e30e2
TELEGRAM_ADMIN_ID=327459477
TELEGRAM_SESSION_STRING=[SESSION_STRING_اینجا]
```

### Start Command:
```bash
python self_render_secure.py
```

---

## 2️⃣ Helper-Bot Service (کنترل پنل)

### Environment Variables:
```bash
TELEGRAM_BOT_TOKEN=1251044377:AAFDgc2hxdcJvMsRw4aIWHDu4qpJ2RizU1o
ADMIN_ID=327459477
```

### Start Command:
```bash
python helper_render_secure.py
```

---

## 🔄 Deploy Process:

1. **Git Repository:** [https://github.com/roboka-admin/iQself](https://github.com/roboka-admin/iQself)
2. **Branch:** `master`
3. **Auto-Deploy:** فعال شود

---

## ✅ تست عملکرد:

### Self-Bot:
- در تلگرام پیامی برای خودتان بفرستید
- بات پاسخ بدهد

### Helper-Bot:
- URL را باز کنید
- کنترل پنل کار کند

---

## 🆘 اگر مشکلی بود:

### چک کردن Log:
- Render Dashboard → Logs

### متداولترین مشکلات:
- **Build Error:** Dependencies را چک کنید
- **Session Error:** Session string را چک کنید  
- **Bot Not Responding:** Environment variables را چک کنید

---

**🎯 Session string خود را دریافت کردید؟** آماده تنظیم Render هستید!