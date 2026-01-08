from bot.bot import bot
from bot.utils.states import bot_states
from database.user.service import user_service
from database.user.models import User


@bot.message_handler(content_types=['contact'], state=bot_states.WAITING_FOR_CONTACT)
async def contact_handler(message):
    contact = message.contact
    if contact is not None:
        phone_number = contact.phone_number
        user = User(
            id=message.chat.id,
            username=message.chat.username or "",
            phone_number=phone_number,
            rating=0.0,
            reviews=[],
            listings=[]
        )
        await user_service.register_user(user)
        await bot.send_message(
            chat_id=message.chat.id,
            text="Спасибо! Вы успешно зарегистрированы в боте. ✅"
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Произошла ошибка при получении вашего контакта. Пожалуйста, попробуйте снова."
        )
