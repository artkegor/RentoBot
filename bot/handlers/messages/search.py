from datetime import datetime
from uuid import uuid4

from bot.bot import bot
from bot.utils.memory import listings_memory
from bot.utils.states import bot_states
from database.listings.service import listing_service
from bot.keyboards.inline.menu import back_to_menu_keyboard

from database.logs.service import log_service
from database.logs.models import Log

from bot.handlers.callbacks.listings.browse import show_listing


@bot.message_handler(content_types=['text'], state=bot_states.WAITING_FOR_SEARCH_QUERY)
async def search_handler(message):
    """Handle messages for search queries."""
    query = message.text.strip()
    if not query:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Запрос не может быть пустым. Пожалуйста, введите корректный запрос для поиска:"
        )
        return

    results = await listing_service.search_listings(query=query)
    if not results:
        await bot.send_message(
            chat_id=message.chat.id,
            text="По вашему запросу не найдено объявлений. Попробуйте изменить запрос и поискать снова.",
            reply_markup=back_to_menu_keyboard()
        )
        return

    results = [l.listing_id for l in results]
    listings_memory.set_listings(
        user_id=message.from_user.id,
        key="list_search_results",
        listings=results,
    )

    msg = await bot.send_message(
        chat_id=message.chat.id,
        text="Найденные объявления загружаются..."
    )
    await log_service.create_log(
        Log(
            log_id=str(uuid4().int >> 64),
            timestamp=str(datetime.utcnow().timestamp()),
            user_id=message.chat.id,
            action="search_listings",
        )
    )
    await show_listing(
        bot=bot,
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        user_id=message.from_user.id,
        key="list_search_results",
    )
