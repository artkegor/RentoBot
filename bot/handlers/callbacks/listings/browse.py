from uuid import uuid4
from datetime import datetime

from telebot.types import InputMediaPhoto

from bot.bot import bot
from bot.utils.states import bot_states
from bot.keyboards.inline.menu import back_to_menu_keyboard
from bot.keyboards.inline.listings import listings_keyboard, search_type_keyboard

from database.users.service import user_service
from database.listings.service import listing_service
from database.logs.service import log_service
from database.logs.models import Log

from bot.utils.validate import validate_listing_text
from bot.utils.memory import listings_memory, form_memory

from config import config


# =========================
# Helpers
# =========================

async def get_listing_or_alert(call, listing_id):
    listing = await listing_service.get_listing(listing_id)
    if not listing:
        await bot.answer_callback_query(call.id, "Объявление не найдено.", show_alert=True)
        return None
    return listing


def is_owner(call, listing):
    return listing.user_id == call.from_user.id


async def start_listings_flow(chat_id, user_id, listings, key):
    listings_memory.set_listings(user_id=user_id, key=key, listings=listings)

    msg = await bot.send_message(chat_id, "Загружаю объявление...")

    await show_listing(
        bot=bot,
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        user_id=user_id,
        key=key,
    )


async def handle_listings(call, listings, key, empty_text):
    if not listings:
        await bot.answer_callback_query(call.id, empty_text, show_alert=True)
        return

    listing_ids = [
        {'id': l.listing_id if hasattr(l, "listing_id") else l, 'distance': getattr(l, "distance", None)}
        for l in listings
    ]

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    await start_listings_flow(
        chat_id=call.message.chat.id,
        user_id=call.from_user.id,
        listings=listing_ids,
        key=key
    )


# =========================
# Handlers
# =========================

@bot.callback_query_handler(func=lambda c: c.data == 'listings:search')
async def search_listings_callback_handler(call):
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Выберите тип объявлений:",
        reply_markup=search_type_keyboard("listings:search")
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith('listings:search:'))
async def search_listings_callback_handler(call):
    _, _, listing_type = call.data.split(":")

    await bot.set_state(
        chat_id=call.message.chat.id,
        user_id=call.message.chat.id,
        state=bot_states.WAITING_FOR_SEARCH_QUERY
    )

    form_memory.set_answer(
        user_id=call.message.chat.id,
        form="search",
        question="listing_type",
        answer=listing_type
    )

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🔍 Введите запрос для поиска объявлений:",
        reply_markup=back_to_menu_keyboard()
    )


@bot.callback_query_handler(func=lambda c: c.data == 'listings:my')
async def my_listings_callback_handler(call):
    user = await user_service.get_user(call.from_user.id)
    listings = user.listings if user else []
    await handle_listings(call, listings, "list_my", "У вас нет объявлений.")


@bot.callback_query_handler(func=lambda c: c.data == 'listings:recent')
async def recent_choose_type(call):
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Выберите тип объявлений:",
        reply_markup=search_type_keyboard("listings:recent")
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith('listings:recent:'))
async def recent_listings_callback_handler(call):
    _, _, listing_type = call.data.split(":")

    listings = await listing_service.get_recent_listings(
        limit=20,
        listing_type=listing_type
    )

    await handle_listings(call, listings, "list_recent", "Нет доступных объявлений.")


@bot.callback_query_handler(func=lambda c: c.data == 'listings:nearest')
async def nearest_listings_callback_handler(call):
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Выберите тип объявлений:",
        reply_markup=search_type_keyboard("listings:nearest")
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith('listings:nearest:'))
async def nearest_listings_callback_handler(call):
    _, _, listing_type = call.data.split(":")

    user = await user_service.get_user(call.message.chat.id)

    listings = await listing_service.get_nearest_listings(
        latitude=user.latitude,
        longitude=user.longitude,
        listing_type=listing_type
    )

    await handle_listings(call, listings, "list_nearest", "Нет объявлений поблизости.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("listings:list"))
async def listings_pagination_handler(call):
    _, key, _, page = call.data.split(":")
    page = int(page)

    listings = listings_memory.get_listings(call.from_user.id, key)

    if not listings or page < 0 or page >= len(listings):
        await bot.answer_callback_query(call.id)
        return

    listings_memory.set_page(call.from_user.id, key, page)

    await show_listing(
        bot=bot,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        user_id=call.from_user.id,
        key=key,
    )

    await bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('listings:contact'))
async def contact_seller_callback_handler(call):
    listing_id = call.data.split(":")[-1]
    listing = await get_listing_or_alert(call, listing_id)
    if not listing:
        return

    seller = await user_service.get_user(listing.user_id)
    if not seller:
        await bot.answer_callback_query(call.id, "Продавец не найден.", show_alert=True)
        return

    contact_info = (
        f"📞 Контактная информация продавца:\n\n"
        f"👤 Юзернейм: @{seller.username}\n"
        f"📱 Телефон: {seller.phone_number}\n"
        f"🆔 ID объявления: {listing.listing_id}\n\n"
        f"Площадка не несет ответственности за проведение сделки."
    )

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    await log_service.create_log(
        Log(
            log_id=str(uuid4().int >> 64),
            timestamp=str(datetime.utcnow().timestamp()),
            user_id=call.message.chat.id,
            action="contact_seller"
        )
    )

    await bot.send_message(
        call.message.chat.id,
        contact_info,
        reply_markup=back_to_menu_keyboard()
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith('listings:status'))
async def toggle_listing_status_callback_handler(call):
    listing_id = call.data.split(":")[-1]
    listing = await get_listing_or_alert(call, listing_id)
    if not listing:
        return

    if not is_owner(call, listing):
        await bot.answer_callback_query(call.id, "Вы не можете изменить статус.", show_alert=True)
        return

    new_status = not listing.is_active
    await listing_service.update_listing_status(listing_id, new_status)

    if not new_status:
        await listing_service.set_finished_at(
            listing_id,
            str(datetime.utcnow().timestamp())
        )

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    await bot.send_message(
        call.message.chat.id,
        f"✅ {'Активно' if new_status else 'Продано'}",
        reply_markup=back_to_menu_keyboard()
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith('listings:delete'))
async def delete_listing_callback_handler(call):
    listing_id = call.data.split(":")[-1]
    listing = await get_listing_or_alert(call, listing_id)
    if not listing:
        return

    if not is_owner(call, listing):
        await bot.answer_callback_query(call.id, "Вы не можете удалить это объявление.", show_alert=True)
        return

    await listing_service.delete_listing(listing_id)
    await user_service.delete_listing_from_user(call.from_user.id, listing_id)

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    await bot.send_message(
        call.message.chat.id,
        "✅ Объявление удалено.",
        reply_markup=back_to_menu_keyboard()
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith('listings:report'))
async def report_listing_callback_handler(call):
    listing_id = call.data.split(":")[-1]
    listing = await get_listing_or_alert(call, listing_id)
    if not listing:
        return

    was_reported = await log_service.get_logs_by_user_and_action(
        user_id=call.message.chat.id,
        action=f"report_listing_{listing_id}",
    )

    if was_reported:
        await bot.answer_callback_query(call.id, "Вы уже жаловались.", show_alert=True)
        return

    await log_service.create_log(
        Log(
            log_id=str(uuid4().int >> 64),
            timestamp=str(datetime.utcnow().timestamp()),
            user_id=call.message.chat.id,
            action=f"report_listing_{listing_id}"
        )
    )

    await bot.send_message(
        config.FEEDBACK,
        (
            f"⚠️ Жалоба\n\n"
            f"👤 @{call.from_user.username} (ID: {call.message.chat.id})\n"
            f"🆔 {listing.listing_id}\n"
            f"📋 {listing.title}\n"
        )
    )

    await bot.answer_callback_query(
        call.id,
        "Жалоба отправлена.",
        show_alert=True
    )


# =========================
# Core display logic
# =========================

async def show_listing(bot, chat_id, message_id, user_id, key):
    listings = listings_memory.get_listings(user_id, key)
    page = listings_memory.get_page(user_id, key)

    if not listings:
        return

    listing_id = listings[page].get('id')
    distance = listings[page].get('distance')
    listing = await listing_service.get_listing(listing_id)

    text = validate_listing_text(listing) + (f"\n📍 {distance:.1f} км" if distance is not None else "")

    keyboard = listings_keyboard(
        page=page,
        total=len(listings),
        key=key,
        listing_id=listing.listing_id,
        user_id=user_id if listing.user_id != user_id else None,
        is_active=listing.is_active
    )

    if listing.photos:
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(
                media=listing.photos[0],
                caption=text,
                parse_mode="HTML",
            ),
            reply_markup=keyboard,
        )
    else:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
