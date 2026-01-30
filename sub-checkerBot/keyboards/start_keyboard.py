from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

buy_sub = "buy_subscription"

def build_start_keyboard()-> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✨Приобрести подписку✨",
        callback_data=buy_sub,
    )
    return builder.as_markup()