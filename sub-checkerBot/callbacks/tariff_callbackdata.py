from sys import prefix

from aiogram.filters.callback_data import CallbackData

class TariffCallback(CallbackData, prefix="sub_"):
    payload: str