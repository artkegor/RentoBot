from bot.bot import bot
from bot.utils.memory import form_memory
from bot.utils.form_steps import LISTING_STEPS
from bot.keyboards.inline.listings import photos_done_keyboard, go_back_to_listing, confirm_listing_keyboard

from bot.utils.validate import validate_place_input, validate_price_input, validate_final_confirmation_input

from telebot.types import InputMediaPhoto

from logging_config import logger


@bot.message_handler(content_types=['text', 'photo'])
async def listing_handler(message):
    """Handle messages for listing creation steps."""
    state = await bot.get_state(
        chat_id=message.chat.id,
        user_id=message.chat.id
    )
    state_key = state.split(":")[-1]
    step = LISTING_STEPS.get(state_key)
    if not step:
        return

    # Delete the last bot message prompting for input
    last_bot_message_id = form_memory.get_answer(
        user_id=message.chat.id,
        form='create_listing',
        question='last_bot_message_id'
    )
    if last_bot_message_id:
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=last_bot_message_id
            )
        except Exception:
            logger.info(f"Failed to delete message for user {message.chat.id}, message ID: {last_bot_message_id}")

    # Check if the expected content type matches the received message
    if step['content_type'] == 'text' and not message.text:
        sent = await bot.send_message(
            chat_id=message.chat.id,
            text=step['prompt']
        )
        form_memory.set_answer(
            user_id=message.chat.id,
            form='create_listing',
            question='last_bot_message_id',
            answer=sent.message_id
        )
        return
    elif step['content_type'] == 'photo' and not message.photo:
        sent = await bot.send_message(
            chat_id=message.chat.id,
            text=step['prompt']
        )
        form_memory.set_answer(
            user_id=message.chat.id,
            form='create_listing',
            question='last_bot_message_id',
            answer=sent.message_id
        )
        return

    # If content type is text, process text answer
    if step['content_type'] == 'text':
        answer = message.text

        # Additional validation for place input
        if state_key == "WAITING_FOR_LISTING_PLACE":
            answer, latitude, longitude = validate_place_input(answer)
            form_memory.set_answer(
                user_id=message.chat.id,
                form='create_listing',
                question='listing_latitude',
                answer=latitude
            )
            form_memory.set_answer(
                user_id=message.chat.id,
                form='create_listing',
                question='listing_longitude',
                answer=longitude
            )
        # Additional validation for price input
        elif state_key == "WAITING_FOR_LISTING_PRICE" or state_key == "WAITING_FOR_LISTING_RENT_PRICE":
            try:
                price = validate_price_input(answer)
                answer = str(price)
            except ValueError:
                sent = await bot.send_message(
                    chat_id=message.chat.id,
                    text="Пожалуйста, введите корректную цену (положительное число):"
                )
                form_memory.set_answer(
                    user_id=message.chat.id,
                    form='create_listing',
                    question='last_bot_message_id',
                    answer=sent.message_id
                )
                return

        # Store the answer
        form_memory.set_answer(
            user_id=message.chat.id,
            form='create_listing',
            question=step['question'],
            answer=answer
        )
        if form_memory.get_answer(user_id=message.chat.id, form='create_listing', question='is_editing'):
            form_memory.set_answer(
                user_id=message.chat.id,
                form='create_listing',
                question='is_editing',
                answer=False
            )
            text, photos = validate_final_confirmation_input(user_id=message.chat.id)
            media_message_ids = []
            if photos:
                media_group = await bot.send_media_group(
                    chat_id=message.chat.id,
                    media=[InputMediaPhoto(photo_id) for photo_id in photos]
                )
                media_message_ids.extend([m.message_id for m in media_group])
            await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=confirm_listing_keyboard()
            )
            form_memory.set_answer(
                user_id=message.chat.id,
                form='create_listing',
                question='last_message_ids',
                answer=[*media_message_ids]
            )
            return
        sent = await bot.send_message(
            chat_id=message.chat.id,
            text=step['success'].format(answer=answer),
            reply_markup=go_back_to_listing(step['back'])
        )
        form_memory.set_answer(
            user_id=message.chat.id,
            form='create_listing',
            question='last_bot_message_id',
            answer=sent.message_id
        )
        # Move to the next state
        if step['next_state']:
            await bot.set_state(
                chat_id=message.chat.id,
                user_id=message.chat.id,
                state=step['next_state']
            )
        # If this was the last step, show summary
        else:
            # Show summary of the listing
            text, photos = validate_final_confirmation_input(user_id=message.chat.id)

            last_bot_message_id = form_memory.get_answer(
                user_id=message.chat.id,
                form='create_listing',
                question='last_bot_message_id'
            )
            if last_bot_message_id:
                try:
                    await bot.delete_message(
                        chat_id=message.chat.id,
                        message_id=last_bot_message_id
                    )
                except:
                    logger.info(
                        f"Failed to delete message for user {message.chat.id}, message ID: {last_bot_message_id}")

            media_message_ids = []
            if photos:
                media_group = await bot.send_media_group(
                    chat_id=message.chat.id,
                    media=[InputMediaPhoto(photo_id) for photo_id in photos]
                )
                media_message_ids.extend([m.message_id for m in media_group])

            await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=confirm_listing_keyboard()
            )

            form_memory.set_answer(
                user_id=message.chat.id,
                form='create_listing',
                question='last_message_ids',
                answer=[*media_message_ids]
            )
    # If content type is photo, process photo answer
    else:
        photos = form_memory.get_answer(user_id=message.chat.id, form='create_listing', question='listing_photo') or []
        photos.append(message.photo[-1].file_id)
        form_memory.set_answer(
            user_id=message.chat.id,
            form='create_listing',
            question=step['question'],
            answer=photos
        )
        sent = await bot.send_message(
            chat_id=message.chat.id,
            text=step['success'],
            reply_markup=photos_done_keyboard()
        )
        form_memory.set_answer(
            user_id=message.chat.id,
            form='create_listing',
            question='last_bot_message_id',
            answer=sent.message_id
        )
