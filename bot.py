from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler
from api.remotive import get_jobs_number
from config import get_bot_token, get_rapidapi_token
import asyncio
import sys
import numpy as np

START, UNREGISTERED, REGISTRATION, LANGUAGES, TECHNOLOGIES, LEVEL, WORK_FORMAT, NOTICING, MENU, JOBS, PROFILE, SAVED = range(12)

class States:
    START = 1
    UNREGISTERED = 2
    REGISTRATION = 3
    LANGUAGES = 4
    TECHNOLOGIES = 5
    LEVEL = 6
    WORK_FORMAT = 7
    NOTICING = 8
    MENU = 9
    JOBS = 10
    PROFILE = 11
    SAVED = 12

languages_dict = {
    "EN" : "English",
    "DE" : "German",
    "FR" : "French",
    "ES" : "Spanish",
    "IT" : "Italian",
    "NL" : "Dutch",
    "PL" : "Polish",
    "SV" : "Swedish",
    "DA" : "Danish",
    "NO" : "Norwegian",
    "FI" : "Finnish",
    "CS" : "Czech",
    "RO" : "Romanian",
    "HU" : "Hungarian",
    "UK" : "Ukrainian",
}

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

# async def post_init(application):
#     print("Creating tables...")
#     await create_tables()
#     print("Tables created!")

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

        registration_test = True
            
        if registration_test is True:
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
            
        # async with AsyncSessionLocal() as session:
        #     user = await get_user(
        #         session,
        #         telegram_id=update.message.from_user.id
        #         )
            
        #     if user is None:
        #         await update.message.reply_text(
        #             f"You are NEW user! For registration click registration button",
        #             reply_markup=unregisterd_markup
        #         ) 
        #         return REGISTRATION
        #     else:
        #         await update.message.reply_text(
        #             f"Welcome back! Menu is bellow",
        #             reply_markup=menu_markup
        #         )
        #         return MENU

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Let's start...",
        reply_markup=ReplyKeyboardRemove()
    )
    await languages_menu(update, context)
    return LANGUAGES

def build_languages_keyboard(selected: list) -> InlineKeyboardMarkup:
    keyboard = []
    line = []
    for key, label in languages_dict.items():
        text = f"✅ {label}" if key in selected else label
        line.append(InlineKeyboardButton(text, callback_data=f"lang_{key}"))
        if len(line) == 3:
            keyboard.append(line)
            line = []
            continue

    if line:
        keyboard.append(line)

    keyboard.append(
        [InlineKeyboardButton("Continue >", callback_data="next")]
    )
    return InlineKeyboardMarkup(keyboard)

# async def languages_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     markup = build_languages_keyboard([])

#     await update.message.reply_text(
#         f"Choose languages:",
#         reply_markup=markup
#     )
#     return LANGUAGES

async def languages_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = build_languages_keyboard([])

    if update.message:
        chat_id = update.message.chat_id
    else:
        chat_id = update.callback_query.message.chat_id

    await context.bot.send_message(
        chat_id=chat_id,
        text="Choose languages:",
        reply_markup=markup
    )
    return LANGUAGES

async def handle_languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "next":
        selected = context.user_data.get("languages", [])

        await query.edit_message_text(
            f"You chose: {', '.join(selected)}"
        )
        # TODO test and remove
        context.user_data["languages"] = []
        await languages_menu(update, context)
        return LANGUAGES

    language = data.replace("lang_", "")
    selected = context.user_data.get("languages", [])
    if language in selected:
        selected.remove(language)
    else:
        selected.append(language)

    context.user_data["languages"] = selected
    new_markup = build_languages_keyboard(selected)

    await query.edit_message_reply_markup(reply_markup=new_markup)
    return LANGUAGES

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

async def fall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
                    f"Something went wrong"
                )
    start()

REG_DEV = True

if __name__ == '__main__':
    if sys.platform == "win32":
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = Application.builder().token(get_bot_token()).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REGISTRATION: [
                MessageHandler(filters.Regex("^Register$"), register)
            ],
            LANGUAGES: [
                CallbackQueryHandler(
                    handle_languages,
                    pattern="^lang_.*"
                ),
                CallbackQueryHandler(
                    handle_languages,
                    pattern="^next$"
                ),
            ],
            # lang - exp - tech - format - (location) - update freq.

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