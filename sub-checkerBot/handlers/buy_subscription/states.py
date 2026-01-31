from aiogram.fsm.state import StatesGroup, State


class BuySubscription(StatesGroup):
    choosing_tariff = State()
    confirming_payment = State()