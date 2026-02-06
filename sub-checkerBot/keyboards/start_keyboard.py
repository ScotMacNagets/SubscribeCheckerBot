from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.text import StartKeyboard
from callbacks.callback_text import Start


def build_start_keyboard()-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=StartKeyboard.BUY_SUBSCRIPTION,
        callback_data=Start.BUY_SUB,
    )
    builder.button(
        text=StartKeyboard.CHECK_SUBSCRIPTION,
        callback_data=Start.CHECK_SUB
    )
    builder.adjust(1,1)
    return builder.as_markup()