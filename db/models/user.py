from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_id: int
    telegram_id: int
    languages: list[str] = []
    key_words: list[str] = []
    experience: list[str] = []
    job_types: list[str] = []
    locations: list[str] = []