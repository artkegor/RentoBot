from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def go_back_to_listing(step: str) -> InlineKeyboardMarkup:
    """Create an inline keyboard with a button to go back to a specific listing step."""
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(
        text="🔙 Назад",
        callback_data=f'listings:back:{step}'
    )
    keyboard.add(back_button)
    return keyboard


def photos_done_keyboard() -> InlineKeyboardMarkup:
    """Create an inline keyboard with a button to finish adding photos."""
    keyboard = InlineKeyboardMarkup()
    done_button = InlineKeyboardButton(
        text="✅ Готово",
        callback_data='listings:photos:done'
    )
    keyboard.add(done_button)
    return keyboard


def listing_type_keyboard() -> InlineKeyboardMarkup:
    """Create an inline keyboard for selecting listing type."""
    keyboard = InlineKeyboardMarkup(row_width=2)
    sale_button = InlineKeyboardButton(
        text="Продажа 🛒",
        callback_data='listings:type:sale'
    )
    rent_button = InlineKeyboardButton(
        text="Аренда 🏠",
        callback_data='listings:type:rent'
    )
    back_button = InlineKeyboardButton(
        text="🔙 Назад",
        callback_data='listings:back:photo'
    )
    keyboard.add(sale_button, rent_button, back_button)
    return keyboard


def confirm_listing_keyboard() -> InlineKeyboardMarkup:
    """Create an inline keyboard for confirming or editing a listing."""
    keyboard = InlineKeyboardMarkup(row_width=2)
    confirm_button = InlineKeyboardButton(
        text="✅ Подтвердить",
        callback_data='listings:confirm'
    )
    edit_button = InlineKeyboardButton(
        text="✏️ Редактировать",
        callback_data='listings:edit'
    )
    keyboard.add(confirm_button, edit_button)
    return keyboard


def search_type_keyboard(prefix: str):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="Продажа 🛒",
            callback_data=f"{prefix}:sale"
        ),
        InlineKeyboardButton(
            text="Аренда 🏠",
            callback_data=f"{prefix}:rent"
        ),
        InlineKeyboardButton(
            text="Все 📋",
            callback_data=f"{prefix}:all"
        ),
        InlineKeyboardButton(
            text="⬅️ В меню",
            callback_data="menu:main_menu"
        )
    )
    return keyboard


def listings_keyboard(page: int, total: int, key: str, listing_id: int = None, user_id: int = None,
                      is_active: bool = False) -> InlineKeyboardMarkup:
    """Create an inline keyboard for navigating through listings pages."""
    kb = InlineKeyboardMarkup(row_width=3)

    prev_btn = InlineKeyboardButton(
        text="◀️",
        callback_data=f"listings:{key}:page:{page - 1}"
    ) if page > 0 else InlineKeyboardButton(
        text=" ",
        callback_data="noop"
    )

    counter_btn = InlineKeyboardButton(
        text=f"{page + 1} / {total}",
        callback_data="noop"
    )

    next_btn = InlineKeyboardButton(
        text="▶️",
        callback_data=f"listings:{key}:page:{page + 1}"
    ) if page < total - 1 else InlineKeyboardButton(
        text=" ",
        callback_data="noop"
    )

    kb.row(prev_btn, counter_btn, next_btn)

    if user_id:
        kb.add(
            InlineKeyboardButton(
                text="📞 Связаться с продавцом",
                callback_data=f"listings:contact:{listing_id}"
            )
        )
        kb.add(
            InlineKeyboardButton(
                text="⚠️ Пожаловаться на объявление",
                callback_data=f"listings:report:{listing_id}"
            )
        )
    else:
        kb.add(
            InlineKeyboardButton(
                text="✅ Отметить как продано" if is_active else "🕥 Активировать объявление",
                callback_data=f"listings:status:{listing_id}"
            )
        )
        kb.add(
            InlineKeyboardButton(
                text="🗑️ Удалить объявление",
                callback_data=f"listings:delete:{listing_id}"
            )
        )
    kb.add(
        InlineKeyboardButton(
            text="⬅️ В меню",
            callback_data="menu:main_menu"
        )
    )

    return kb


def edit_listing_keyboard(listing_type: str) -> InlineKeyboardMarkup:
    """
    Inline клавиатура для редактирования конкретного поля перед подтверждением.
    """
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton("Название", callback_data="edit:title"),
        InlineKeyboardButton("Описание", callback_data="edit:description"),
        InlineKeyboardButton("Местоположение", callback_data="edit:place"),
        InlineKeyboardButton("Фото", callback_data="edit:photo")
    ]

    if listing_type == "sale":
        buttons.append(InlineKeyboardButton("Цена", callback_data="edit:price"))
    else:
        buttons.extend([
            InlineKeyboardButton("Длительность аренды", callback_data="edit:duration"),
            InlineKeyboardButton("Цена аренды", callback_data="edit:rent_price")
        ])

    # Добавляем кнопки по 2 в ряд
    for i in range(0, len(buttons), 2):
        keyboard.row(*buttons[i:i + 2])

    return keyboard
