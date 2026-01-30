from aiogram.utils.keyboard import InlineKeyboardBuilder

one_month = "1 месяц"
return_to_start_menu = "назад"

def build_tariff_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="1 месяц",
        callback_data=one_month,
    )
    builder.button(
        text="Назад",
        callback_data=return_to_start_menu,
    )
    builder.adjust(1)
    return builder.as_markup()
