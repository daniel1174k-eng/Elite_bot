import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Hello! Welcome to Elite_bot.\n\n"
        "This bot helps you generate content, answer questions, "
        "and automate tasks quickly and easily.\n"
        "Available 24/7."
    )

    await update.message.reply_text(welcome_text)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_text = (
        "🤖 Elite_bot Ready!\n\n"
        "I am here to help you generate content, answer questions, "
        "and automate tasks.\n"
        "Tell me, what can I do for you today?"
    )

    await update.message.reply_text(reply_text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, help_handler)
    )

    print("Bot is running...")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
