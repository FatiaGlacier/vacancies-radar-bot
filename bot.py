from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler
from api.remotive import get_jobs_number
from config import get_bot_token, get_rapidapi_token
from db.engine import AsyncSessionLocal, create_tables
from db.repositories.user_repository import create_user, get_user
from db.models import user
import asyncio
import sys

START, UNREGISTERED, REGISTRATION, LANGUAGES, TECHNOLOGIES, LEVEL, WORK_FORMAT, NOTICING, MENU, JOBS, PROFILE, SAVED= range(12)

unregistered_reply_keyboard = [
    ["Register"],
]
unregisterd_markup = ReplyKeyboardMarkup(unregistered_reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

menu_reply_keyboard = [
    ["Jobs", "Profile", "Saved"],
]
menu_markup = ReplyKeyboardMarkup(menu_reply_keyboard, resize_keyboard=True, one_time_keyboard=False)

jobs_reply_keyboard = [
    ["Menu"],
]
jobs_reply_markup = ReplyKeyboardMarkup(jobs_reply_keyboard, resize_keyboard=True, one_time_keyboard=False)

profile_reply_keyboard = [
    ["Menu"],
]
profile_reply_markup = ReplyKeyboardMarkup(profile_reply_keyboard, resize_keyboard=True, one_time_keyboard=False)

saved_reply_keyboard = [
    ["Menu"],
]
saved_reply_markup = ReplyKeyboardMarkup(saved_reply_keyboard, resize_keyboard=True, one_time_keyboard=False)

async def post_init(application):
    print("Creating tables...")
    await create_tables()
    print("Tables created!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_name = update.message.from_user.first_name

        print("START")

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
                await update.message.reply_text(
                    f"You are NEW user! For registration click registration button",
                    reply_markup=unregisterd_markup
                ) 
                return REGISTRATION
            else:
                await update.message.reply_text(
                    f"Welcome back! Menu is bellow",
                    reply_markup=menu_markup
                )
                return MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Menu",
        reply_markup=menu_markup
    )
    return MENU

async def jobs_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Jobs",
        reply_markup=jobs_reply_markup
    )
    return JOBS

async def profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Profile",
        reply_markup=profile_reply_markup
    )
    return PROFILE

async def saved_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Saved",
        reply_markup=profile_reply_markup
    )
    return SAVED

async def unregistered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return

async def fall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
                    f"Something went wrong"
                )
    start()

if __name__ == '__main__':
    if sys.platform == "win32":
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = Application.builder().token(get_bot_token()).post_init(post_init).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(filters.Regex("^Jobs$"), jobs_menu),
                MessageHandler(filters.Regex("^Profile$"), profile_menu),
                MessageHandler(filters.Regex("^Saved$"), saved_menu)
            ],
            JOBS: [
                MessageHandler(filters.Regex("^Menu$"), main_menu),
            ],
            PROFILE: [
                MessageHandler(filters.Regex("^Menu$"), main_menu),
            ],
            SAVED: [
                MessageHandler(filters.Regex("^Menu$"), main_menu),
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), fall)]
    )
    app.add_handler(conv_handler)

    print("Starting bot...")
    app.run_polling(poll_interval=1)