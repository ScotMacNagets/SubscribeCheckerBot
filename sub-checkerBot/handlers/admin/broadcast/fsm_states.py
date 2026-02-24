from aiogram.fsm.state import StatesGroup, State


class BroadcastState(StatesGroup):
    waiting_for_message = State()
    sending_photo = State()
    waiting_for_photo = State()
    confirm = State()