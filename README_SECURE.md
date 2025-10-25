# 🤖 Telegram Self-Bot System - Secure Edition

A secure Telegram self-bot management system with dual-bot architecture, optimized for cloud deployment.

## 🔒 Security Features

- **Environment Variables**: All sensitive credentials stored in environment variables
- **No Hardcoded Secrets**: No API keys or tokens in source code
- **Production Ready**: Optimized for cloud deployment
- **Admin Protection**: Commands restricted to authorized admin

## 🏗️ System Architecture

### Main Bot (`self_render_secure.py`)
- **Purpose**: Core account management and monitoring
- **Features**:
  - System statistics and monitoring
  - Interactive dashboard with inline buttons
  - Text translation services
  - Text-to-speech functionality
  - Real-time system charts
  - Admin command interface

### Helper Bot (`helper_render_secure.py`)
- **Purpose**: Management panel and webhook server
- **Features**:
  - Flask web framework
  - REST API endpoints
  - Webhook processing
  - Admin notification system
  - Health monitoring

## 🚀 Quick Deployment

### 1. Environment Variables Setup

Configure these environment variables in your deployment platform:

```bash
# Required for Main Bot
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_ADMIN_ID=your_admin_user_id

# Authentication (choose ONE method)
# Method 1: Session String (Recommended)
TELEGRAM_SESSION_STRING=your_session_string_here

# Method 2: Traditional Login (not recommended for cloud)
TELEGRAM_PHONE=+1234567890
TELEGRAM_PASSWORD=your_password

# Required for Helper Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_ID=your_admin_user_id

# Optional Configuration
WEBHOOK_PORT=5000
WEBHOOK_HOST=0.0.0.0
TELEGRAM_SESSION_NAME=self_bot
```

### 2. Generate Session String (Recommended)

#### Option A: Use Session String Generator
1. **Run the generator script:**
   ```bash
   python session_generator.py
   ```
2. **Enter your credentials when prompted:**
   - API ID and API Hash
   - Phone number
   - Verification code
   - 2FA password (if enabled)
3. **Copy the session string** from the output
4. **Add to Render environment:**
   ```
   TELEGRAM_SESSION_STRING=your_generated_session_string
   ```

#### Option B: Manual Session Creation
1. **Install dependencies locally:**
   ```bash
   pip install telethon
   ```
2. **Run authentication script:**
   ```bash
   python -c "
   from telethon import TelegramClient
   client = TelegramClient('session', API_ID, API_HASH)
   client.start()
   session_string = client.session.save()
   print(session_string)
   "
   ```

### 3. Install Dependencies

```bash
pip install -r requirements_secure.txt
```

### 3. Run the System

**Main Bot:**
```bash
python self_render_secure.py
```

**Helper Bot:**
```bash
python helper_render_secure.py
```

## 🌐 API Endpoints (Helper Bot)

### Status Check
```
GET /status
```
Returns system status and bot information.

### Admin Information
```
GET /admin/info
```
Returns admin user information.

### Send Message
```
POST /send
Content-Type: application/json

{
  "message": "Your message here"
}
```
Sends message to admin.

### Webhook Endpoint
```
POST /webhook
Content-Type: application/json

{
  "type": "message",
  "message": "Webhook message",
  "chat_id": 123456789
}
```
Handles webhook requests.

### Health Check
```
GET /health
```
Returns health status.

## 📱 Admin Commands

### Main Bot Commands
- `/start` - Show main menu
- `/stats` - System statistics
- `/chart` - System usage chart
- `/time` - Current time
- `/translate <text>` - Translate text
- `/tts <text>` - Text to speech
- `/help` - Show help

### Interactive Menu
The bot provides inline keyboard menu for easy navigation.

## 🛠️ System Requirements

- Python 3.8+
- Internet connection
- Valid Telegram API credentials
- Sufficient server resources for monitoring

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_API_ID` | ✅ | Your Telegram API ID |
| `TELEGRAM_API_HASH` | ✅ | Your Telegram API Hash |
| `TELEGRAM_ADMIN_ID` | ✅ | Admin user ID |
| `TELEGRAM_BOT_TOKEN` | ✅ | Bot token for helper |
| `TELEGRAM_SESSION_STRING` | ⚡ | Session string (recommended) |
| `TELEGRAM_SESSION_NAME` | ❌ | Session file name (default: self_bot) |
| `WEBHOOK_PORT` | ❌ | Webhook server port (default: 5000) |
| `WEBHOOK_HOST` | ❌ | Webhook server host (default: 0.0.0.0) |

### Authentication Methods

#### Method 1: Session String (Recommended)
- **Secure**: No passwords stored in environment
- **Portable**: Easy backup and restoration
- **Cloud-friendly**: Perfect for deployment platforms

#### Method 2: Traditional Login
- **Variables**: `TELEGRAM_PHONE`, `TELEGRAM_PASSWORD`
- **Less secure**: Password stored in environment
- **Manual**: Requires manual login on server startup

## 📊 Features

### System Monitoring
- CPU usage monitoring
- Memory usage tracking
- Disk space monitoring
- Real-time charts and graphs

### Translation Services
- Google Translate integration
- Multiple language support
- Fast text translation

### Audio Features
- Text-to-speech conversion
- Multiple language TTS support

### Management Interface
- Web-based admin panel
- REST API for integration
- Webhook support for external systems

## 🔐 Security Considerations

1. **Never commit** environment variables to version control
2. **Use secrets management** in your deployment platform
3. **Rotate credentials** regularly
4. **Monitor access logs** for unusual activity
5. **Limit admin access** to authorized users only

## 🚨 Troubleshooting

### Common Issues

**Bot not connecting:**
- Verify API credentials
- Check admin ID is correct
- Ensure internet connection

**Webhook not working:**
- Check WEBHOOK_HOST and WEBHOOK_PORT
- Verify firewall settings
- Check Flask logs

**Permission errors:**
- Ensure proper file permissions
- Check Python version compatibility

### Logs
- Main bot log: `bot.log`
- Helper bot log: `helper_bot.log`

## 📄 License

This project is for educational purposes. Use responsibly and comply with Telegram's Terms of Service.

## 🤝 Contributing

Contributions are welcome! Please follow security best practices:
- Never include credentials in code
- Use environment variables
- Add proper error handling
- Include tests for new features

---

**⚠️ Important**: This system requires valid Telegram API credentials and should be used in compliance with Telegram's Terms of Service.