import os
from dotenv import load_dotenv
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

API_TOKEN = os.getenv("API_TOKEN")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am Vacancies radar bot")

if __name__ == '__main__':
    print("Starting bot")
    app = Application.builder().token(API_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    print("Polling...")
    app.run_polling(poll_interval=3)