from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for the main menu."""
    keyboard = InlineKeyboardMarkup(row_width=2)
    row1 = [
        InlineKeyboardButton(text="Поиск объявлений 🔍", callback_data="listings:search"),
        InlineKeyboardButton(text="Создать объявление ➕", callback_data="listings:create"),
    ]
    row2 = [
        InlineKeyboardButton(text="Новые объявления 🕒", callback_data="listings:recent"),
        InlineKeyboardButton(text="Объявления поблизости 📍", callback_data="listings:nearest"),
    ]
    row3 = [
        InlineKeyboardButton(text="Мои объявления 📋", callback_data="listings:my"),
        InlineKeyboardButton(text="Профиль 👤", callback_data="menu:profile"),
    ]
    row4 = [
        InlineKeyboardButton(text="Помощь ❓", callback_data="menu:help"),
    ]
    keyboard.add(*row1)
    keyboard.add(*row2)
    keyboard.add(*row3)
    keyboard.add(*row4)
    return keyboard


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for the users profile."""
    keyboard = InlineKeyboardMarkup(row_width=2)
    main_menu_button = InlineKeyboardButton(
        text="Главное меню 🏠",
        callback_data="menu:main_menu"
    )
    keyboard.add(main_menu_button)
    return keyboard


def feedback_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for feedback."""
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(
        text="Оставить фидбэк 📝",
        callback_data="menu:feedback"
    ))
    keyboard.add(InlineKeyboardButton(
        text="Главное меню 🏠",
        callback_data="menu:main_menu"
    ))

    return keyboard
