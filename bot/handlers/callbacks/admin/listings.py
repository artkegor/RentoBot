from bot.bot import bot
from bot.utils.states import bot_states
from bot.keyboards.inline.admin import back_to_menu_keyboard


@bot.callback_query_handler(func=lambda call: call.data == 'admin:delete_listing')
async def delete_listing_callback_handler(call):
    await bot.set_state(
        chat_id=call.message.chat.id,
        user_id=call.message.chat.id,
        state=bot_states.ADMIN_WAITING_FOR_LISTING_ID
    )

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🆔 Введите ID объявления для удаления:",
        reply_markup=back_to_menu_keyboard()
    )
