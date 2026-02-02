from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.callback_text import Back, Start


def build_renew_keyboard(only_back: bool = False):
    builder = InlineKeyboardBuilder()

    if only_back:
        builder.button(
            text="Назад",
            callback_data=Back.CHECK_BACK
        )

    else:
        builder.button(
            text="💳 Приобрести подписку",
            callback_data=Start.BUY_SUB
        )

        builder.button(
            text="Назад",
            callback_data=Back.CHECK_BACK
        )

    builder.adjust(1,1)
    return builder.as_markup()