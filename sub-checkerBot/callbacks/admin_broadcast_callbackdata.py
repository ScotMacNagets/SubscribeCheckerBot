from aiogram.filters.callback_data import CallbackData


class BroadcastCB(CallbackData, prefix="admin_broadcast"):
    action: str