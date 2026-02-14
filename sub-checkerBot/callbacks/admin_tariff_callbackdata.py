from aiogram.filters.callback_data import CallbackData


class AdminTariffCB(CallbackData, prefix="admin_tariff"):

    action: str
    tariff_id: int | None = None

