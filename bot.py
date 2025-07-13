import asyncio
import logging
import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)
from telegram.constants import ParseMode
from config import TELEGRAM_TOKEN, MAX_FILE_SIZE, validate_config
from spotify_downloader import SpotifyDownloader
from utils import is_valid_spotify_url, format_file_size, logger

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class SpotifyBot:
    def __init__(self):
        self.downloader = SpotifyDownloader()
        self.active_downloads = {}

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_message = (
            "🎵 *Welcome to Spotify Downloader Bot!*\n\n"
            "Send me a Spotify track link or use `/song <spotify_url>`."
        )
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_message = (
            "🔧 *Bot Commands*\n\n"
            "`/start` - Welcome message\n"
            "`/help` - Show help\n"
            "`/song <url>` - Download a song from Spotify URL\n\n"
            "Send a Spotify track URL to download the song."
        )
        await update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)

    async def song_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide a Spotify URL.\nUsage: `/song <spotify_url>`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        spotify_url = context.args[0]
        await self.process_spotify_url(update, context, spotify_url)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_text = update.message.text.strip()
        if 'spotify.com' in message_text:
            await self.process_spotify_url(update, context, message_text)
        else:
            await update.message.reply_text(
                "🎵 Send me a Spotify track URL to download the song!\nUse `/help` for more information.",
                parse_mode=ParseMode.MARKDOWN
            )

    async def process_spotify_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
        user_id = update.effective_user.id
        if user_id in self.active_downloads:
            await update.message.reply_text(
                "⏳ You already have a download in progress. Please wait."
            )
            return
        if not is_valid_spotify_url(url):
            await update.message.reply_text(
                "❌ Invalid Spotify URL. Please provide a valid Spotify track link."
            )
            return
        self.active_downloads[user_id] = True
        try:
            status_message = await update.message.reply_text(
                "🔄 *Processing your request...*\nGetting track information...",
                parse_mode=ParseMode.MARKDOWN
            )
            await self.download_and_send(update, context, url, status_message)
        except Exception as e:
            logger.error(f"Error processing URL for user {user_id}: {e}")
            await update.message.reply_text(
                "❌ An error occurred while processing your request."
            )
        finally:
            self.active_downloads.pop(user_id, None)

    async def download_and_send(self, update: Update, context: ContextTypes.DEFAULT_TYPE, url: str, status_message):
        user_id = update.effective_user.id
        try:
            await status_message.edit_text(
                "🔄 *Processing your request...*\n✅ Got track info\n🔍 Searching YouTube...",
                parse_mode=ParseMode.MARKDOWN
            )
            result = self.downloader.download_track(url)
            if not result:
                await status_message.edit_text(
                    "❌ *Download failed*\nCould not find or download the track.",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            file_path, track_info = result
            file_size = os.path.getsize(file_path)
            if file_size > MAX_FILE_SIZE:
                self.downloader.cleanup_file(file_path)
                await status_message.edit_text(
                    f"❌ *File too large*\nThe file ({format_file_size(file_size)}) exceeds Telegram's limit.",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            await status_message.edit_text(
                "🔄 *Processing your request...*\n✅ Got track info\n✅ Found YouTube video\n✅ Downloaded audio\n✅ Added metadata\n📤 Sending file...",
                parse_mode=ParseMode.MARKDOWN
            )
            with open(file_path, 'rb') as audio_file:
                await context.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=audio_file,
                    title=f"{track_info['artist']} - {track_info['name']}",
                    performer=track_info['artist'],
                    duration=int(track_info['duration_ms'] / 1000),
                    filename=f"{track_info['artist']} - {track_info['name']}.mp3"
                )
            success_text = (
                f"✅ *Download Complete!*\n\n"
                f"🎵 **{track_info['name']}**\n"
                f"👤 **{track_info['artist']}**\n"
                f"💿 **{track_info['album']}**\n"
                f"📁 **Size:** {format_file_size(file_size)}\n"
                f"🎧 **Quality:** 320kbps MP3\n\nEnjoy your music! 🎶"
            )
            await status_message.edit_text(success_text, parse_mode=ParseMode.MARKDOWN)
            self.downloader.cleanup_file(file_path)
        except Exception as e:
            logger.error(f"Error in download_and_send for user {user_id}: {e}")
            await status_message.edit_text(
                "❌ *Download failed*\nAn error occurred during the download process.",
                parse_mode=ParseMode.MARKDOWN
            )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f"Exception while handling an update: {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again later."
            )

def main():
    try:
        validate_config()
        bot = SpotifyBot()
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler("start", bot.start_command))
        application.add_handler(CommandHandler("help", bot.help_command))
        application.add_handler(CommandHandler("song", bot.song_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
        application.add_error_handler(bot.error_handler)
        logging.info("Starting Spotify Downloader Bot...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main() 