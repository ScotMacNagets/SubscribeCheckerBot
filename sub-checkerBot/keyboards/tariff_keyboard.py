from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_text import back
from core.tariff import TARIFFS


def build_tariff_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for tariff in TARIFFS.values():
        mouths = tariff.days // 30
        price_rub = tariff.price // 100

        text = f"{mouths} мес. | {price_rub} ₽"
        if mouths == 6:
            text = f"💎 {text} 💎"

        builder.button(
            text=text,
            callback_data=tariff.id
        )

    builder.button(
        text="Назад",
        callback_data=back.back,
    )
    builder.adjust(2,1,1)
    return builder.as_markup()
