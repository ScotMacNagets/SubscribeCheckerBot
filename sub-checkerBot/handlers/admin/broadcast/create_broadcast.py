import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.admin_broadcast_callbackdata import BroadcastCB
from callbacks.admin_callback_text import AdminBroadcast, AdminBroadcastActions
from core.bot_instance import bot
from core.text import AdminBroadcastText
from handlers.admin.broadcast.fsm_states import BroadcastState
from keyboards.admin_broadcast_keyboard import build_broadcast_keyboard, builder_confirm_broadcast_keyboard
from keyboards.admin_tariffs_keyboard import back_to_admin_menu_keyboard
from services.admin_broadcast import get_all_users

router = Router()

logger = logging.getLogger(__name__)

@router.callback_query(F.data == AdminBroadcast.BROADCAST_MENU)
async def open_broadcast_menu(query: CallbackQuery):
    await query.message.edit_text(
        text=AdminBroadcastText.BROADCAST_MENU,
        reply_markup=build_broadcast_keyboard()
    )

@router.callback_query(BroadcastCB.filter(F.action == AdminBroadcastActions.START))
async def broadcast_start(
        query: CallbackQuery,
        state: FSMContext
):
    await state.set_state(BroadcastState.waiting_for_message)
    await query.message.edit_text(
        text=AdminBroadcastText.SEND_MESSAGE,
    )


@router.message(BroadcastState.waiting_for_message)
async def get_broadcast_text(
        message: Message,
        state: FSMContext,
):
    await state.update_data(message=message.text)

    await state.set_state(BroadcastState.confirm)

    await message.answer(
        text=AdminBroadcastText.CONFIRM_MESSAGE.format(message=message.text),
        reply_markup=builder_confirm_broadcast_keyboard()
    )


@router.callback_query(BroadcastCB.filter(F.action == AdminBroadcastActions.CONFIRM))
async def confirm_broadcast(
        query: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    data = await state.get_data()
    text = data.get("message")

    users = await get_all_users(
        session=session
    )

    for user in users:
        try:
            await bot.send_message(user.id, text)
        except Exception as error:
            logger.error("Cannot sent message to user", exc_info=error)

    await state.clear()
    await query.message.edit_text(
        text=AdminBroadcastText.BROADCAST_SENT,
        reply_markup=back_to_admin_menu_keyboard()
    )


@router.callback_query(BroadcastCB.filter(F.action == AdminBroadcastActions.CANCEL))
async def cancel_broadcast(
        query: CallbackQuery,
        state: FSMContext,
):
    await state.clear()
    await query.message.edit_text(
        text=AdminBroadcastText.BROADCAST_CANCELED,
        reply_markup=back_to_admin_menu_keyboard()
    )