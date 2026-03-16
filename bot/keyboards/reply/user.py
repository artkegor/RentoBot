from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_contact_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard with button to request users's contact."""
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


def request_location_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard with button to request users's location."""
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    location_button = KeyboardButton(
        text="Поделиться местоположением 📍",
        request_location=True
    )
    keyboard.add(location_button)
    return keyboard
