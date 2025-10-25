#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick bot ID checker - find the real admin ID
"""

import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def check_real_admin():
    """Find the real admin ID from the session string."""
    print("🔍 Finding Real Admin ID...")
    print("="*50)
    
    # Your credentials
    API_ID = 514739
    API_HASH = "6cdd4549556212c69109c70cf30e30e2"
    SESSION_STRING = "1BJWap1wBu1QLqMbFS9sov4sBkBn2B19W1vCslvkNORTmbGRHTcZrPYEjFtzAy_wWytDwpSA34LsRMd1VvyDO8XTTP5_C_lhAZ1b2OF5dZmp0xiQBVInpTz_R6QnfK8dQlid_cnTduQcGFEw0BVbYDgLiwdzV2PhMnSS43DjCCbqcvDVcWMGeCbSiS1obqawHnIhVhHiMdhNvcDL6DjBBaoTLZeyZYUnM27MoOuD0qaafdCUf0pQoYKcob9uLe1jPNXnE9D8b0XdoXHVYoYvsDlnX5B6_2fbpFxKWMlPLrymWWUN21oHvcQZAjMj0pf625Q1hxPA5evRtZ7NEX934r7yYtTAwvpU="
    
    try:
        print("🤖 Connecting to Telegram...")
        client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
        await client.connect()
        
        me = await client.get_me()
        
        print("✅ Connected successfully!")
        print(f"👤 Name: {me.first_name}")
        print(f"🆔 Real Admin ID: {me.id}")
        print(f"🎯 Current ADMIN_ID in settings: 327459477")
        print(f"🔄 Match: {me.id == 327459477}")
        
        if me.id != 327459477:
            print(f"\n🚨 MISMATCH FOUND!")
            print(f"You need to set ADMIN_ID to: {me.id}")
        
        await client.disconnect()
        return me.id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    admin_id = asyncio.run(check_real_admin())
    if admin_id:
        print(f"\n🎯 ACTION REQUIRED:")
        print(f"Update TELEGRAM_ADMIN_ID to: {admin_id}")
