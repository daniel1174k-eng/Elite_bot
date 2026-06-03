import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Initialize Flask app
app = Flask(__name__)

# Retrieve environment variables
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL") # Render provides this automatically

# Initialize Telegram Application
telegram_app = Application.builder().token(TOKEN).build()

# Define the /start command response
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Hello! Welcome to **Elite_bot**.\n\n"
        "This bot helps you generate content, answer questions, and automate tasks quickly and easily.\n"
        "Available 24/7."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# Define a default help/response handler for other messages
async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_text = (
        "🤖 **Elite_bot Ready!**\n\n"
        "I am here to help you generate content, answer questions, and automate tasks.\n"
        "Tell me, what can I do for you today?"
    )
    await update.message.reply_text(reply_text, parse_mode="Markdown")

# Register handlers to the telegram app
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help_handler))

# Flask route to receive updates from Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
async def respond():
    # Ensure the background logic is initialized
    if not telegram_app.running:
        await telegram_app.initialize()
    
    # Process the update from Telegram
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK", 200

# Route to automatically set up the webhook on Telegram's side
@app.route("/", methods=["GET"])
async def setup_webhook():
    if not telegram_app.running:
        await telegram_app.initialize()
    
    # Tell Telegram where to send messages
    webhook_target = f"{WEBHOOK_URL}/{TOKEN}"
    await telegram_app.bot.set_webhook(url=webhook_target)
    return f"Elite_bot Webhook successfully configured to: {webhook_target}", 200
