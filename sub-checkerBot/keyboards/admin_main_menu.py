from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.admin_callback_text import AdminUsers, AdminTariffs


def build_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Управление пользователями",
        callback_data=AdminUsers.HUMAN_RESOURCE
    )
    builder.button(
        text="Управление тарифами",
        callback_data=AdminTariffs.TARIFFS_MENU,
    )

    return builder.as_markup()