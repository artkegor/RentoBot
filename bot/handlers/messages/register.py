from telebot.types import ReplyKeyboardRemove

from datetime import datetime
from bot.bot import bot
from bot.utils.states import bot_states

from bot.keyboards.reply.user import request_location_keyboard
from bot.keyboards.inline.menu import main_menu_keyboard

from database.users.service import user_service
from database.users.models import User


@bot.message_handler(content_types=['contact'], state=bot_states.WAITING_FOR_CONTACT)
async def contact_handler(message):
    contact = message.contact
    if contact and contact.phone_number:
        # Extract phone number from the contact and register the users
        await user_service.register_user(
            User(
                id=message.chat.id,
                created_at=str(datetime.utcnow().timestamp()),
                username=message.chat.username or "",
                phone_number=contact.phone_number,
                latitude=0.0,
                longitude=0.0,
                rating=0.0,
                reviews=[],
                listings=[]
            )
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="Отправьте ваше местоположение при помощи кнопки ниже, чтобы мы могли показать вам объявления поблизости. 📍",
            reply_markup=request_location_keyboard()
        )
        await bot.set_state(
            chat_id=message.chat.id,
            user_id=message.chat.id,
            state=bot_states.WAITING_FOR_LOCATION
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Произошла ошибка при получении вашего номера телефона. Пожалуйста, попробуйте снова."
        )


@bot.message_handler(content_types=['location'], state=bot_states.WAITING_FOR_LOCATION)
async def location_handler(message):
    location = message.location
    if location and location.latitude and location.longitude:
        # Update the users's location in the database
        await user_service.update_location(
            user_id=message.chat.id,
            latitude=location.latitude,
            longitude=location.longitude
        )
        # Greet the users and show the main menu
        await bot.delete_state(
            chat_id=message.chat.id,
            user_id=message.chat.id
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="Спасибо! Вы успешно зарегистрированы в боте. ✅",
            reply_markup=ReplyKeyboardRemove()
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="<b>Главное меню:</b>",
            reply_markup=main_menu_keyboard()
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Произошла ошибка при получении вашего местоположения. Пожалуйста, попробуйте снова."
        )
