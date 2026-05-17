import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPIDAPI_TOKEN = os.getenv("RAPIDAPI_TOKEN")

def get_bot_token():
    return BOT_TOKEN

def get_rapidapi_token():
    return RAPIDAPI_TOKEN