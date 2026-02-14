from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.admin_callback_text import AdminUsers, AdminTariffs


def build_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Управление пользователями",
        callback_data=AdminUsers.HUMAN_RESOURCE
    )

    return builder.as_markup()