from aiogram.fsm.state import StatesGroup, State

class CreateTariff(StatesGroup):
    title = State()
    days = State()
    price = State()
    confirm = State()

