from bot.utils.states import bot_states

RESET_FIELDS = {
    'listings:back:type': ['listing_type', 'listing_price', 'listing_duration', 'listing_rent_price'],
    'listings:back:photo': ['listing_photo'],
}

CALLBACK_BACK_MAP = {
    'listings:back:title': bot_states.WAITING_FOR_LISTING_TITLE,
    'listings:back:description': bot_states.WAITING_FOR_LISTING_DESCRIPTION,
    'listings:back:place': bot_states.WAITING_FOR_LISTING_PLACE,
    'listings:back:photo': bot_states.WAITING_FOR_LISTING_PHOTO,
    'listings:back:price': bot_states.WAITING_FOR_LISTING_PRICE,
    'listings:back:duration': bot_states.WAITING_FOR_LISTING_DURATION,
    'listings:back:rent_price': bot_states.WAITING_FOR_LISTING_RENT_PRICE
}

CALLBACK_BACK_TEXT = {
    bot_states.WAITING_FOR_LISTING_TITLE: "1️⃣ Введите название товара:",
    bot_states.WAITING_FOR_LISTING_DESCRIPTION: "2️⃣ Введите описание товара:",
    bot_states.WAITING_FOR_LISTING_PLACE: "3️⃣ Введите ваше местоположение:",
    bot_states.WAITING_FOR_LISTING_PHOTO: "4️⃣ Отправьте фото товара:",
    bot_states.WAITING_FOR_LISTING_PRICE: "6️⃣ Введите цену товара:",
    bot_states.WAITING_FOR_LISTING_DURATION: "6️⃣ Введите длительность аренды:",
    bot_states.WAITING_FOR_LISTING_RENT_PRICE: "7️⃣ Введите цену аренды:"
}

CALLBACK_BACK_FOR_STRINGS = {
    'WAITING_FOR_LISTING_TITLE': "1️⃣ Введите название товара:",
    'WAITING_FOR_LISTING_DESCRIPTION': "2️⃣ Введите описание товара:",
    'WAITING_FOR_LISTING_PLACE': "3️⃣ Введите ваше местоположение:",
    'WAITING_FOR_LISTING_PHOTO': "4️⃣ Отправьте фото товара:",
    'WAITING_FOR_LISTING_PRICE': "6️⃣ Введите цену товара:",
    'WAITING_FOR_LISTING_DURATION': "6️⃣ Введите длительность аренды:",
    'WAITING_FOR_LISTING_RENT_PRICE': "7️⃣ Введите цену аренды:"
}

STATE_FOR_STRINGS = {
    'WAITING_FOR_LISTING_TITLE': bot_states.WAITING_FOR_LISTING_TITLE,
    'WAITING_FOR_LISTING_DESCRIPTION': bot_states.WAITING_FOR_LISTING_DESCRIPTION,
    'WAITING_FOR_LISTING_PLACE': bot_states.WAITING_FOR_LISTING_PLACE,
    'WAITING_FOR_LISTING_PHOTO': bot_states.WAITING_FOR_LISTING_PHOTO,
    'WAITING_FOR_LISTING_PRICE': bot_states.WAITING_FOR_LISTING_PRICE,
    'WAITING_FOR_LISTING_DURATION': bot_states.WAITING_FOR_LISTING_DURATION,
    'WAITING_FOR_LISTING_RENT_PRICE': bot_states.WAITING_FOR_LISTING_RENT_PRICE
}

BACK_MAP = {
    bot_states.WAITING_FOR_LISTING_TITLE: 'menu',
    bot_states.WAITING_FOR_LISTING_DESCRIPTION: 'title',
    bot_states.WAITING_FOR_LISTING_PLACE: 'description',
    bot_states.WAITING_FOR_LISTING_PHOTO: 'place',
    bot_states.WAITING_FOR_LISTING_PRICE: 'photo',
    bot_states.WAITING_FOR_LISTING_DURATION: 'type',
    bot_states.WAITING_FOR_LISTING_RENT_PRICE: 'type'
}

LISTING_STEPS = {
    "WAITING_FOR_LISTING_TITLE": {
        'question': 'listing_title',
        'prompt': "Название не может быть пустым. Пожалуйста, введите корректное название:",
        'success': "Название '{answer}' сохранено!\n2️⃣ Введите описание товара:",
        'next_state': bot_states.WAITING_FOR_LISTING_DESCRIPTION,
        'back': 'title',
        'content_type': 'text'
    },
    "WAITING_FOR_LISTING_DESCRIPTION": {
        'question': 'listing_description',
        'prompt': "Описание не может быть пустым. Пожалуйста, введите корректное описание:",
        'success': "Описание сохранено!\n3️⃣ Введите ваше местоположение:",
        'next_state': bot_states.WAITING_FOR_LISTING_PLACE,
        'back': 'description',
        'content_type': 'text'
    },
    "WAITING_FOR_LISTING_PLACE": {
        'question': 'listing_place',
        'prompt': "Местоположение не может быть пустым. Пожалуйста, введите корректное местоположение:",
        'success': "Местоположение '{answer}' сохранено!\n4️⃣ Отправьте фото товара:",
        'next_state': bot_states.WAITING_FOR_LISTING_PHOTO,
        'back': 'place',
        'content_type': 'text'
    },
    "WAITING_FOR_LISTING_PHOTO": {
        'question': 'listing_photo',
        'prompt': "Отправьте фото товара:",
        'success': "Фото сохранено! Вы можете отправить еще фото или нажать 'Готово', если закончили.",
        'next_state': None,
        'back': 'photo',
        'content_type': 'photo'
    },
    "WAITING_FOR_LISTING_PRICE": {
        'question': 'listing_price',
        'prompt': "Цена не может быть пустой. Пожалуйста, введите корректную цену:",
        'success': "Цена '{answer}' сохранена!",
        'next_state': None,
        'back': 'price',
        'content_type': 'text'
    },
    "WAITING_FOR_LISTING_DURATION": {
        'question': 'listing_duration',
        'prompt': "Длительность аренды не может быть пустой. Пожалуйста, введите корректную длительность:",
        'success': "Длительность аренды '{answer}' сохранена!\n7️⃣ Введите цену аренды:",
        'next_state': bot_states.WAITING_FOR_LISTING_RENT_PRICE,
        'back': 'duration',
        'content_type': 'text'
    },
    "WAITING_FOR_LISTING_RENT_PRICE": {
        'question': 'listing_price',
        'prompt': "Цена аренды не может быть пустой. Пожалуйста, введите корректную цену:",
        'success': "Цена аренды '{answer}' сохранена!",
        'next_state': None,
        'back': 'rent_price',
        'content_type': 'text'
    }
}
