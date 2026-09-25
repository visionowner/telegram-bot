import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ChatJoinRequestHandler, MessageHandler, filters, ContextTypes

TOKEN = "8821749427:AAFtRZVS3qUNQgP0sadNBYfnzrc-7O0mOrA"
APK_URL = "https://t.me/+ui28nFh4I5o0NjMx"
VIDEO_URL = "https://raw.githubusercontent.com/telegramdesktop/tdesktop/dev/Telegram/Resources/art/video.mp4"

# Health check server for Render
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# 1. Join Request Handler
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = user.id

    welcome_msg = (
        f"Hello {user.first_name}! 🎉\n\n"
        "HELLO USER CONGRATULATIONS ✨\n"
        "YOU ARE A PREMIUM USER NOW 🔥\n\n\n"
        "COLOUR TRADING LOSS RECOVER CHANNEL LINK 🔥\n"
        "[100% LOSS RECOVER HOGA YAHA]\n"
        "JOIN HERE ⬇️ (EXPIRE IN 5 MINUTES)"
    )

    keyboard = [[InlineKeyboardButton("📲 Join Telegram Channel", url=APK_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await context.bot.send_video(
            chat_id=chat_id,
            video=VIDEO_URL,
            caption=welcome_msg,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"DM Error: {e}")

# 2. Channel Auto Reaction Handler
async def auto_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.set_message_reaction(
            chat_id=update.effective_chat.id,
            message_id=update.effective_message.message_id,
            reaction=["🔥", "👍", "❤️"]
        )
    except Exception as e:
        print(f"Reaction Error: {e}")

def main():
    Thread(target=run_web_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, auto_react))
    
    print("Bot is running with auto-reactions...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
