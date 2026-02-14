from collections.abc import Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.callback_text import Back
from callbacks.tariff_callbackdata import TariffCB
from core.models.tariff import Tariff
from keyboards.tariff_keyboard.format_helpers import format_tariff_button


def build_tariff_keyboard(tariffs: Sequence[Tariff]) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()

    for tariff in tariffs:
        text = format_tariff_button(tariff)

        builder.button(
            text=text,
            callback_data=TariffCB(payload=tariff.payload).pack(),
        )

    builder.button(
        text="Назад",
        callback_data=Back.BACK,
    )
    builder.adjust(1)
    return builder.as_markup()
