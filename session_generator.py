#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session String Generator for Telegram Self-Bot
This script helps you create a session string for your Telegram account.
Run this on your local machine, then use the session string in Render.
"""

import os
import asyncio
import sys
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PhoneNumberInvalidError
import base64
import json

# Your credentials (enter manually)
API_ID = int(input("Enter your API ID: "))
API_HASH = input("Enter your API Hash: ")

async def generate_session_string():
    """Generate session string for Telegram authentication."""
    
    # Create temporary client
    client = TelegramClient('temp_session', API_ID, API_HASH)
    
    try:
        print("🚀 Starting Telegram authentication...")
        
        # Start authentication process
        await client.start()
        
        # If we get here, authentication was successful
        session_string = client.session.save()
        
        print("✅ Authentication successful!")
        print(f"📄 Session string generated: {session_string[:50]}...")
        
        # Save to file
        with open('session_string.txt', 'w') as f:
            f.write(session_string)
        
        print("💾 Session string saved to: session_string.txt")
        print("\n🔐 COPY THE SESSION STRING BELOW:")
        print("=" * 60)
        print(session_string)
        print("=" * 60)
        print("\n📋 INSTRUCTIONS:")
        print("1. Copy the session string above")
        print("2. In Render, go to your self-bot service")
        print("3. Add environment variable: TELEGRAM_SESSION_STRING")
        print("4. Paste the session string as the value")
        print("5. Redeploy your service")
        
        return session_string
        
    except PhoneNumberInvalidError:
        print("❌ Invalid phone number")
        return None
    except PhoneCodeInvalidError:
        print("❌ Invalid verification code")
        return None
    except SessionPasswordNeededError:
        print("🔑 Two-step verification required")
        password = input("Enter your 2FA password: ")
        
        try:
            await client.start(password=password)
            session_string = client.session.save()
            
            print("✅ Authentication successful with 2FA!")
            print(f"📄 Session string generated: {session_string[:50]}...")
            
            with open('session_string.txt', 'w') as f:
                f.write(session_string)
            
            print("💾 Session string saved to: session_string.txt")
            print("\n🔐 COPY THE SESSION STRING BELOW:")
            print("=" * 60)
            print(session_string)
            print("=" * 60)
            
            return session_string
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return None
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
    
    finally:
        await client.disconnect()

async def main():
    """Main function."""
    print("🤖 Telegram Session String Generator")
    print("=" * 40)
    print("This tool will help you create a session string")
    print("for your Telegram self-bot deployment.")
    print()
    
    session_string = await generate_session_string()
    
    if session_string:
        print("\n🎉 Session string generated successfully!")
        print("Keep this string secure and private.")
    else:
        print("\n❌ Failed to generate session string")
        print("Please check your credentials and try again.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Process cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)