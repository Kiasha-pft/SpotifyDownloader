# 🎵 Spotify Telegram Downloader Bot

A powerful Telegram bot that downloads songs from Spotify as high-quality MP3 files. The bot uses YouTube as an intermediary to find and download audio, then adds proper metadata and album art.
💫 This bot is currently running at : @BoroBiaSpoti_Bot 

## ✨ Features

- **High Quality Downloads**: 320kbps MP3 files
- **Automatic Metadata**: Artist, title, album, and album art
- **Easy to Use**: Just send a Spotify track URL
- **Real-time Status**: Progress updates during download
- **File Size Validation**: Ensures files fit Telegram's limits
- **Error Handling**: Comprehensive error handling and user feedback

## 🛠️ Prerequisites

Before running this bot, you'll need:

1. **Python 3.8+** installed on your system
2. **FFmpeg** installed for audio conversion
3. **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)
4. **Spotify API Credentials** from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

### Installing FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Using Scoop
scoop install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
# Using Homebrew
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

## 🚀 Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd spotify_telegram_bot
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env with your credentials
   nano .env
   ```

4. **Get your credentials:**

   **Telegram Bot Token:**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Use `/newbot` command
   - Follow instructions to create your bot
   - Copy the token to `TELEGRAM_TOKEN` in `.env`

   **Spotify API Credentials:**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Copy Client ID and Client Secret to `.env`

## 📝 Configuration

Edit your `.env` file with the following variables:

```env
# Required
TELEGRAM_TOKEN=your_telegram_bot_token_here
SPOTIPY_CLIENT_ID=your_spotify_client_id_here
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret_here

# Optional
DOWNLOAD_PATH=downloads
```

## 🍪 YouTube Cookies (Optional, for Restricted Videos)

Some YouTube videos require you to be logged in to download them (age-restricted, region-locked, or protected content). You can provide your YouTube cookies to the bot for these cases.

**How to add cookies.txt:**
1. Install a browser extension like [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/) for Chrome or Firefox.
2. Log in to youtube.com with your account (a throwaway account is recommended).
3. Use the extension to export your cookies as `cookies.txt`.
4. Place the `cookies.txt` file in the root of your project directory.

The bot will automatically use `cookies.txt` if it is present.

## 🎯 Usage

1. **Start the bot:**
   ```bash
   python bot.py
   ```

2. **Use the bot:**
   - Send `/start` to see the welcome message
   - Send a Spotify track URL (e.g., `https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh`)
   - Or use `/song <spotify_url>` command
   - Wait for the download to complete
   - Receive your MP3 file!

## 📁 Project Structure

```
spotify_telegram_bot/
│
├── bot.py                     # Main bot entry point
├── spotify_downloader.py     # Core download logic
├── utils.py                  # Helper functions
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── env.example              # Environment variables template
└── README.md                # This file
```

## 🔧 How It Works

1. **URL Processing**: Bot extracts track ID from Spotify URL
2. **Spotify API**: Gets track metadata (title, artist, album, etc.)
3. **YouTube Search**: Searches YouTube for the best matching video
4. **Audio Download**: Downloads audio using yt-dlp
5. **Conversion**: Converts to MP3 with FFmpeg
6. **Metadata**: Adds ID3 tags and album art
7. **Delivery**: Sends file to user via Telegram

## 🛡️ Legal Notice

This bot is for educational purposes. Please respect copyright laws and only download music you have the right to access. The bot downloads from YouTube, which may have different licensing terms than Spotify.

## 🐛 Troubleshooting

### Common Issues

**"Invalid Spotify URL"**
- Make sure you're using a Spotify track URL (not album or playlist)
- URL should look like: `https://open.spotify.com/track/...`

**"Download failed"**
- Check your internet connection
- Some tracks might not be available on YouTube
- Try a different track

**"File too large"**
- Telegram has a 50MB file size limit
- Try downloading shorter tracks

**FFmpeg not found**
- Make sure FFmpeg is installed and in your system PATH
- Restart your terminal after installing FFmpeg

### Logs

The bot logs all activities. Check the console output for detailed error messages.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This bot is provided as-is for educational purposes. Users are responsible for complying with local copyright laws and terms of service.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all prerequisites are installed
3. Verify your credentials are correct
4. Check the console logs for error messages

---

**Enjoy your music! 🎶** 
