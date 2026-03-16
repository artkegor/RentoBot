from bot.bot import bot
from bot.keyboards.inline.menu import main_menu_keyboard, back_to_menu_keyboard, feedback_keyboard

from database.users.service import user_service
from config import config
from logging_config import logger
from bot.utils.states import bot_states


@bot.callback_query_handler(func=lambda call: call.data == 'menu:main_menu')
async def main_menu_callback_handler(call):
    """Handle the 'main menu' callback query."""
    user_id = call.message.chat.id
    await bot.delete_state(
        chat_id=call.message.chat.id,
        user_id=call.message.chat.id
    )

    try:
        await bot.delete_message(
            chat_id=user_id,
            message_id=call.message.message_id
        )
    except:
        logger.warning(f"Failed to delete message for user {user_id}. It may have already been deleted.")

    # Check if the users exists before showing the main menu
    if await user_service.get_user(user_id):
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="<b>Главное меню:</b>",
            reply_markup=main_menu_keyboard()
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="Пожалуйста, зарегистрируйтесь сначала, используя команду /start.",
            show_alert=True
        )


@bot.callback_query_handler(func=lambda call: call.data == 'menu:profile')
async def profile_callback_handler(call):
    """Handle the 'profile' callback query."""
    user_id = call.message.chat.id
    if await user_service.get_user(user_id):
        user = await user_service.get_user(user_id)
        profile_text = (
            f"<b>Профиль пользователя:</b>\n\n"
            f"👤 Имя пользователя: @{user.username}\n"
            f"📞 Номер телефона: {user.phone_number}\n"
            # f"⭐ Рейтинг: {user.rating:.1f}\n"
            # f"📝 Количество отзывов: {len(user.reviews)}\n"
            f"📋 Количество объявлений: {len(user.listings)}"
        )
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=profile_text,
            reply_markup=back_to_menu_keyboard()
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="Пожалуйста, зарегистрируйтесь сначала, используя команду /start.",
            show_alert=True
        )


@bot.callback_query_handler(func=lambda call: call.data == 'menu:help')
async def help_callback_handler(call):
    """Handle the 'help' callback query."""
    help_text = (
        f"По всем вопросам пишите сюда: @{config.ADMIN_USERNAME}\n\n"
        f"Сервис не несет ответственности за сделки между пользователями.\n\n"
        f"Вы можете оставить фидбэк о площадке по кнопке ниже, это поможет нам стать лучше! 🤝"
    )
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=help_text,
        reply_markup=feedback_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data == 'menu:feedback')
async def feedback_callback_handler(call):
    """Handle the 'feedback' callback query."""
    await bot.set_state(
        chat_id=call.message.chat.id,
        user_id=call.message.chat.id,
        state=bot_states.WAITING_FOR_FEEDBACK
    )

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Пожалуйста, напишите свой отзыв о площадке. Ваш фидбэк поможет нам улучшить сервис! 📝",
        reply_markup=back_to_menu_keyboard()
    )
