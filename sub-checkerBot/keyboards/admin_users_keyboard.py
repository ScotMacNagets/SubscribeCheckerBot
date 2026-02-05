from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .admin_callback_text import AdminUsers, AdminUserActions


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


def build_user_actions_keyboard(username) -> InlineKeyboardMarkup:
    """
    Клавиатура действий над конкретным пользователем.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="➕ +7 дней",
        callback_data=f"{AdminUserActions.EXTEND_7}:{username}",
    )
    builder.button(
        text="➕ +30 дней",
        callback_data=f"{AdminUserActions.EXTEND_30}:{username}",
    )
    builder.button(
        text="➕ +90 дней",
        callback_data=f"{AdminUserActions.EXTEND_90}:{username}",
    )
    builder.button(
        text="📅 Установить дату",
        callback_data=f"{AdminUserActions.SET_END_DATE}:{username}",
    )
    builder.button(
        text="✂ Отменить подписку",
        callback_data=f"{AdminUserActions.CANCEL_SUB}:{username}",
    )
    builder.button(
        text="🗑 Удалить пользователя",
        callback_data=f"{AdminUserActions.DELETE_USER}:{username}",
    )
    builder.button(
        text="⬅ В админ-меню",
        callback_data=AdminUserActions.BACK_TO_ADMIN_MENU,
    )
    builder.adjust(3, 2, 1)
    return builder.as_markup()

