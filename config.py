import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class to hold bot settings."""
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_DEFAULT_BOT_TOKEN")
    DB_URL = os.getenv("DB_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "mydatabase")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_LIST = list(map(int, os.getenv("ADMIN_LIST", "").split(",")))
    FEEDBACK = os.getenv("FEEDBACK", "")
    YANDEX_MAPS_API_KEY = os.getenv("YANDEX_MAPS_API_KEY", "YOUR_DEFAULT_YANDEX_MAPS_API_KEY")


config = Config()
