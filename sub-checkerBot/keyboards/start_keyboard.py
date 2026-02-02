from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_text import Start


def build_start_keyboard()-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✨Приобрести подписку✨",
        callback_data=Start.BUY_SUB,
    )
    builder.button(
        text="🔎📂Посмотреть текущую подписку🔎📂",
        callback_data=Start.CHECK_SUB
    )
    builder.adjust(1,1)
    return builder.as_markup()