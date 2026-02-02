from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_text import Payment, Back


def build_payment_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="💳 Оплатить",
        callback_data=Payment.CONFIRM_PAY,
    )
    builder.button(
        text="⛔ Отменить оплату",
        callback_data=Payment.CANCEL_PAY,
    )
    builder.button(
        text="Назад",
        callback_data=Back.BACK,
    )
    builder.adjust(2,1)
    return builder.as_markup()