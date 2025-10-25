#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Helper Bot - Secure Version
Management panel with Flask webhooks
Uses environment variables for sensitive data
"""

import os
import logging
import asyncio
from flask import Flask, request, jsonify, send_file
from telethon import TelegramClient, events
from telethon.tl.types import User
import aiohttp
import json
from datetime import datetime
import io

# Secure configuration using environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('TELEGRAM_ADMIN_ID', '0'))
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '5000'))
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', '0.0.0.0')

if not all([BOT_TOKEN, ADMIN_ID]):
    logging.error("❌ Missing required environment variables:")
    logging.error("Please set: TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_ID")
    exit(1)

# Initialize Flask app
app = Flask(__name__)

# Global variables
client = None
admin_user = None
webhook_active = False

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('helper_bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class HelperBot:
    """Helper bot class for management operations."""
    
    def __init__(self):
        self.client = None
        self.admin_id = ADMIN_ID
        self.bot_token = BOT_TOKEN
        
    async def setup_client(self):
        """Setup Telegram client."""
        try:
            if API_ID and API_HASH:
                self.client = TelegramClient('helper_bot', API_ID, API_HASH)
                await self.client.start(bot_token=self.bot_token)
                
                # Get admin user info
                admin_entity = await self.client.get_entity(self.admin_id)
                logger.info(f"✅ Helper bot connected as {admin_entity.first_name}")
                return True
            else:
                logger.warning("⚠️ API_ID/API_HASH not provided, client features limited")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to setup client: {e}")
            return False
    
    async def send_message_to_admin(self, message):
        """Send message to admin."""
        try:
            if self.client:
                await self.client.send_message(self.admin_id, message)
                logger.info(f"📨 Message sent to admin: {message[:50]}...")
                return True
            else:
                logger.warning("⚠️ Client not available, cannot send message")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False
    
    async def get_admin_info(self):
        """Get admin information."""
        try:
            if self.client:
                admin = await self.client.get_entity(self.admin_id)
                return {
                    'id': admin.id,
                    'first_name': admin.first_name,
                    'username': admin.username,
                    'phone': getattr(admin, 'phone', None)
                }
            else:
                return {'error': 'Client not available'}
        except Exception as e:
            return {'error': str(e)}

# Global helper bot instance
helper_bot = HelperBot()

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Handle webhook requests."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        logger.info(f"📥 Webhook received: {data.get('type', 'unknown')}")
        
        # Handle different webhook types
        webhook_type = data.get('type')
        
        if webhook_type == 'message':
            await handle_message_webhook(data)
        elif webhook_type == 'status':
            await handle_status_webhook(data)
        elif webhook_type == 'admin_request':
            await handle_admin_request_webhook(data)
        else:
            logger.warning(f"⚠️ Unknown webhook type: {webhook_type}")
        
        return jsonify({'status': 'success', 'message': 'Webhook processed'})
    
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

async def handle_message_webhook(data):
    """Handle message webhook."""
    try:
        message = data.get('message', '')
        chat_id = data.get('chat_id')
        
        if chat_id == ADMIN_ID:
            # Send to admin via bot
            response_message = f"🤖 **Webhook Message:**\n{message}"
            await helper_bot.send_message_to_admin(response_message)
        
    except Exception as e:
        logger.error(f"❌ Message webhook error: {e}")

async def handle_status_webhook(data):
    """Handle status webhook."""
    try:
        status = data.get('status', 'unknown')
        message = data.get('message', '')
        
        response_message = f"📊 **Status Update:**\nStatus: {status}\nMessage: {message}"
        await helper_bot.send_message_to_admin(response_message)
        
    except Exception as e:
        logger.error(f"❌ Status webhook error: {e}")

async def handle_admin_request_webhook(data):
    """Handle admin request webhook."""
    try:
        action = data.get('action', '')
        parameters = data.get('parameters', {})
        
        response_message = f"🔧 **Admin Request:**\nAction: {action}\nParameters: {json.dumps(parameters, indent=2)}"
        await helper_bot.send_message_to_admin(response_message)
        
    except Exception as e:
        logger.error(f"❌ Admin request webhook error: {e}")

@app.route('/status', methods=['GET'])
def get_status():
    """Get bot status."""
    try:
        status_data = {
            'bot_token': 'set' if BOT_TOKEN else 'not set',
            'admin_id': ADMIN_ID,
            'webhook_active': webhook_active,
            'timestamp': datetime.now().isoformat(),
            'flask_running': True
        }
        
        # Add client info if available
        if helper_bot.client:
            status_data['client_connected'] = True
        else:
            status_data['client_connected'] = False
        
        return jsonify(status_data)
    
    except Exception as e:
        logger.error(f"❌ Status error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/admin/info', methods=['GET'])
async def get_admin_info():
    """Get admin information."""
    try:
        admin_info = await helper_bot.get_admin_info()
        return jsonify(admin_info)
    
    except Exception as e:
        logger.error(f"❌ Admin info error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/send', methods=['POST'])
async def send_message():
    """Send message to admin."""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        success = await helper_bot.send_message_to_admin(message)
        
        if success:
            return jsonify({'status': 'success', 'message': 'Message sent'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send message'}), 500
    
    except Exception as e:
        logger.error(f"❌ Send message error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': 'running'
    })

async def setup_bot():
    """Setup the helper bot."""
    try:
        logger.info("🚀 Setting up Helper Bot...")
        
        # Setup client
        await helper_bot.setup_client()
        
        logger.info("✅ Helper Bot setup completed")
        return True
    
    except Exception as e:
        logger.error(f"❌ Bot setup error: {e}")
        return False

async def start_webhook_server():
    """Start the webhook server."""
    try:
        logger.info(f"🌐 Starting webhook server on {WEBHOOK_HOST}:{WEBHOOK_PORT}")
        
        # Run Flask app
        app.run(
            host=WEBHOOK_HOST,
            port=WEBHOOK_PORT,
            debug=False,
            use_reloader=False
        )
    
    except Exception as e:
        logger.error(f"❌ Webhook server error: {e}")

async def main():
    """Main function."""
    try:
        logger.info("🚀 Starting Telegram Helper Bot...")
        
        # Setup bot
        if not await setup_bot():
            logger.error("❌ Failed to setup bot")
            return
        
        # Start webhook server
        await start_webhook_server()
    
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
    finally:
        if helper_bot.client:
            await helper_bot.client.disconnect()

if __name__ == "__main__":
    # Start the bot
    asyncio.run(main())