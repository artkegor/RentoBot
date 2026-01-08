from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_contact_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard with button to request user's contact."""
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    contact_button = KeyboardButton(
        text="Поделиться контактом 📞",
        request_contact=True
    )
    keyboard.add(contact_button)
    return keyboard
