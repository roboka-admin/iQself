# 🚀 Quick Session String Guide

## ⚡ **سریعترین راه برای ساخت Session String**

### **مرحله ۱: Session Generator را دانلود کنید**
```bash
wget https://raw.githubusercontent.com/roboka-admin/iQself/master/session_generator.py
```

### **مرحله ۲: Python را نصب کنید** (اگر ندارید)
- Windows: از python.org دانلود کنید
- Mac: `brew install python`
- Linux: `sudo apt install python3 python3-pip`

### **مرحله ۳: Dependencies نصب کنید**
```bash
pip install telethon
```

### **مرحله ۴: Session String بسازید**
```bash
python session_generator.py
```

**دستوراتی که از شما می‌خواهد:**
1. `API ID`: `514739`
2. `API Hash`: `6cdd4549556212c69109c70cf30e30e2`
3. `Phone Number`: شماره تلفن شما (مثال: `+989123456789`)
4. `Verification Code`: کدی که از تلگرام می‌گیرید
5. `Password`: رمز دوعاملی (اگر فعال کرده‌اید)

### **مرحله ۵: Session String را کپی کنید**
در انتهای process، یک session string بلند دریافت می‌کنید. آن را کپی کنید.

### **مرحله ۶: در Render تنظیم کنید**
1. به سرویس self-bot خود در Render بروید
2. Environment Variables:
   ```
   TELEGRAM_SESSION_STRING=کپی_کنید_اینجا
   ```

## 🎯 **مثال Session String (نمونه):**
```
1BVtsOKcAQA6EBASDIORrmfbM5KGrwghPvf1TL0KbYB9BG2Z1...
```

## 🔐 **مزایای Session String:**
✅ **امن**: رمز عبور در سرور ذخیره نمی‌شود
✅ **ساده**: یک Environment Variable
✅ **قابل backup**: می‌توانید save کنید
✅ **قابل migration**: بین سرورها جابجا می‌شود

## 🆘 **عیب‌یابی:**

**خطای "Invalid credentials":**
- API_ID و API_HASH را چک کنید
- شماره تلفن را با کد کشور وارد کنید

**خطای "Invalid verification code":**
- کد جدیدی از تلگرام دریافت کنید
- چند دقیقه صبر کنید

**خطای "SessionPasswordNeededError":**
- رمز دوعاملی خود را وارد کنید
- اگر ندارید، پیام دهید

---

**🎉 بعد از ساخت Session String، ربات شما بدون نیاز به login آماده است!**