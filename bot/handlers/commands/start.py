from database.users.service import user_service

from bot.keyboards.reply.user import request_contact_keyboard
from bot.bot import bot
from bot.utils.states import bot_states
from bot.keyboards.inline.menu import main_menu_keyboard
from logging_config import logger


@bot.message_handler(commands=['start'])
async def start_handler(message):
    user_id = message.chat.id
    logger.info(f"User {user_id} initiated /start command.")

    if await user_service.get_user(user_id) is False:
        await bot.set_state(
            chat_id=message.chat.id,
            user_id=message.chat.id,
            state=bot_states.WAITING_FOR_CONTACT
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="Добро пожаловать в Рентобот! 👋\n"
                 "Пожалуйста, отправьте свой номер телефона для завершения регистрации при помощи кнопки ниже.",
            reply_markup=request_contact_keyboard()
        )
    else:
        username = (await user_service.get_user(user_id)).username
        if username != message.chat.username:
            await user_service.update_username(user_id, message.chat.username)
        await bot.send_message(
            chat_id=message.chat.id,
            text="<b>Главное меню:</b>",
            reply_markup=main_menu_keyboard()
        )
