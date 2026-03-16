from bot.bot import bot
from bot.keyboards.inline.admin import admin_panel
from logging_config import logger


@bot.callback_query_handler(func=lambda call: call.data == 'admin:back_to_menu')
async def back_to_menu_callback_handler(call):
    await bot.delete_state(
        chat_id=call.message.chat.id,
        user_id=call.message.chat.id
    )

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>Панель администратора:</b>",
        reply_markup=admin_panel()
    )
