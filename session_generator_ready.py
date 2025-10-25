#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session String Generator - آماده استفاده
اطلاعات API شما از قبل تنظیم شده
"""

import os
import asyncio
import sys
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PhoneNumberInvalidError

# اطلاعات شما (از قبل تنظیم شده)
API_ID = 514739
API_HASH = "6cdd4549556212c69109c70cf30e30e2"

async def generate_session_string():
    """Generate session string for Telegram authentication."""
    
    print("🤖 Telegram Session String Generator - آماده استفاده")
    print("=" * 50)
    print("🔑 اطلاعات API:")
    print(f"   API_ID: {API_ID}")
    print(f"   API_HASH: {API_HASH[:20]}...")
    print()
    
    # دریافت شماره تلفن از کاربر
    phone_number = input("📱 شماره تلفن خود را وارد کنید (با کد کشور): ").strip()
    
    if not phone_number:
        print("❌ شماره تلفن الزامی است!")
        return None
    
    # Create temporary client
    client = TelegramClient('temp_session', API_ID, API_HASH)
    
    try:
        print("\n🚀 شروع احراز هویت تلگرام...")
        
        # Start authentication process
        await client.start(phone=phone_number)
        
        # If we get here, authentication was successful
        session_string = client.session.save()
        
        print("✅ احراز هویت موفق بود!")
        print(f"📄 Session string تولید شد: {session_string[:50]}...")
        
        # Save to file
        with open('session_string.txt', 'w') as f:
            f.write(session_string)
        
        print("💾 Session string ذخیره شد در: session_string.txt")
        print("\n🔐 SESSION STRING:")
        print("=" * 60)
        print(session_string)
        print("=" * 60)
        print("\n📋 مراحل بعدی:")
        print("1. این session string را کپی کنید")
        print("2. در Render، به environment variables بروید")
        print("3. متغیر جدید: TELEGRAM_SESSION_STRING")
        print("4. مقدار را paste کنید")
        print("5. Deploy کنید")
        
        return session_string
        
    except PhoneNumberInvalidError:
        print("❌ شماره تلفن نامعتبر است")
        print("💡 مطمئن شوید با کد کشور وارد کردید (مثال: +98912...)")
        return None
    except PhoneCodeInvalidError:
        print("❌ کد تأیید نامعتبر است")
        print("💡 چند دقیقه صبر کنید و کد جدید درخواست کنید")
        return None
    except SessionPasswordNeededError:
        print("🔑 رمز عبور دوم تلگرام (2FA) مورد نیاز است")
        password = input("رمز عبور دوم را وارد کنید: ")
        
        try:
            await client.start(phone=phone_number, password=password)
            session_string = client.session.save()
            
            print("✅ احراز هویت با 2FA موفق بود!")
            print(f"📄 Session string تولید شد: {session_string[:50]}...")
            
            with open('session_string.txt', 'w') as f:
                f.write(session_string)
            
            print("💾 Session string ذخیره شد در: session_string.txt")
            print("\n🔐 SESSION STRING:")
            print("=" * 60)
            print(session_string)
            print("=" * 60)
            
            return session_string
            
        except Exception as e:
            print(f"❌ احراز هویت ناموفق: {e}")
            return None
    
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")
        return None
    
    finally:
        await client.disconnect()

async def main():
    """Main function."""
    session_string = await generate_session_string()
    
    if session_string:
        print("\n🎉 Session string با موفقیت تولید شد!")
        print("🔒 این را در جای امن نگهداری کنید")
        print("\n⚡ مرحله بعدی: تنظیم در Render")
    else:
        print("\n❌ تولید session string ناموفق بود")
        print("💡 لطفاً اطلاعات را بررسی کنید و مجدداً تلاش کنید")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 فرآیند توسط کاربر متوقف شد")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطای مهلک: {e}")
        sys.exit(1)