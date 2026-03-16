from bot.bot import bot
from database.users.service import user_service
from database.listings.service import listing_service
from database.logs.service import log_service


@bot.callback_query_handler(func=lambda call: call.data == 'admin:statistics')
async def statistics_callback_handler(call):
    """Handle the 'statistics' callback query."""

    users = await user_service.get_registration_statistics()
    listings = await listing_service.get_listing_statistics()
    logs = await log_service.get_action_statistics()

    text = f"""
    📊 *Статистика платформы*
    
    👤 Пользователи
    За день: {users['day']}
    За неделю: {users['week']}
    За месяц: {users['month']}
    
    📦 Создано объявлений
    За день: {listings['created']['day']}
    За неделю: {listings['created']['week']}
    За месяц: {listings['created']['month']}
    
    ✅ Завершено объявлений
    За день: {listings['finished']['day']}
    За неделю: {listings['finished']['week']}
    За месяц: {listings['finished']['month']}
    
    🔍 Поиск
    За день: {logs['search']['day']}
    За неделю: {logs['search']['week']}
    За месяц: {logs['search']['month']}
    
    📞 Получено контактов
    За день: {logs['contact']['day']}
    За неделю: {logs['contact']['week']}
    За месяц: {logs['contact']['month']}
    """

    await bot.send_message(
        call.message.chat.id,
        text,
        parse_mode="Markdown"
    )
