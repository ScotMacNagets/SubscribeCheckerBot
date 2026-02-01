from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_text import start


def build_start_keyboard()-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✨Приобрести подписку✨",
        callback_data=start.buy_sub,
    )
    return builder.as_markup()