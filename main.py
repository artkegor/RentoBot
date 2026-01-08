from telebot.types import BotCommand
from telebot.async_telebot import asyncio_filters

from logging_config import logger

from bot.bot import bot
from bot.handlers.commands import start
from bot.handlers.messages import contact


async def main():
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
