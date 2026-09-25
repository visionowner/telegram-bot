import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ChatJoinRequestHandler, MessageHandler, filters, ContextTypes

TOKEN = "8821749427:AAHZbUq0ZVVCyAPZZgKJ6Cmcih8gZB7HThU"
APK_URL = "https://t.me/+ui28nFh4I5o0NjMx"

# 1. Health check server for Render (24/7 Keep Alive)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Helper function to send welcome message with join link button
async def send_welcome_message(bot, chat_id, first_name):
    welcome_msg = (
        f"Hello {first_name}! 🎉\n\n"
        "HELLO USER CONGRATULATIONS ✨\n"
        "YOU ARE A PREMIUM USER NOW 🔥\n\n\n"
        "COLOUR TRADING LOSS RECOVER CHANNEL LINK 🔥\n"
        "[100% LOSS RECOVER HOGA YAHA]\n"
        "JOIN HERE ⬇️ (EXPIRE IN 5 MINUTES)"
    )

    keyboard = [[InlineKeyboardButton("📲 Join Telegram Channel", url=APK_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=welcome_msg,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"DM Error: {e}")

# 2. Direct /start Command Handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await send_welcome_message(context.bot, user.id, user.first_name)

# 3. Join Request Handler (Triggers when user requests to join channel)
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    await send_welcome_message(context.bot, user.id, user.first_name)

# 4. Channel Auto Reaction Handler (Triggers on new channel posts)
async def auto_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.set_message_reaction(
            chat_id=update.effective_chat.id,
            message_id=update.effective_message.message_id,
            reaction=["🔥", "👍", "❤️"]
        )
        print(f"Reaction successfully added to post {update.effective_message.message_id}")
    except Exception as e:
        print(f"Reaction Error: {e}")

def main():
    # Start Keep-Alive Web Server
    Thread(target=run_web_server, daemon=True).start()

    # Build Telegram Bot Application
    app = Application.builder().token(TOKEN).build()
    
    # Handlers Registration
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, auto_react))
    
    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
