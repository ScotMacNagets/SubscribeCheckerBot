from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_text import Back
from core.tariff import TARIFFS


def build_tariff_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for tariff in TARIFFS.values():
        months = tariff.days // 30
        price_rub = tariff.price // 100
        hot = tariff.hot
        emoji = tariff.emoji

        text = f"{months} мес. | {price_rub} ₽"
        if hot:
            text = f"{emoji} {text} {emoji}"

        builder.button(
            text=text,
            callback_data=tariff.id
        )

    builder.button(
        text="Назад",
        callback_data=Back.BACK,
    )
    builder.adjust(2,1,1)
    return builder.as_markup()
