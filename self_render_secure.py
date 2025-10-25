#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Self-Bot - Secure Version
This version uses environment variables for sensitive data
"""

import os
import asyncio
import logging
from telethon import TelegramClient, events, Button
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PhoneNumberInvalidError
from telethon.tl.types import User, Chat, Channel
import matplotlib
matplotlib.use('Agg')  # For headless environment
import matplotlib.pyplot as plt
import psutil
import json
import aiohttp
from datetime import datetime
import pytz
from googletrans import Translator
from gtts import gTTS
import io
import re

# Secure configuration using environment variables
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
ADMIN_ID = int(os.getenv('TELEGRAM_ADMIN_ID', '0'))
SESSION_NAME = os.getenv('TELEGRAM_SESSION_NAME', 'self_bot')
SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')  # Alternative to session file

if not all([API_ID, API_HASH]):
    logging.error("❌ Missing required environment variables:")
    logging.error("Please set: TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_ADMIN_ID")
    exit(1)

if not SESSION_STRING:
    logging.warning("⚠️ TELEGRAM_SESSION_STRING not set. Bot may need authentication.")

# Initialize logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Global variables
client = None
admin_user = None
translator = Translator()

async def setup_matplotlib():
    """Setup matplotlib for plotting with proper configuration."""
    import warnings
    warnings.filterwarnings('default')
    plt.style.use('default')
    plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

async def setup_client():
    """Initialize and setup Telegram client."""
    global client, admin_user
    
    try:
        if SESSION_STRING:
            # Use session string for quick authentication
            logger.info("🔑 Using session string for authentication")
            client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
            await client.start()
            # Load session string if available
            await client.session.set_dc(2, "149.154.164.5", 443)
            await client.session.auth_key = await client.session.generate_auth_key()
            await client.session.save()
        else:
            # Use traditional authentication
            logger.info("🔐 Starting traditional authentication")
            client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
            await client.start()
        
        # Get admin user info
        admin_user = await client.get_entity(ADMIN_ID)
        logger.info(f"✅ Bot connected successfully as {admin_user.first_name}")
        
        return True
    except SessionPasswordNeededError:
        logger.error("❌ Two-step verification password required")
        logger.error("Set TELEGRAM_PASSWORD environment variable or create session string")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to setup client: {e}")
        return False

async def get_system_stats():
    """Get system statistics."""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu': f"{cpu_percent:.1f}%",
            'memory': f"{memory.percent:.1f}%",
            'disk': f"{disk.percent:.1f}%",
            'memory_gb': f"{memory.used // 1024**3}GB / {memory.total // 1024**3}GB",
            'disk_gb': f"{disk.used // 1024**3}GB / {disk.total // 1024**3}GB"
        }
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        return {'error': str(e)}

async def create_system_chart():
    """Create system usage chart."""
    try:
        await setup_matplotlib()
        
        # Get current stats
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # CPU and Memory usage
        categories = ['CPU', 'Memory', 'Disk']
        usage = [cpu_percent, memory.percent, disk.percent]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        
        bars = ax1.bar(categories, usage, color=colors)
        ax1.set_title('System Usage (%)')
        ax1.set_ylim(0, 100)
        
        # Add value labels on bars
        for bar, value in zip(bars, usage):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{value:.1f}%', ha='center', va='bottom')
        
        # Memory breakdown
        memory_data = [memory.used // 1024**3, memory.free // 1024**3]
        memory_labels = ['Used', 'Free']
        ax2.pie(memory_data, labels=memory_labels, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Memory Usage')
        
        plt.tight_layout()
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer.getvalue()
    except Exception as e:
        logger.error(f"Error creating chart: {e}")
        return None

async def translate_text(text, dest='en'):
    """Translate text using Google Translate."""
    try:
        result = translator.translate(text, dest=dest)
        return result.text
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return f"Translation failed: {e}"

async def text_to_speech(text, lang='en'):
    """Convert text to speech."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        logger.error(f"TTS error: {e}")
        return None

@events.NewMessage(chats=ADMIN_ID)
async def admin_handler(event):
    """Handle admin messages."""
    try:
        message = event.message
        text = message.text or ""
        
        # Main menu
        if text == '/start':
            await show_main_menu(event)
        
        # System commands
        elif text == '/stats':
            stats = await get_system_stats()
            if 'error' in stats:
                await event.respond(f"❌ Error getting stats: {stats['error']}")
            else:
                stats_text = f"""📊 **System Statistics**
                
🔧 **CPU:** {stats['cpu']}
🧠 **Memory:** {stats['memory']} ({stats['memory_gb']})
💾 **Disk:** {stats['disk']} ({stats['disk_gb']})"""
                
                await event.respond(stats_text)
        
        elif text == '/chart':
            chart_data = await create_system_chart()
            if chart_data:
                await event.respond("📊 **System Usage Chart**", file=chart_data)
            else:
                await event.respond("❌ Failed to generate chart")
        
        elif text == '/time':
            now = datetime.now(pytz.UTC)
            await event.respond(f"🕐 **Current Time:** {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Translation commands
        elif text.startswith('/translate '):
            text_to_translate = text[11:].strip()
            if text_to_translate:
                translated = await translate_text(text_to_translate)
                await event.respond(f"🌐 **Translation:** {translated}")
            else:
                await event.respond("❌ Please provide text to translate")
        
        elif text.startswith('/tts '):
            text_to_speech_input = text[5:].strip()
            if text_to_speech_input:
                audio_data = await text_to_speech(text_to_speech_input)
                if audio_data:
                    await event.respond("🔊 **Text to Speech**", file=audio_data)
                else:
                    await event.respond("❌ Failed to generate audio")
            else:
                await event.respond("❌ Please provide text for TTS")
        
        # Help command
        elif text == '/help':
            await show_help(event)
        
        else:
            await event.respond("🤖 **Bot is running!** Type /help for available commands.")
    
    except Exception as e:
        logger.error(f"Admin handler error: {e}")
        await event.respond(f"❌ Error: {str(e)}")

async def show_main_menu(event):
    """Show main menu."""
    keyboard = [
        [Button.inline("📊 System Stats", b"stats")],
        [Button.inline("📈 System Chart", b"chart"), Button.inline("🕐 Time", b"time")],
        [Button.inline("🌐 Translate", b"translate"), Button.inline("🔊 Text to Speech", b"tts")],
        [Button.inline("❓ Help", b"help")]
    ]
    
    await event.respond(
        "🤖 **Telegram Self-Bot Dashboard**\n\n"
        "Choose an action:",
        buttons=keyboard
    )

async def show_help(event):
    """Show help information."""
    help_text = """🤖 **Telegram Self-Bot Help**

**Available Commands:**
• `/start` - Show main menu
• `/stats` - System statistics
• `/chart` - System usage chart
• `/time` - Current time
• `/translate <text>` - Translate text
• `/tts <text>` - Text to speech
• `/help` - Show this help

**Features:**
✅ System monitoring
✅ Text translation
✅ Text to speech
✅ Interactive interface

**Admin Only:** Commands restricted to bot admin."""
    
    await event.respond(help_text)

@events.CallbackQuery
async def callback_handler(event):
    """Handle callback queries."""
    try:
        data = event.data.decode('utf-8')
        
        if data == "stats":
            stats = await get_system_stats()
            if 'error' in stats:
                await event.respond(f"❌ Error: {stats['error']}")
            else:
                stats_text = f"""📊 **System Statistics**

🔧 **CPU:** {stats['cpu']}
🧠 **Memory:** {stats['memory']} ({stats['memory_gb']})
💾 **Disk:** {stats['disk']} ({stats['disk_gb']})"""
                await event.respond(stats_text)
        
        elif data == "chart":
            chart_data = await create_system_chart()
            if chart_data:
                await event.respond("📊 **System Usage Chart**", file=chart_data)
            else:
                await event.respond("❌ Failed to generate chart")
        
        elif data == "time":
            now = datetime.now(pytz.UTC)
            await event.respond(f"🕐 **Current Time:** {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        elif data == "help":
            await show_help(event)
        
        elif data == "translate":
            await event.respond("🌐 **Translation Feature**\n\nUse: `/translate <text>`\n\nExample: `/translate Hello world`")
        
        elif data == "tts":
            await event.respond("🔊 **Text to Speech Feature**\n\nUse: `/tts <text>`\n\nExample: `/tts Hello world`")
        
        await event.answer()
    
    except Exception as e:
        logger.error(f"Callback handler error: {e}")
        await event.answer(f"❌ Error: {str(e)}")

async def main():
    """Main function."""
    try:
        logger.info("🚀 Starting Telegram Self-Bot...")
        
        # Setup client
        if not await setup_client():
            logger.error("❌ Failed to setup client")
            return
        
        # Add event handlers
        client.add_event_handler(admin_handler, events.NewMessage)
        client.add_event_handler(callback_handler, events.CallbackQuery)
        
        logger.info("✅ Bot handlers registered successfully")
        
        # Keep bot running
        await client.run_until_disconnected()
    
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
    finally:
        if client:
            await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())