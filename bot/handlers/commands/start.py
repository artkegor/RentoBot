from database.user.service import user_service
from bot.keyboards.reply.user import request_contact_keyboard
from bot.bot import bot
from bot.utils.states import bot_states


@bot.message_handler(commands=['start'])
async def start_handler(message):
    user_id = message.chat.id
    if await user_service.check_if_user_exists(user_id) is False:
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
        await bot.send_message(
            chat_id=message.chat.id,
            text="Вы уже зарегистрированы в системе."
        )
