from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.payment_keyboard import back
from core.config import tariff


def build_tariff_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="1 месяц | 299 рублей",
        callback_data=tariff.plan_1,
    )
    builder.button(
        text="3 месяца | 500 рублей",
        callback_data=tariff.plan_3,
    )
    builder.button(
        text="💎 6 месяцев | 900 рублей 💎",
        callback_data=tariff.plan_6,
    )
    builder.button(
        text="Назад",
        callback_data=back,
    )
    builder.adjust(2,1,1)
    return builder.as_markup()
