from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.admin_callback_text import AdminUsers, AdminUserActions
from callbacks.admin_user import AdminUserCB
from core.text import AdminUsersKeyboard


def build_admin_main_users_keyboard() -> InlineKeyboardMarkup:
    """
    Главное подменю управления пользователями.
    Сейчас оставляем только поиск по ID.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔍 Поиск по ID",
        callback_data=AdminUsers.SEARCH_BY_USERNAME,
    )
    builder.adjust(1)
    return builder.as_markup()


def build_user_actions_keyboard(username: str) -> InlineKeyboardMarkup:
    """
    Клавиатура действий над конкретным пользователем.
    """
    builder = InlineKeyboardBuilder()
    for days in (7, 30, 90):
        builder.button(
            text=AdminUsersKeyboard.EXTEND_DAYS.format(days=days),
            callback_data=AdminUserCB(
                action=AdminUserActions.EXTEND,
                username=username,
                days=days,
            ).pack()
        )
    builder.button(
        text=AdminUsersKeyboard.SET_THE_DATE,
        callback_data=AdminUserCB(
            action=AdminUserActions.SET_END_DATE,
            username=username,
        ).pack()
    )
    builder.button(
        text=AdminUsersKeyboard.CANCEL_SUB,
        callback_data=AdminUserCB(
            action=AdminUserActions.CANCEL_SUB,
            username=username,
        ).pack()
    )
    builder.button(
        text=AdminUsersKeyboard.DELETE_USER,
        callback_data=AdminUserCB(
            action=AdminUserActions.DELETE_USER,
            username=username,
        ).pack()
    )
    builder.button(
        text=AdminUsersKeyboard.BACK_TO_ADMIN_MENU,
        callback_data=AdminUserActions.BACK_TO_ADMIN_MENU,
    )
    builder.adjust(3, 2, 1)
    return builder.as_markup()

