from telebot.handler_backends import State, StatesGroup


class BotStates(StatesGroup):
    """Bot states for managing users interactions."""
    WAITING_FOR_CONTACT = State()
    WAITING_FOR_LOCATION = State()
    WAITING_FOR_LISTING_TITLE = State()
    WAITING_FOR_LISTING_DESCRIPTION = State()
    WAITING_FOR_LISTING_PLACE = State()
    WAITING_FOR_LISTING_PHOTO = State()
    WAITING_FOR_LISTING_PRICE = State()
    WAITING_FOR_LISTING_DURATION = State()
    WAITING_FOR_LISTING_RENT_PRICE = State()
    WAITING_FOR_SEARCH_QUERY = State()
    WAITING_FOR_FEEDBACK = State()

    ADMIN_WAITING_FOR_LISTING_ID = State()


bot_states = BotStates()
