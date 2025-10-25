#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug script to find exact bot issue
"""

import os
import sys
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import User

async def test_exact_setup():
    """Test the exact setup as in the bot."""
    print("🔍 Testing Exact Bot Setup...")
    print("="*50)
    
    # Get environment variables exactly as in bot
    API_ID = os.getenv('TELEGRAM_API_ID')
    API_HASH = os.getenv('TELEGRAM_API_HASH')
    ADMIN_ID = int(os.getenv('TELEGRAM_ADMIN_ID', '0'))
    SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')
    
    print(f"API_ID: {API_ID}")
    print(f"API_HASH: {API_HASH[:10]}...{API_HASH[-5:] if API_HASH else 'None'}")
    print(f"ADMIN_ID: {ADMIN_ID}")
    print(f"SESSION_STRING: {'Set' if SESSION_STRING else 'Missing'}")
    
    if not all([API_ID, API_HASH, ADMIN_ID, SESSION_STRING]):
        print("\n❌ MISSING ENVIRONMENT VARIABLES!")
        print("This is why the bot won't respond to messages.")
        print("\n📋 Required variables:")
        for var in ['TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_ADMIN_ID', 'TELEGRAM_SESSION_STRING']:
            if not os.getenv(var):
                print(f"  ❌ {var}: NOT SET")
        return False
    
    try:
        print("\n🤖 Creating client exactly as in bot...")
        client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
        
        print("🔗 Connecting...")
        await client.connect()
        
        if not client.is_user_authorized():
            print("❌ Not authorized!")
            return False
        
        me = await client.get_me()
        print(f"✅ Connected as: {me.first_name}")
        print(f"👤 User ID: {me.id}")
        print(f"🎯 Admin ID: {ADMIN_ID}")
        print(f"🆔 Match: {me.id == ADMIN_ID}")
        
        if me.id != ADMIN_ID:
            print(f"\n🚨 CRITICAL PROBLEM FOUND!")
            print(f"Connected user ID ({me.id}) ≠ Admin ID ({ADMIN_ID})")
            print("This means the bot filters out all messages!")
            print(f"\n🔧 FIX: Change ADMIN_ID to {me.id}")
            await client.disconnect()
            return False
        
        # Test message handler
        print("\n🧪 Testing message handler...")
        
        # Add a simple test handler
        message_received = False
        
        async def test_handler(event):
            nonlocal message_received
            message_received = True
            print(f"📨 Handler triggered! Message: {event.message.text}")
            
            # Check if it's from admin
            if event.sender_id == ADMIN_ID:
                print("✅ Message from admin - should be processed")
            else:
                print(f"⚠️ Message not from admin (ID: {event.sender_id})")
        
        print("📝 Adding test event handler...")
        client.add_event_handler(test_handler, events.NewMessage)
        
        print("🎯 Testing admin filter...")
        test_message = "Test message"
        
        # Simulate admin message (this won't work in test, just checking logic)
        print(f"✅ Handler registered successfully")
        print(f"🎯 Will respond to messages from ID: {ADMIN_ID}")
        
        await client.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🤖 BOT DEBUG TOOL")
    print("="*60)
    
    # First check environment
    print("\n1️⃣ Environment Check:")
    print("-"*30)
    
    required_vars = ['TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_ADMIN_ID', 'TELEGRAM_SESSION_STRING']
    all_set = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if 'SESSION' in var or 'HASH' in var:
                display = value[:10] + "..." + value[-5:]
            else:
                display = value
            print(f"✅ {var}: {display}")
        else:
            print(f"❌ {var}: NOT SET")
            all_set = False
    
    if not all_set:
        print("\n🚨 ROOT CAUSE: Environment variables not set!")
        print("🔧 SOLUTION:")
        print("1. Go to Render Dashboard")
        print("2. Select your service")
        print("3. Go to Environment section")
        print("4. Add missing variables")
        print("5. Deploy again")
        return
    
    print("\n2️⃣ Testing Bot Setup:")
    print("-"*30)
    
    try:
        result = asyncio.run(test_exact_setup())
        
        if result:
            print("\n✅ SETUP IS CORRECT!")
            print("If bot still doesn't respond, check:")
            print("- You're messaging the correct bot account")
            print("- The bot is properly deployed and running")
            print("- No network/firewall issues")
        else:
            print("\n❌ SETUP HAS ISSUES!")
            print("Fix the problems above and try again.")
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    main()