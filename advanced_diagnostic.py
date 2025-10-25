#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced diagnostic script for bot troubleshooting
"""

import os
import sys
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def check_render_environment():
    """Check what's actually available in the Render environment."""
    print("🔍 Rendering Environment Check...")
    print("="*50)
    
    # Check all environment variables that might be related
    telegram_vars = {}
    for key, value in os.environ.items():
        if key.upper().startswith('TELEGRAM'):
            # Mask sensitive values
            if 'SESSION' in key or 'TOKEN' in key or 'HASH' in key:
                if value:
                    display_value = value[:20] + "..." + value[-10:] if len(value) > 30 else value
                else:
                    display_value = "NOT SET"
            else:
                display_value = value
            telegram_vars[key] = display_value
            print(f"✅ {key}: {display_value}")
    
    print()
    print("📋 Summary:")
    required_vars = ['TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_ADMIN_ID', 'TELEGRAM_SESSION_STRING']
    
    for var in required_vars:
        env_var = os.getenv(var)
        if env_var:
            print(f"✅ {var}: Available")
        else:
            print(f"❌ {var}: Missing")
    
    return telegram_vars

async def test_with_render_env():
    """Test connection using actual Render environment variables."""
    print("\n🧪 Testing with Render Environment...")
    print("="*50)
    
    try:
        API_ID = os.getenv('TELEGRAM_API_ID')
        API_HASH = os.getenv('TELEGRAM_API_HASH')
        ADMIN_ID = os.getenv('TELEGRAM_ADMIN_ID')
        SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')
        
        print(f"API_ID: {API_ID}")
        print(f"API_HASH: {API_HASH[:20]}..." if API_HASH else "API_HASH: None")
        print(f"ADMIN_ID: {ADMIN_ID}")
        print(f"SESSION_STRING: {'Available' if SESSION_STRING else 'Missing'}")
        
        if not all([API_ID, API_HASH, ADMIN_ID, SESSION_STRING]):
            print("❌ Missing required environment variables!")
            return False
        
        print("\n🔑 Creating client with Render environment...")
        client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)
        
        print("🔗 Connecting to Telegram...")
        await client.connect()
        
        if client.is_user_authorized():
            me = await client.get_me()
            print("✅ SUCCESS: Bot connected with Render environment!")
            print(f"👤 Name: {me.first_name}")
            print(f"🆔 ID: {me.id}")
            print(f"🎯 Admin ID Expected: {ADMIN_ID}")
            print(f"🎯 Admin ID Match: {me.id == int(ADMIN_ID)}")
            
            await client.disconnect()
            return True
        else:
            print("❌ FAILED: Not authorized with Render environment")
            await client.disconnect()
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

async def simulate_message_handler():
    """Simulate message handling to test event registration."""
    print("\n📨 Testing Message Handler Logic...")
    print("="*50)
    
    # Simulate the admin handler logic
    try:
        API_ID = os.getenv('TELEGRAM_API_ID')
        API_HASH = os.getenv('TELEGRAM_API_HASH')
        SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')
        ADMIN_ID = int(os.getenv('TELEGRAM_ADMIN_ID', '0'))
        
        if not all([API_ID, API_HASH, SESSION_STRING]):
            print("❌ Cannot test handler: missing credentials")
            return False
        
        print("🤖 Setting up client for handler test...")
        client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)
        await client.connect()
        
        if not client.is_user_authorized():
            print("❌ Client not authorized")
            await client.disconnect()
            return False
        
        me = await client.get_me()
        print(f"👤 Connected as: {me.first_name} (ID: {me.id})")
        print(f"🎯 Target Admin ID: {ADMIN_ID}")
        print(f"✅ Admin ID Match: {me.id == ADMIN_ID}")
        
        if me.id != ADMIN_ID:
            print("❌ CRITICAL: Connected user ID ≠ Admin ID!")
            print("This means the bot will ignore all messages!")
        
        await client.disconnect()
        return me.id == ADMIN_ID
        
    except Exception as e:
        print(f"❌ Handler test failed: {e}")
        return False

async def main():
    """Main diagnostic function."""
    print("🤖 ADVANCED BOT DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Check environment
    await check_render_environment()
    
    # Test with render env
    env_success = await test_with_render_env()
    
    # Test handler logic
    handler_success = await simulate_message_handler()
    
    print("\n" + "=" * 60)
    print("📊 DIAGNOSIS RESULTS:")
    print(f"Environment Variables: {'✅ OK' if env_success else '❌ ISSUE'}")
    print(f"Handler Logic: {'✅ OK' if handler_success else '❌ ISSUE'}")
    
    if not handler_success:
        print("\n🚨 ROOT CAUSE FOUND:")
        print("The bot connects successfully but the ADMIN_ID doesn't match!")
        print("This means the bot filters out all messages because they don't come from the admin.")
        print("\n🔧 SOLUTION:")
        print("1. Check what your actual Telegram user ID is")
        print("2. Update TELEGRAM_ADMIN_ID in Render to match your real ID")
        print("3. Get your ID by messaging @userinfobot in Telegram")
    
    print("\n🎯 NEXT STEPS:")
    if not env_success:
        print("1. Set up environment variables in Render dashboard")
    if not handler_success:
        print("2. Fix admin ID mismatch")
    print("3. Deploy and test again")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())