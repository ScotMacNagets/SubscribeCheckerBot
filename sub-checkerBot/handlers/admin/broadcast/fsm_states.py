from aiogram.fsm.state import StatesGroup, State


class BroadcastState(StatesGroup):
    waiting_for_message = State()
    confirm = State()