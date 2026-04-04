from uuid import uuid4
from datetime import datetime

from bot.bot import bot
from bot.utils.states import bot_states
from bot.keyboards.inline.menu import back_to_menu_keyboard
from bot.keyboards.inline.listings import edit_listing_keyboard
from bot.utils.memory import form_memory

from database.users.service import user_service
from database.listings.service import listing_service
from database.listings.models import Listing
from logging_config import logger

from services.tags.tags_extractor import generate_tags


@bot.callback_query_handler(func=lambda call: call.data == 'listings:create')
async def create_listing_callback_handler(call):
    """Handle the 'create listing' callback query."""
    sent = await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="1️⃣ Введите название товара:",
        reply_markup=back_to_menu_keyboard()
    )
    form_memory.set_answer(
        user_id=call.message.chat.id,
        form='create_listing',
        question='last_bot_message_id',
        answer=sent.message_id
    )
    await bot.set_state(
        chat_id=call.message.chat.id,
        user_id=call.message.chat.id,
        state=bot_states.WAITING_FOR_LISTING_TITLE
    )


@bot.callback_query_handler(func=lambda call: call.data == "listings:edit")
async def edit_listing_callback(call):
    """Handle the 'edit listing' callback query."""
    user_id = call.message.chat.id

    data = form_memory.get_answers(user_id=user_id, form="create_listing")
    listing_type = data.get("listing_type")

    if not listing_type:
        await bot.answer_callback_query(call.id, "Невозможно редактировать, тип объявления не определен",
                                        show_alert=True)
        return

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="Выберите поле для редактирования:",
        reply_markup=edit_listing_keyboard(listing_type)
    )


@bot.callback_query_handler(func=lambda call: call.data == 'listings:confirm')
async def confirm_listing_callback_handler(call):
    """Handle the 'confirm listing' callback query."""
    user_id = call.message.chat.id

    last_msg_ids = form_memory.get_answer(
        user_id=user_id,
        form='create_listing',
        question='last_message_ids'
    )

    try:
        for msg_id in last_msg_ids:
            await bot.delete_message(
                chat_id=user_id,
                message_id=msg_id
            )
    except Exception:
        logger.info(f"Failed to delete messages for user {user_id}, message IDs: {last_msg_ids}")

    data = form_memory.get_answers(user_id=user_id, form='create_listing')

    tags = generate_tags(
        f"{data.get('listing_title')} {data.get('listing_description')}"
    )

    listing_id = str(uuid4().int >> 64)
    listing_type = data.get('listing_type')

    price = None
    duration = None

    if listing_type == "sale":
        price = float(data.get("listing_price"))
    else:
        price = float(data.get("listing_price"))
        duration = data.get("listing_duration")

    listing = Listing(
        listing_id=listing_id,
        user_id=user_id,
        created_at=str(datetime.utcnow().timestamp()),
        finished_at="",

        title=data.get('listing_title'),
        description=data.get('listing_description'),

        transaction_type=listing_type,
        is_active=True,

        tags=tags,

        price=price,
        duration=duration,

        place=data.get('listing_place'),

        location={
            "type": "Point",
            "coordinates": [
                float(data.get('listing_longitude')),
                float(data.get('listing_latitude'))
            ]
        },

        photos=data.get('listing_photo', []),
        score=None
    )

    await listing_service.create_listing(
        listing=listing
    )

    await user_service.add_listing_to_user(
        user_id=user_id,
        listing_id=listing.listing_id
    )

    form_memory.clear_form(
        user_id=user_id,
        form='create_listing'
    )

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="✅ Ваше объявление успешно создано!",
        reply_markup=back_to_menu_keyboard()
    )
