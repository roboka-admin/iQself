#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Session String Generator - فارسی و آماده
"""

import os
import asyncio
import sys
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PhoneNumberInvalidError

# اطلاعات کاربر
API_ID = 514739
API_HASH = "6cdd4549556212c69109c70cf30e30e2"

async def generate_session_string():
    """ایجاد session string برای احراز هویت تلگرام"""
    
    print("🤖 مولد Session String تلگرام")
    print("=" * 45)
    print("📊 اطلاعات API:")
    print(f"   API_ID: {API_ID}")
    print(f"   API_HASH: {API_HASH[:15]}...")
    print("-" * 45)
    
    # دریافت شماره تلفن
    phone = input("📱 شماره تلفن شما (مثال: +98912...) = ").strip()
    
    if not phone:
        print("❌ خطا: شماره تلفن وارد نشده!")
        return None
    
    client = TelegramClient('temp', API_ID, API_HASH)
    
    try:
        print("\n🔄 در حال اتصال به تلگرام...")
        await client.start(phone=phone)
        
        session_str = client.session.save()
        
        print("✅ موفقیت! احراز هویت انجام شد")
        print("📄 Session string ساخته شد")
        
        # ذخیره فایل
        with open('my_session_string.txt', 'w', encoding='utf-8') as f:
            f.write(session_str)
        
        print("\n" + "="*60)
        print("🔐 SESSION STRING شما:")
        print("="*60)
        print(session_str)
        print("="*60)
        print("\n💾 در فایل 'my_session_string.txt' ذخیره شد")
        print("\n⚡ مراحل بعدی:")
        print("1️⃣ این session string را کپی کنید")
        print("2️⃣ در Render داشبورد بروید")
        print("3️⃣ Environment Variables را باز کنید")
        print("4️⃣ متغیر جدید بسازید:")
        print("   - Name: TELEGRAM_SESSION_STRING")
        print("   - Value: (session string اینجا)")
        print("5️⃣ Deploy کنید")
        
        return session_str
        
    except PhoneNumberInvalidError:
        print("❌ شماره تلفن نامعتبر")
        print("💡 نکته: حتماً باید با کد کشور باشد (مثال: +98912...)")
        return None
        
    except PhoneCodeInvalidError:
        print("❌ کد تأیید اشتباه")
        print("💡 نکته: چند دقیقه صبر کنید و کد جدید بگیرید")
        return None
        
    except SessionPasswordNeededError:
        print("🔑 نیاز به رمز عبور دوم (2FA)")
        password = input("رمز عبور دوم خود را وارد کنید: ")
        
        try:
            await client.start(phone=phone, password=password)
            session_str = client.session.save()
            
            print("✅ با موفقیت وارد شدید!")
            print("📄 Session string با 2FA ساخته شد")
            
            with open('my_session_string.txt', 'w', encoding='utf-8') as f:
                f.write(session_str)
            
            print("\n" + "="*60)
            print("🔐 SESSION STRING شما:")
            print("="*60)
            print(session_str)
            print("="*60)
            
            return session_str
            
        except Exception as e:
            print(f"❌ خطا در 2FA: {e}")
            return None
    
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")
        return None
    
    finally:
        await client.disconnect()

async def main():
    print("🎯 ایجاد Session String برای Render Deployment")
    print("=" * 50)
    
    result = await generate_session_string()
    
    if result:
        print("\n🎉 تبریک! Session string آماده است!")
        print("🚀 آماده Deploy در Render")
    else:
        print("\n❌ متأسفانه مشکلی پیش آمد")
        print("🔄 دوباره تلاش کنید")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ متوقف شد")
    except Exception as e:
        print(f"\n💥 خطای سیستمی: {e}")