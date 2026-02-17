from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.text import PaymentKeyboard, GeneralButtons
from callbacks.callback_text import Payment, Back


def build_payment_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=PaymentKeyboard.PAY,
        callback_data=Payment.CONFIRM_PAY,
    )
    builder.button(
        text=PaymentKeyboard.CANCEL_PAYMENT,
        callback_data=Payment.CANCEL_PAY,
    )
    builder.button(
        text=GeneralButtons.BACK_BUTTON,
        callback_data=Back.BACK,
    )
    builder.adjust(2,1)
    return builder.as_markup()