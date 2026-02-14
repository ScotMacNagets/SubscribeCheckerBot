from sys import prefix

from aiogram.filters.callback_data import CallbackData

class TariffCB(CallbackData, prefix="sub_"):
    payload: str