from config import config
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

bot = AsyncTeleBot(
    token=config.BOT_TOKEN,
    parse_mode="HTML",
    state_storage=StateMemoryStorage()
)
