

from aiogram.filters.callback_data import CallbackData

class AdminUserCB(CallbackData, prefix="admin_user"):
    action: str
    username: str | None = None
    days: int | None = None