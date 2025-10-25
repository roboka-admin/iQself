#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test session string validity
"""

import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def test_session():
    # Your credentials
    API_ID = 514739
    API_HASH = "6cdd4549556212c69109c70cf30e30e2"
    SESSION_STRING = "1BJWap1wBu1QLqMbFS9sov4sBkBn2B19W1vCslvkNORTmbGRHTcZrPYEjFtzAy_wWytDwpSA34LsRMd1VvyDO8XTTP5_C_lhAZ1b2OF5dZmp0xiQBVInpTz_R6QnfK8dQlid_cnTduQcGFEw0BVbYDgLiwdzV2PhMnSS43DjCCbqcvDVcWMGeCbSiS1obqawHnIhVhHiMdhNvcDL6DjBBaoTLZeyZYUnM27MoOuD0qaafdCUf0pQoYKcob9uLe1jPNXnE9D8b0XdoXHVYoYvsDlnX5B6_2fbpFxKWMlPLrymWWUN21oHvcQZAjMj0pf625Q1hxPA5evRtZ7NEX934r7yYtTAwvpU="
    
    print("🔍 Testing Session String...")
    print(f"📝 Session String Length: {len(SESSION_STRING)} characters")
    print(f"🔐 Session String Preview: {SESSION_STRING[:20]}...{SESSION_STRING[-10:]}")
    print()
    
    try:
        # Create client with session string
        print("🔑 Creating Telegram client...")
        client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
        
        print("🔗 Connecting to Telegram...")
        await client.connect()
        
        if client.is_user_authorized():
            me = await client.get_me()
            print("✅ SESSION STRING IS VALID!")
            print()
            print("👤 Account Information:")
            print(f"   Name: {me.first_name} {me.last_name or ''}")
            print(f"   Username: @{me.username or 'N/A'}")
            print(f"   ID: {me.id}")
            print(f"   Phone: {me.phone}")
            print(f"   Bot: {'Yes' if me.bot else 'No'}")
            
            # Check if this is the correct admin account
            admin_id = 327459477
            if me.id == admin_id:
                print("✅ ADMIN ID MATCH: This session belongs to the admin account!")
            else:
                print(f"⚠️ ID MISMATCH: Session ID ({me.id}) ≠ Admin ID ({admin_id})")
            
            await client.disconnect()
            return True
        else:
            print("❌ SESSION INVALID: Not authorized")
            await client.disconnect()
            return False
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_session())
    if result:
        print("\n🎉 SUCCESS: Session string is working correctly!")
    else:
        print("\n❌ FAILED: Session string has issues!")