from bot.bot import bot
from bot.utils.states import bot_states
from database.listings.service import listing_service
from bot.keyboards.inline.menu import back_to_menu_keyboard
from config import config
from database.users.service import user_service
from logging_config import logger


@bot.message_handler(content_types=['text'], state=bot_states.ADMIN_WAITING_FOR_LISTING_ID)
async def search_handler(message):
    logger.info(f"Admin {message.chat.id} is attempting to delete listing with ID: {message.text.strip()}")
    if message.chat.id not in config.ADMIN_LIST:
        await bot.send_message(
            chat_id=message.chat.id,
            text="У вас нет доступа к этой команде."
        )
        return

    listing_id = message.text.strip()
    listing = await listing_service.get_listing(listing_id=listing_id)
    user_id = listing.user_id if listing else None
    title = listing.title if listing else "неизвестно"

    delete_success = await listing_service.delete_listing(listing_id=listing_id)
    user_success = await user_service.delete_listing_from_user(user_id=user_id, listing_id=listing_id)

    if delete_success and user_success:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"✅ Объявление с ID {listing_id} успешно удалено.",
            reply_markup=back_to_menu_keyboard()
        )
        await bot.send_message(
            chat_id=user_id,
            text=f"‼️ Ваше объявление с ID {listing_id} ({title}) было удалено администратором.\n"
                 f"📇 Если вы считаете, что это ошибка, пожалуйста, свяжитесь с поддержкой."
        )
        await bot.delete_state(
            chat_id=message.chat.id,
            user_id=message.chat.id
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Объявление с ID {listing_id} не найдено. Пожалуйста, проверьте ID и попробуйте снова.",
            reply_markup=back_to_menu_keyboard()
        )
