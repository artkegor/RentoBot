from config import config
from bot.bot import bot
from bot.keyboards.inline.admin import admin_panel


@bot.message_handler(commands=['admin'])
async def admin_command_handler(message):
    """Handle the /admin command to show the admin panel."""
    if message.chat.id in config.ADMIN_LIST:
        await bot.send_message(
            chat_id=message.chat.id,
            text="<b>Панель администратора:</b>",
            reply_markup=admin_panel()
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="У вас нет доступа к этой команде."
        )
