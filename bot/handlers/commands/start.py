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
            text="👋 Привет! Ты в Ненабалкон — месте, где вещи не пылятся на балконах, а работают на людей!\n"
                 "Устал хранить ненужные вещи? Или ищешь что-то конкретное, но не хочешь переплачивать?\n\n"
                 "Мы соединяем:\n\n"
                 "Владельцев вещей, которые хотят заработать\n"
                 "Людей, которым вещи нужны прямо сейчас\n\n"
                 "Как это работает:\n\n"
                 "Размещаешь свою вещь или ищешь чужую\n"
                 "Находишь собеседника\n"
                 "Договариваешься о встрече\n"
                 "Получаешь или отдаёшь вещь",
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
