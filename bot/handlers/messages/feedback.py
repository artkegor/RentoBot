from config import config
from bot.utils.states import bot_states
from bot.bot import bot


@bot.message_handler(state=bot_states.WAITING_FOR_FEEDBACK, content_types=['text', 'photo', 'video', 'document', 'audio'])
async def feedback_handler(message):
    feedback_msg_id = message.message_id
    feedback_chat_id = config.FEEDBACK

    await bot.delete_state(
        chat_id=message.chat.id,
        user_id=message.chat.id
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text="Спасибо за ваш отзыв! 🙏 Ваше сообщение было отправлено команде поддержки."
    )

    await bot.send_message(
        chat_id=feedback_chat_id,
        text=f"Новый отзыв от пользователя {message.chat.id} (@{message.chat.username}):"
    )

    await bot.copy_message(
        chat_id=feedback_chat_id,
        from_chat_id=message.chat.id,
        message_id=feedback_msg_id
    )
