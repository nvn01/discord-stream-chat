# Discord Stream Monitor

A headless Python tool that captures real-time messages and images from Discord channels using the User Gateway Protocol. Perfect for monitoring restricted channels where bots are forbidden.

## 🎯 Features

- **Event-Driven Architecture**: Zero CPU usage when idle, only activates when messages arrive
- **Multi-Channel Monitoring**: Monitor multiple text channels simultaneously
- **Automatic Image Downloads**: All images saved with `MessageID_Filename` format to prevent overwrites
- **Daily JSON Logging**: Auto-rotating log files for each day (`YYYY-MM-DD.json`)
- **User Account Support**: Uses Discord user tokens (not bot tokens) for channels that forbid bots
- **Secure Configuration**: Token stored in `.env` file, never committed to Git
- **Auto-Reconnection**: Handles disconnections gracefully with exponential backoff

## 📋 Requirements

- Python 3.8 or higher
- Discord user account (not a bot account)
- Channel IDs you want to monitor

## 🚀 Installation

1. **Clone or download this project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and fill in your values
   ```

4. **Get your Discord token**
   - Open Discord in your **browser** (not the app)
   - Press `F12` to open Developer Tools
   - Go to the **Network** tab
   - Refresh the page (`F5`)
   - Look for requests and find one with an `authorization` header
   - Copy the token value (long string of characters)
   - Paste it into `.env` as `DISCORD_TOKEN`

5. **Get channel IDs**
   - Enable Developer Mode in Discord:
     - User Settings → Advanced → Developer Mode
   - Right-click on any channel you want to monitor
   - Select "Copy ID"
   - Add all channel IDs to `.env` as comma-separated values:
     ```
     CHANNEL_IDS=123456789012345678,987654321098765432
     ```

## 🎮 Usage

**Start the monitor:**
```bash
python main.py
```

**Stop the monitor:**
- Press `Ctrl+C` in the terminal

## 📁 Project Structure

```
discord-stream-monitor/
├── main.py              # Application entry point
├── config.py           # Configuration loader
├── monitor.py          # Discord monitoring logic
├── utils/
│   ├── logger.py       # Daily JSON logging system
│   ├── downloader.py   # Image download handler
│   └── alerts.py       # Alert system
├── logs/               # Daily message logs (YYYY-MM-DD.json)
└── downloads/          # Downloaded images (MessageID_Filename)
```

## 📝 Log Format

Each day's log file (`logs/YYYY-MM-DD.json`) contains an array of message objects:

```json
[
  {
    "message_id": "123456789",
    "timestamp": "2026-01-06T22:27:42+07:00",
    "author": "Username#1234",
    "author_id": "987654321",
    "channel_id": "111222333",
    "channel_name": "general",
    "content": "Message text",
    "attachments": [
      {
        "filename": "image.png",
        "url": "https://...",
        "size": 102400,
        "downloaded": true,
        "local_path": "downloads/123456789_image.png"
      }
    ]
  }
]
```

## 🔐 Security Notes

- **Never commit `.env` file** - It contains your Discord token
- **Never share your token** - Anyone with your token can access your account
- **Token expiration** - If your token expires, the monitor will alert you and stop
- **Rate limits** - Discord may rate limit excessive activity

## ⚠️ Important Warnings

> **Discord Terms of Service**
> 
> Using user accounts for automation may violate Discord's Terms of Service. Use this tool responsibly and only in private channels or with proper authorization.

> **Account Security**
> 
> If Discord detects unusual activity, your account may be flagged or locked. Use at your own risk.

## 🔮 Future Features (Planned)

- [ ] Desktop notifications for new messages
- [ ] Webhook alerts for critical events
- [ ] OCR integration for extracting text from images
- [ ] Image analysis/filtering
- [ ] Message keyword filtering
- [ ] Export to other formats (CSV, Database)

## 🛠️ Troubleshooting

**"Invalid token" error**
- Make sure you copied the token correctly from browser DevTools
- Ensure there's no "Bot " prefix in your token
- Try refreshing Discord and getting a new token

**"Channel not found" warning**
- Make sure you have access to the channel
- Verify the channel ID is correct
- Check if the channel still exists

**Images not downloading**
- Check your internet connection
- Verify the `downloads/` folder exists and is writable
- Check console for specific error messages

## 📄 License

This project is for educational purposes. Use responsibly and in accordance with Discord's Terms of Service.
