from telebot.types import InputMediaPhoto

from bot.bot import bot
from bot.keyboards.inline.listings import go_back_to_listing, listing_type_keyboard, confirm_listing_keyboard
from bot.keyboards.inline.menu import back_to_menu_keyboard
from bot.utils.states import bot_states
from bot.utils.form_steps import CALLBACK_BACK_MAP, CALLBACK_BACK_TEXT, BACK_MAP, RESET_FIELDS, LISTING_STEPS, \
    CALLBACK_BACK_FOR_STRINGS, STATE_FOR_STRINGS
from bot.utils.memory import form_memory
from bot.utils.validate import validate_final_confirmation_input


@bot.callback_query_handler(func=lambda call: call.data.startswith('listings:back:'))
async def back_callback_handler(call):
    """Handle 'back' callback queries for listing creation steps."""
    user_id = call.message.chat.id
    new_state = CALLBACK_BACK_MAP.get(call.data)

    # Reset relevant fields
    for field in RESET_FIELDS.get(call.data, []):
        form_memory.set_answer(user_id=user_id, form='create_listing', question=field, answer=None)

    # Special case: listing type selection
    if call.data == 'listings:back:type':
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text="5️⃣ Выберите тип объявления:",
            reply_markup=listing_type_keyboard()
        )
        return

    if not new_state:
        return

    keyboard = back_to_menu_keyboard() if new_state == bot_states.WAITING_FOR_LISTING_TITLE else go_back_to_listing(
        BACK_MAP[new_state])

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=CALLBACK_BACK_TEXT[new_state],
        reply_markup=keyboard
    )
    await bot.set_state(chat_id=user_id, user_id=user_id, state=new_state)


@bot.callback_query_handler(func=lambda call: call.data == 'listings:photos:done')
async def photos_done_callback_handler(call):
    """Handle 'photos done' callback query."""
    if form_memory.get_answer(user_id=call.message.chat.id, form='create_listing', question='is_editing'):
        form_memory.set_answer(
            user_id=call.message.chat.id,
            form='create_listing',
            question='is_editing',
            answer=False
        )

        text, photos = validate_final_confirmation_input(user_id=call.message.chat.id)
        media_message_ids = []
        if photos:
            media_group = await bot.send_media_group(
                chat_id=call.message.chat.id,
                media=[InputMediaPhoto(photo_id) for photo_id in photos]
            )
            media_message_ids.extend([m.message_id for m in media_group])

        sent = await bot.send_message(
            chat_id=call.message.chat.id,
            text=text,
            reply_markup=confirm_listing_keyboard()
        )

        form_memory.set_answer(
            user_id=call.message.chat.id,
            form='create_listing',
            question='last_message_ids',
            answer=[*media_message_ids, sent.message_id]
        )
        return
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Фото сохранены!\n5️⃣ Выберите тип объявления (продажа или аренда):",
        reply_markup=listing_type_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('listings:type:'))
async def listing_type_callback_handler(call):
    """Handle listing type selection callback query."""
    user_id = call.message.chat.id
    listing_type = call.data.split(':')[-1]

    form_memory.set_answer(user_id=user_id, form='create_listing', question='listing_type', answer=listing_type)

    is_sale = listing_type == 'sale'
    text = (
        "Вы выбрали тип объявления: Продажа 🛒\n6️⃣ Введите цену товара/услуги:"
        if is_sale else
        "Вы выбрали тип объявления: Аренда 🏠\n6️⃣ Введите длительность аренды:"
    )

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=go_back_to_listing('type')
    )

    next_state = bot_states.WAITING_FOR_LISTING_PRICE if is_sale else bot_states.WAITING_FOR_LISTING_DURATION
    await bot.set_state(chat_id=user_id, user_id=user_id, state=next_state)


@bot.callback_query_handler(func=lambda call: call.data.startswith("edit:"))
async def edit_field_callback_handler(call):
    """Handle editing specific fields in the listing."""
    user_id = call.message.chat.id
    field_to_edit = call.data.split(":")[1]

    step_info = CALLBACK_BACK_FOR_STRINGS.get(f'WAITING_FOR_LISTING_{field_to_edit.upper()}')
    if not step_info:
        await bot.answer_callback_query(call.id, "Невозможно редактировать это поле.", show_alert=True)
        return

    form_memory.set_answer(
        user_id=user_id,
        form='create_listing',
        question='is_editing',
        answer=True
    )

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=step_info
    )

    await bot.set_state(
        chat_id=user_id,
        user_id=user_id,
        state=STATE_FOR_STRINGS.get(f'WAITING_FOR_LISTING_{field_to_edit.upper()}')
    )
