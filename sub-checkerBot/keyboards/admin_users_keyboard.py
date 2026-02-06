from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.admin_callback_text import AdminUsers, AdminUserActions
from callbacks.admin_user import AdminUserCB


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
            text=f"➕ +{days} дней",
            callback_data=AdminUserCB(
                action=AdminUserActions.EXTEND,
                username=username,
                days=days,
            ).pack()
        )
    builder.button(
        text="📅 Установить дату",
        callback_data=AdminUserCB(
            action=AdminUserActions.SET_END_DATE,
            username=username,
        ).pack()
    )
    builder.button(
        text="✂ Отменить подписку",
        callback_data=AdminUserCB(
            action=AdminUserActions.CANCEL_SUB,
            username=username,
        ).pack()
    )
    builder.button(
        text="🗑 Удалить пользователя",
        callback_data=AdminUserCB(
            action=AdminUserActions.DELETE_USER,
            username=username,
        ).pack()
    )
    builder.button(
        text="⬅ В админ-меню",
        callback_data=AdminUserActions.BACK_TO_ADMIN_MENU,
    )
    builder.adjust(3, 2, 1)
    return builder.as_markup()

