import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.admin.users.helpers import _format_user_detail, get_user_and_days
from handlers.admin.users.users_states import AdminUserStates
from keyboards.admin_callback_text import AdminUsers, AdminUserActions
from keyboards.admin_users_keyboard import (
    build_admin_main_users_keyboard,
    build_user_actions_keyboard,
)
from services import admin_users as admin_users_service


logger = logging.getLogger(__name__)

router = Router()

@router.callback_query(F.data == AdminUsers.HUMAN_RESOURCE)
async def users_main_menu(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text(
        text="Меню управления юзерами",
        reply_markup=build_admin_main_users_keyboard(),
    )

@router.callback_query(F.data == AdminUsers.SEARCH_BY_USERNAME)
async def ask_user_id_for_search(
    query: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(AdminUserStates.SEARCH_BY_USERNAME)
    await query.answer()
    await query.message.edit_text(
        text=(
            "Введите username пользователя, которого нужно найти."
        )
    )


@router.message(StateFilter(AdminUserStates.SEARCH_BY_USERNAME))
async def handle_user_search_by_id(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    username = message.text.strip().lstrip("@")

    user = await admin_users_service.get_user_by_username(session=session, username=username)

    if not user:
        await message.answer(
            text=f"Пользователь с username {username} не найден.",
            reply_markup=build_admin_main_users_keyboard(),
        )
        await state.clear()
        return

    text = _format_user_detail(user)
    await message.answer(
        text=text,
        reply_markup=build_user_actions_keyboard(username=username),
        parse_mode="HTML",
    )
    await state.clear()


def _parse_user_id_from_callback(data: str) -> int | None:
    """
    Ожидаемый формат: "<action>:<user_id>".
    """
    try:
        _, raw_id = data.split(":", maxsplit=1)
        return int(raw_id)
    except (ValueError, IndexError):
        return None


@router.callback_query(F.data.startswith("extend_"))
async def extend_7_days(
    query: CallbackQuery,
    session: AsyncSession,
):
    days, username = get_user_and_days(query=query)
    days = int(days)

    if username is None:
        await query.answer("Некорректные данные.", show_alert=True)
        return

    user = await admin_users_service.extend_subscription(
        session=session,
        username=username,
        days=days,
    )
    await query.answer()

    if not user:
        await query.message.edit_text(
            text="Пользователь не найден.",
            reply_markup=build_admin_main_users_keyboard(),
        )
        return

    text = _format_user_detail(user)
    await query.message.edit_text(
        text=text,
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("admin_user_cancel_sub"))
async def cancel_subscription(
    query: CallbackQuery,
    session: AsyncSession,
):
    _, username = query.data.split(":")
    if username is None:
        await query.answer("Некорректные данные.", show_alert=True)
        return

    user = await admin_users_service.set_subscription_end(
        session=session,
        username=username,
        cancel=True,
    )
    await query.answer()

    if not user:
        await query.message.edit_text(
            text="Пользователь не найден.",
            reply_markup=build_admin_main_users_keyboard(),
        )
        return

    text = _format_user_detail(user)
    await query.message.edit_text(
        text=text,
        reply_markup=build_user_actions_keyboard(username=username),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("admin_user_set_end"))
async def ask_new_end_date(
    query: CallbackQuery,
    state: FSMContext,
):
    """
    Запрос новой даты окончания подписки в формате ДД.ММ.ГГГГ.
    """

    _, username = query.data.split(":")
    if username is None:
        await query.answer("Некорректные данные.", show_alert=True)
        return

    await state.update_data(target_username=username)
    await state.set_state(AdminUserStates.SET_END_DATE)

    await query.answer()
    await query.message.edit_text(
        text=(
            f"Введите новую дату окончания подписки для пользователя {username} "
            "в формате ДД.ММ.ГГГГ.\n"
            "Например: 25.12.2026\n"
        )
    )


@router.message(StateFilter(AdminUserStates.SET_END_DATE))
async def handle_new_end_date(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    """
    Обработка введённой даты окончания подписки.
    """

    raw = message.text.strip()
    try:
        new_date = datetime.strptime(raw, "%d.%m.%Y").date()
    except ValueError:
        await message.answer(
            "Некорректный формат даты. Используйте ДД.ММ.ГГГГ, например 25.12.2026, "
        )
        return

    data = await state.get_data()
    username = data.get("target_username")
    if username is None:
        await message.answer("Не удалось определить пользователя. Попробуйте снова через меню админа.")
        await state.clear()
        return

    user = await admin_users_service.set_subscription_end(
        session=session,
        username=username,
        new_end=new_date,
    )

    await state.clear()

    if not user:
        await message.answer(
            text="Пользователь не найден.",
            reply_markup=build_admin_main_users_keyboard(),
        )
        return

    text = _format_user_detail(user)
    await message.answer(
        text=text,
        reply_markup=build_user_actions_keyboard(username=username),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("admin_user_delete"))
async def delete_user(
    query: CallbackQuery,
    session: AsyncSession,
):
    _, username = query.data.split(":")
    deleted = await admin_users_service.delete_user(
        session=session,
        username=username,
    )
    await query.answer()

    if not deleted:
        await query.message.edit_text(
            text="Пользователь не найден или уже удалён.",
            reply_markup=build_admin_main_users_keyboard(),
        )
        return

    await query.message.edit_text(
        text=f"Пользователь с username {username} удалён из базы данных.",
        reply_markup=build_admin_main_users_keyboard(),
    )


@router.callback_query(F.data.startswith("admin_back_main"))
async def back_to_admin_menu(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text(
        text="Админ: управление пользователями",
        reply_markup=build_admin_main_users_keyboard(),
    )
