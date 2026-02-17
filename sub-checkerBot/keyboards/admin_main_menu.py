from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.admin_callback_text import AdminUsers, AdminTariffs, AdminTariffsActions
from core.config import settings
from core.text import AdminTariffKeyboard, AdminTariffMenu, AdminUsersMenu


def build_main_menu(username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=AdminUsersMenu.USER_MANAGE_MENU,
        callback_data=AdminUsers.HUMAN_RESOURCE,
    )

    builder.button(
        text=AdminTariffMenu.TARIFF_MENU,
        callback_data=AdminTariffs.TARIFFS_MENU,
    )

    if username == settings.admin.super_user:
        builder.button(
            text=AdminTariffKeyboard.START_CREATING,
            callback_data=AdminTariffsActions.START_CREATING
        )

    builder.adjust(1)

    return builder.as_markup()