#!/usr/bin/env python3
"""
Quick environment check for bot debugging
"""

import os

def main():
    print("🔍 Environment Variables Check")
    print("="*40)
    
    # Check each variable
    vars_to_check = [
        'TELEGRAM_API_ID',
        'TELEGRAM_API_HASH', 
        'TELEGRAM_ADMIN_ID',
        'TELEGRAM_SESSION_STRING'
    ]
    
    for var in vars_to_check:
        value = os.getenv(var)
        if value:
            if 'SESSION' in var or 'HASH' in var:
                # Mask sensitive data
                display = value[:15] + "..." + value[-5:]
            else:
                display = value
            print(f"✅ {var}: {display}")
        else:
            print(f"❌ {var}: NOT SET")
    
    print("\n" + "="*40)
    
    # Check if any Telegram vars are set at all
    telegram_vars = {k: v for k, v in os.environ.items() if 'TELEGRAM' in k}
    
    if telegram_vars:
        print("✅ Some Telegram environment variables are set")
    else:
        print("❌ NO Telegram environment variables found!")
        print("\n🔧 You need to set these in Render Dashboard:")
        print("1. Go to your service in Render")
        print("2. Click Environment")
        print("3. Add each variable with its value")

if __name__ == "__main__":
    main()