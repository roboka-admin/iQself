#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic script to check bot status and troubleshoot connection issues
"""

import os
import sys

def check_environment():
    """Check if all required environment variables are set."""
    print("🔍 Checking Environment Variables...")
    
    required_vars = [
        'TELEGRAM_API_ID',
        'TELEGRAM_API_HASH', 
        'TELEGRAM_ADMIN_ID',
        'TELEGRAM_SESSION_STRING'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Hide sensitive data in display
            if var == 'TELEGRAM_SESSION_STRING':
                display_value = value[:20] + "..." + value[-10:] if len(value) > 30 else value
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
    
    print()

def check_bot_info():
    """Check basic bot information."""
    print("🤖 Bot Diagnostic Info...")
    
    # Check bot username from session string
    session_string = os.getenv('TELEGRAM_SESSION_STRING')
    if session_string:
        print(f"📝 Session String Length: {len(session_string)} characters")
        print(f"🔐 Session String Format: {session_string[:20]}...{session_string[-10:]}")
    else:
        print("❌ No session string provided")
    
    # Check admin ID
    admin_id = os.getenv('TELEGRAM_ADMIN_ID')
    if admin_id:
        print(f"👤 Admin ID: {admin_id}")
    else:
        print("❌ No admin ID provided")
    
    print()

def test_connection():
    """Test basic connection to Telegram."""
    print("🌐 Testing Telegram Connection...")
    
    try:
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        
        API_ID = os.getenv('TELEGRAM_API_ID')
        API_HASH = os.getenv('TELEGRAM_API_HASH')
        SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')
        
        if not all([API_ID, API_HASH, SESSION_STRING]):
            print("❌ Missing required credentials for connection test")
            return False
        
        print("🔑 Creating client...")
        client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)
        
        print("🔗 Connecting to Telegram...")
        client.connect()
        
        if client.is_user_authorized():
            me = client.get_me()
            print(f"✅ Connected successfully!")
            print(f"👤 Bot Name: {me.first_name}")
            print(f"🆔 Bot ID: {me.id}")
            print(f"📱 Phone: {me.phone}")
            print(f"👥 Bot Type: {'User' if me.bot else 'User'}")
            print(f"🔐 Authorized: {client.is_user_authorized()}")
            
            client.disconnect()
            return True
        else:
            print("❌ Bot not authorized. Session string might be invalid.")
            client.disconnect()
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main diagnostic function."""
    print("="*60)
    print("🤖 TELEGRAM BOT DIAGNOSTIC TOOL")
    print("="*60)
    print()
    
    check_environment()
    check_bot_info()
    
    print("🧪 Running Connection Test...")
    print("-" * 40)
    
    success = test_connection()
    
    print()
    print("="*60)
    if success:
        print("🎉 DIAGNOSIS: Bot connection is working correctly!")
        print()
        print("💡 TROUBLESHOOTING:")
        print("1. Make sure you're messaging the correct bot")
        print("2. Check if your ADMIN_ID is correct")
        print("3. Try sending /start command")
        print("4. Verify the bot has received messages")
    else:
        print("❌ DIAGNOSIS: Bot connection has issues!")
        print()
        print("🔧 SOLUTIONS:")
        print("1. Regenerate session string using @ForwardMsgOfficialBot")
        print("2. Verify API_ID and API_HASH are correct")
        print("3. Check if the bot account is still active")
        print("4. Ensure session string was created with correct credentials")
    print("="*60)

if __name__ == "__main__":
    main()