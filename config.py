import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class to hold bot settings."""
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_DEFAULT_BOT_TOKEN")
    DB_URL = os.getenv("DB_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "mydatabase")


config = Config()
