import logging
from datetime import datetime, date

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.admin_user_callbackdata import AdminUserCB
from core.text import AdminUsersMenu, AdminUserAction, AdminMenu
from handlers.admin.helpers import open_admin_menu_helper
from services.admin_users import render_user
from handlers.admin.users.users_states import AdminUserStates
from callbacks.admin_callback_text import AdminUsers, AdminUserActions
from keyboards.admin_users_keyboard import build_admin_main_users_keyboard
from services import admin_users as admin_users_service


logger = logging.getLogger(__name__)

router = Router()

@router.callback_query(F.data == AdminUsers.HUMAN_RESOURCE)
async def users_main_menu(query: CallbackQuery):
    await query.answer()
    logger.info("Users menu opened | %s", query.from_user.id)
    await query.message.edit_text(
        text=AdminUsersMenu.USER_MANAGE_MENU,
        reply_markup=build_admin_main_users_keyboard(),
    )


@router.callback_query(F.data == AdminUsers.SEARCH_BY_USERNAME)
async def ask_user_id_for_search(
    query: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(AdminUserStates.SEARCH_BY_USERNAME)
    await query.answer()
    logger.info("Search by username | %s", query.from_user.id)
    await query.message.edit_text(
        text=AdminUserAction.ENTER_USERNAME
    )


@router.message(StateFilter(AdminUserStates.SEARCH_BY_USERNAME))
async def handle_user_search_by_id(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    username = message.text.strip().lstrip("@")
    logger.info("Searching for user with username %s | by %s", username, message.from_user.id)

    user = await admin_users_service.get_user_by_username(session=session, username=username)

    if not user:
        await message.edit_text(
            text=AdminUserAction.USER_NOT_FOUND,
        )
        await back_to_users_admin_menu(message=message)
        logger.info("User %s not found | by %s", username, message.from_user.id)
        return

    logger.info("User %s found | by %s", username, message.from_user.id)


    await render_user(
        user=user,
        username=username,
        target=message,
        reply_markup=build_admin_main_users_keyboard(),
    )
    await state.clear()


@router.callback_query(AdminUserCB.filter(F.action == AdminUserActions.EXTEND))
async def extend_sub_for_user(
    query: CallbackQuery,
    callback_data: AdminUserCB,
    session: AsyncSession,
):
    logger.info("Extending sub for %s | by %s", callback_data.username, query.from_user.id)

    if not callback_data.username or not callback_data.days:
        logger.warning(
            "Invalid data received for extension: %s | by %s",
            callback_data.username,
            query.from_user.id,
        )
        await query.answer(text=AdminUserAction.INCORRECT_DATA, show_alert=True)
        return
    try:
        user = await admin_users_service.extend_subscription(
            session=session,
            username=callback_data.username,
            days=callback_data.days,
        )
    except Exception as error:
        logger.exception(
            "Failed to extend subscription for %s | by %s",
            callback_data.username,
            query.from_user.id,
        )
        raise

    logger.info(
        "User subscription extended successfully for %s | by %s",
        callback_data.username,
        query.from_user.id,
    )

    await render_user(
        user=user,
        username=callback_data.username,
        target=query,
        is_callback=True,
        reply_markup=build_admin_main_users_keyboard(),
    )


@router.callback_query(AdminUserCB.filter(F.action == AdminUserActions.CANCEL_SUB))
async def cancel_subscription(
    query: CallbackQuery,
    callback_data: AdminUserCB,
    session: AsyncSession,
):
    logger.info(
        "Cancelling subscription for %s | by %s",
        callback_data.username,
        query.from_user.id,
    )
    if not callback_data.username:
        logger.error(
            "Invalid data received for cancelation: %s | by %s",
            callback_data.username,
            query.from_user.id,
        )
        await query.answer(AdminUserAction.INCORRECT_DATA, show_alert=True)
        return

    user = await admin_users_service.set_subscription_end(
        session=session,
        username=callback_data.username,
        cancel=True,
    )

    logger.info(
        "User subscription cancelled successfully for %s | by %s",
        callback_data.username,
        query.from_user.id,
    )

    await render_user(
        user=user,
        username=callback_data.username,
        target=query,
        is_callback=True,
        reply_markup=build_admin_main_users_keyboard(),
    )


@router.callback_query(AdminUserCB.filter(F.action == AdminUserActions.SET_END_DATE))
async def ask_new_end_date(
    query: CallbackQuery,
    callback_data: AdminUserCB,
    state: FSMContext,
):
    logger.info(
        "Set end date requested for %s | by %s",
        callback_data.username,
        query.from_user.id,
    )
    if not callback_data.username:
        logger.error(
            "Invalid data received for setting new date: %s | by %s",
            callback_data.username,
            query.from_user.id,
        )
        await query.answer(AdminUserAction.INCORRECT_DATA, show_alert=True)
        return

    await state.update_data(target_username=callback_data.username)
    await state.set_state(AdminUserStates.SET_END_DATE)
    logger.info(
        "Setting new end date for %s started | by %s",
        callback_data.username,
        query.from_user.id,
    )

    await query.answer()
    await query.message.edit_text(
        text=AdminUserAction.SET_NEW_DATE.format(username=callback_data.username)
    )


@router.message(StateFilter(AdminUserStates.SET_END_DATE))
async def handle_new_end_date(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):

    raw = message.text.strip()
    today = date.today()

    new_date = datetime.strptime(raw, "%d.%m.%Y").date()

    if new_date < today:
        await message.answer(
            AdminUserAction.PAST_DATE
        )
        return
    logger.warning(
        "Invalid data format: %s | by %s",
        raw,
        message.from_user.id,
    )
    await message.answer(
        AdminUserAction.INCORRECT_DATA_FORMAT
    )

    data = await state.get_data()
    username = data.get("target_username")
    if username is None:
        await message.answer(text=AdminUserAction.CANNOT_IDENTIFY_USER)
        logger.error(
            "Invalid data format: %s | by %s",
            raw,
            message.from_user.id,
        )
        await state.clear()
        return

    user = await admin_users_service.set_subscription_end(
        session=session,
        username=username,
        new_end=new_date,
    )

    logger.info(
        "Successfully set new date for %s | by %s",
        username,
        message.from_user.id,
    )

    await state.clear()


    await render_user(
        user=user,
        username=username,
        target=message,
        reply_markup=build_admin_main_users_keyboard(),
    )


@router.callback_query(AdminUserCB.filter(F.action == AdminUserActions.DELETE_USER))
async def delete_user(
    query: CallbackQuery,
    callback_data: AdminUserCB,
    session: AsyncSession,
):
    logger.info("Deleting user %s requested | by %s", callback_data.username, query.from_user.id)
    username = callback_data.username
    deleted = await admin_users_service.delete_user(
        session=session,
        username=username,
    )
    await query.answer()

    if not deleted:
        await query.message.edit_text(
            text=AdminUserAction.USER_NOT_FOUND_OR_DELETED,
            reply_markup=build_admin_main_users_keyboard(),
        )
        return

    logger.info("User %s successfully deleted | by %s", callback_data.username, query.from_user.id)

    await render_user(
        username=username,
        target=query,
        is_callback=True,
        short=True,
        reply_markup=build_admin_main_users_keyboard()
    )


@router.callback_query(F.data == AdminUserActions.BACK_TO_USERS_ADMIN_MENU)
async def back_to_users_admin_menu(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text(
        text=AdminUsersMenu.USER_MANAGE_MENU,
        reply_markup=build_admin_main_users_keyboard(),
    )

@router.callback_query(F.data == AdminUserActions.BACK_TO_ADMIN_MENU)
async def back_to_admin_menu(
    query: CallbackQuery,
):
    # await query.answer()
    # await query.message.edit_text(
    #     text=AdminMenu.MENU,
    #     reply_markup=build_main_menu(username=query.from_user.username),
    # )
    await open_admin_menu_helper(query=query)
