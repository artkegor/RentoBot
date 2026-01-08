from telebot.handler_backends import State, StatesGroup


class BotStates(StatesGroup):
    """Класс состояний бота."""
    WAITING_FOR_CONTACT = State()


bot_states = BotStates()
