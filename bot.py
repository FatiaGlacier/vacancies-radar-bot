from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from api.remotive import get_jobs_number
from config import get_bot_token, get_rapidapi_token
from db.engine import AsyncSessionLocal, create_tables
from db.repositories.user_repository import create_user, get_user
from db.models import user
import asyncio
import sys

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name

    await update.message.reply_photo(
        photo=Path("./media/start_photo.jpg"),
        caption=(
            f"Servus, {user_name}\n\n"
            f"Welcome to VanaciesRadarBot"
        )
    )

    user = None

    async with AsyncSessionLocal() as session:
        user = await get_user(
            session,
            telegram_id=update.message.from_user.id
            )
        
        if user is None:

            user = await create_user(
                session,
                telegram_id=update.message.from_user.id
            )
            
            await update.message.reply_text(
                f"You are NEW user! ID: {user.id} | TELEGRAM ID: {user.telegram_id}"
            ) 

        else:
            await update.message.reply_text(
                f"You are OLD user! ID: {user.id} | TELEGRAM ID: {user.telegram_id}"
            ) 

async def post_init(application):
    print("Creating tables...")
    await create_tables()
    print("Tables created!")

if __name__ == '__main__':
    if sys.platform == "win32":
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = Application.builder().token(get_bot_token()).post_init(post_init).build()

    app.add_handler(CommandHandler('start', start_command))

    print("Starting bot...")
    app.run_polling(poll_interval=3)