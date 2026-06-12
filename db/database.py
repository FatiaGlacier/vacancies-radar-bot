import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER_NAME = os.getenv("MONGO_APP_USER")
DB_USER_PASSWORD = os.getenv("MONGO_APP_PASSWORD")
DB_NAME = os.getenv("MONGO_APP_DB")

uri = f"mongodb://{DB_USER_NAME}:{DB_USER_PASSWORD}@localhost:27017/{DB_NAME}"

client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client[DB_NAME]
