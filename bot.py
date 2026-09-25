import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

TOKEN = "8821749427:AAFtRZVS3qUNQgP0sadNBYfnzrc-7O0mOrA"

APK_URL = "https://t.me/+ui28nFh4I5o0NjMx"
VIDEO_URL = "https://raw.githubusercontent.com/telegramdesktop/tdesktop/dev/Telegram/Resources/art/video.mp4"

async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = user.id

    # 1. टेक्स्ट मैसेज
    welcome_msg = (
        f"Hello {user.first_name}! 🎉\n\n"
        "HELLO USER CONGRATULATIONS ✨\n"
        "YOU ARE A PREMIUM USER NOW 🔥\n\n\n"
        "COLOUR TRADING LOSS RECOVER CHANNEL LINK 🔥\n"
        "[100% LOSS RECOVER HOGA YAHA]\n"
        "JOIN HERE ⬇️ (EXPIRE IN 5 MINUTES)"
    )

    # 2. बटन सेट करना
    keyboard = [
        [InlineKeyboardButton("📲 Join Telegram Channel", url=APK_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 3. मैसेज और बटन भेजना
    try:
        await context.bot.send_video(
            chat_id=chat_id,
            video=VIDEO_URL,
            caption=welcome_msg,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=chat_id,
            text=welcome_msg,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(ChatJoinRequestHandler(approve_request))
    
    print("Bot is running with buttons...")
    app.run_polling()

if __name__ == "__main__":
    main()
