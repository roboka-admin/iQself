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
from gtts import gTTS
import io
import re
from flask import Flask, jsonify, render_template_string, request

# Initialize logging immediately
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Translation services (optional due to Python 3.13 compatibility)
try:
    from googletrans import Translator
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False
    logger.warning("⚠️ googletrans not available - translation features disabled")

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

# Global variables
client = None
admin_user = None
app = Flask(__name__)

# Health check endpoints for Render
@app.route('/')
def home():
    """Home page with bot status."""
    return render_template_string("""
    <html>
        <head>
            <title>Telegram Self-Bot</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .status { padding: 20px; border-radius: 5px; margin: 10px 0; }
                .online { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
                .info { background-color: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
                h1 { color: #333; }
                .emoji { font-size: 24px; }
            </style>
        </head>
        <body>
            <h1>🤖 Telegram Self-Bot</h1>
            <div class="status online">
                <span class="emoji">✅</span> <strong>Bot Status:</strong> Running & Connected
            </div>
            <div class="status info">
                <span class="emoji">📊</span> <strong>Service:</strong> Web Worker with Telegram Integration
            </div>
            <div class="status info">
                <span class="emoji">🚀</span> <strong>Platform:</strong> Render Cloud
            </div>
            <div class="status info">
                <span class="emoji">🔧</span> <strong>Commands:</strong> /start, /stats, /chart, /time, /help
            </div>
            <p>Use the bot commands in Telegram to interact with this service.</p>
        </body>
    </html>
    """)

@app.route('/health')
def health_check():
    """Health check endpoint for Render."""
    return jsonify({
        'status': 'healthy',
        'service': 'telegram_self_bot',
        'bot_connected': client is not None and client.is_connected() if client else False,
        'timestamp': datetime.now(pytz.UTC).isoformat()
    })

@app.route('/status')
def status():
    """Detailed status endpoint."""
    try:
        system_stats = {
            'cpu': f"{psutil.cpu_percent():.1f}%",
            'memory': f"{psutil.virtual_memory().percent:.1f}%",
            'disk': f"{psutil.disk_usage('/').percent:.1f}%"
        }
    except:
        system_stats = {'error': 'Unable to get system stats'}
    
    return jsonify({
        'service': 'telegram_self_bot',
        'bot_connected': client is not None and client.is_connected() if client else False,
        'admin_id': ADMIN_ID,
        'session_string_available': bool(SESSION_STRING),
        'system_stats': system_stats,
        'timestamp': datetime.now(pytz.UTC).isoformat()
    })

# HTTP server thread
async def start_http_server():
    """Start HTTP server in a separate thread."""
    import threading
    import time
    
    def run_server():
        port = int(os.getenv('PORT', 8080))
        logger.info(f"🌐 Starting HTTP server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    
    http_thread = threading.Thread(target=run_server, daemon=True)
    http_thread.start()
    logger.info("✅ HTTP server started successfully")

# Webhook handler for Telegram updates
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram webhook."""
    try:
        # Process the update through Telethon
        update_data = request.get_json()
        if update_data:
            # The update will be processed by Telethon's event handlers
            return jsonify({'status': 'ok'})
        return jsonify({'status': 'no_data'})
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

# Initialize translator (optional)
if GOOGLETRANS_AVAILABLE:
    translator = Translator()
else:
    translator = None

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
            from telethon.sessions import StringSession
            client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
            await client.start()
        else:
            # Use traditional authentication
            logger.info("🔐 Starting traditional authentication")
            client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
            await client.start()
        
        # Get admin user info
        admin_user = await client.get_entity(ADMIN_ID)
        logger.info(f"✅ Bot connected successfully as {admin_user.first_name}")
        logger.info(f"🎯 Admin ID: {ADMIN_ID}")
        logger.info("📡 Using polling mode for message reception")
        
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
    if not translator:
        return "❌ Translation service not available"
    
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

async def admin_handler(event):
    """Handle admin messages."""
    try:
        # Check if message is from admin
        if event.sender_id != ADMIN_ID:
            return
        
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
        logger.info("🚀 Starting Telegram Self-Bot with HTTP Server...")
        
        # Start HTTP server first
        await start_http_server()
        await asyncio.sleep(2)  # Give HTTP server time to start
        
        # Setup client
        if not await setup_client():
            logger.error("❌ Failed to setup client")
            return
        
        # Add event handlers with proper filters
        client.add_event_handler(admin_handler, events.NewMessage(chats=ADMIN_ID))
        client.add_event_handler(callback_handler, events.CallbackQuery)
        
        logger.info("✅ Bot handlers registered successfully")
        logger.info("🌐 Bot is ready! Both HTTP server and Telegram bot are running")
        
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
    # Run the main async function
    asyncio.run(main())