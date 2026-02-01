from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_text import payment, back


def build_payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="💳 Оплатить",
        callback_data=payment.confirm_pay,
    )
    builder.button(
        text="⛔ Отменить оплату",
        callback_data=payment.cancel_pay,
    )
    builder.button(
        text="Назад",
        callback_data=back.back,
    )
    builder.adjust(2,1)
    return builder.as_markup()