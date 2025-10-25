#!/usr/bin/env python3
"""
Test script to verify bot connectivity and message handling
"""

import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

async def test_bot_connection():
    """Test bot connection and basic functionality."""
    
    # Get environment variables
    API_ID = os.getenv('TELEGRAM_API_ID')
    API_HASH = os.getenv('TELEGRAM_API_HASH')
    ADMIN_ID = int(os.getenv('TELEGRAM_ADMIN_ID', '0'))
    SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')
    
    if not all([API_ID, API_HASH, SESSION_STRING]):
        print("❌ Missing environment variables")
        return
    
    print("🔌 Testing bot connection...")
    
    try:
        # Create client with session string
        from telethon.sessions import StringSession
        client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
        
        await client.start()
        
        # Get admin info
        admin_user = await client.get_entity(ADMIN_ID)
        print(f"✅ Connected as: {admin_user.first_name}")
        print(f"🎯 Admin ID: {ADMIN_ID}")
        print(f"👤 Username: @{admin_user.username}")
        
        # Test message to admin
        print("📤 Sending test message...")
        await client.send_message(ADMIN_ID, "🤖 **Bot Test Message**\n\nThis is a test to verify the bot is working correctly!")
        
        print("✅ Test message sent successfully!")
        print("🔍 Check your Telegram for the message")
        
        # Test getting dialogs
        print("\n📋 Testing dialog access...")
        async for dialog in client.iter_dialogs():
            if dialog.is_user:
                user = dialog.entity
                if user.id == ADMIN_ID:
                    print(f"✅ Found admin dialog: {user.first_name}")
                    break
        
        await client.disconnect()
        print("✅ Bot connectivity test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot_connection())