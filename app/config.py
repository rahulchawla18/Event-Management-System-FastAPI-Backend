import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Kolkata")

settings = Settings()