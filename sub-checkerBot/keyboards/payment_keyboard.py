from aiogram.utils.keyboard import InlineKeyboardBuilder

confirm_pay = "confirm payment"
cancel_pay = "cancel payment"
back = "back"

def build_payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="💳 Оплатить",
        callback_data=confirm_pay,
    )
    builder.button(
        text="⛔ Отменить оплату",
        callback_data=cancel_pay,
    )
    builder.button(
        text="Назад",
        callback_data=back,
    )
    builder.adjust(2,1)
    return builder.as_markup()