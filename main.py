from telebot.types import BotCommand
from telebot.async_telebot import asyncio_filters

from logging_config import logger

from bot.bot import bot
from bot.handlers.commands import start, admin  # noqa: F401
from bot.handlers.messages import feedback, admin, search, register, listings  # noqa: F401
from bot.handlers.callbacks import menu  # noqa: F401
from bot.handlers.callbacks.admin import default, listings, statistic  # noqa: F401
from bot.handlers.callbacks.listings import browse, form, create  # noqa: F401

from database.base import base_db


async def main():
    # Initialize database indexes
    logger.info("Initializing database indexes...")
    await base_db.init_indexes()

    # Register custom filters
    bot.add_custom_filter(
        custom_filter=asyncio_filters.StateFilter(bot)
    )

    # Start the bot
    logger.info("Starting the bot...")
    await bot.set_my_commands([
        BotCommand("start", "Запустить бота")
    ])
    logger.info("Bot commands set.")
    await bot.infinity_polling()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
