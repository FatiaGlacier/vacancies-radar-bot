import os
from dotenv import load_dotenv
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from api.remotive import get_jobs_number

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

API_TOKEN = os.getenv("BOT_TOKEN")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name

    await update.message.reply_photo(
        photo=Path("./media/start_photo.jpg"),
        caption=(
            f"Servus, {user_name}\n\n"
            f"Welcome to VanaciesRadarBot\n\n"
        )
    )

    await update.message.reply_text(f"Remotive has {get_jobs_number()} available remote jobs!")



if __name__ == '__main__':
    print("Starting bot")
    app = Application.builder().token(API_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    print("Polling...")
    app.run_polling(poll_interval=3)