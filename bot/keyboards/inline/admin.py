from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_panel():
    """Creates an inline keyboard for the admin panel."""
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(text="Удалить объявление 🗑️", callback_data="admin:delete_listing"),

    )
    keyboard.add(
        InlineKeyboardButton(text="Статистика 📊", callback_data="admin:statistics"),
    )

    return keyboard


def back_to_menu_keyboard():
    """Creates an inline keyboard with a button to return to the main menu."""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Назад в меню 🔙", callback_data="admin:back_to_menu")
    )
    return keyboard
