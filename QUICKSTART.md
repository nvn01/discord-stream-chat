# 🚀 Quick Start Guide - Discord Stream Monitor

## Step 1: Get Your Discord Token

1. Open **Discord in your browser** (not the desktop app!)
2. Press **F12** to open Developer Tools
3. Go to the **Network** tab
4. Press **F5** to refresh the page
5. Look for any request in the list
6. Click on it and find the **Headers** section
7. Scroll down to find `authorization:` header
8. Copy the entire token (it's a long string like `mfa.xxxxxxxxxxx...`)

## Step 2: Get Channel IDs

1. In Discord, go to **User Settings** → **Advanced** → Enable **Developer Mode**
2. Right-click on any text channel you want to monitor
3. Select **Copy ID**
4. Repeat for all channels you want to monitor

## Step 3: Configure the Application

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file and fill in your values:
   ```
   DISCORD_TOKEN=your_token_here
   CHANNEL_IDS=123456789012345678,987654321098765432
   ```

## Step 4: Run the Monitor

```bash
python main.py
```

You should see:
- ✓ Logged in as [your username]
- 📡 Monitoring X channel(s)
- 🚀 Discord Stream Monitor Started

## Step 5: Test It

1. Send a message in one of the monitored channels
2. Upload an image to that channel
3. Check:
   - `logs/` folder for a JSON file with today's date
   - `downloads/` folder for downloaded images

## What to Expect

### Console Output
You'll see real-time updates for every message:
```
💬 [22:30:15] Username#1234 in #general
   Hello world! [1 attachment(s)]
⬇️  Downloaded: 123456789_image.png (102,400 bytes)
```

### Log Files
`logs/2026-01-06.json` will contain all messages in JSON format

### Downloaded Images
`downloads/123456789_image.png` - Images named with message ID to prevent overwrites

## Stopping the Monitor

Press **Ctrl+C** in the terminal

---

## ⚠️ Important Notes

- **Security**: Never share your Discord token!
- **Terms of Service**: Using user accounts for automation may violate Discord's ToS
- **Token Expiration**: If your token expires, you'll get an alert - just get a new token

## 🆘 Troubleshooting

**"Invalid token" error**
→ Make sure you copied the full token from the browser
→ Don't include "Bot " prefix
→ Get a fresh token

**"Channel not found" warning**
→ Make sure you have access to the channel
→ Verify the channel ID is correct

**Nothing happening**
→ Send a test message to the monitored channel
→ Check that CHANNEL_IDS is not empty
