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
    logger.info("Opened broadcast menu | by %s", query.from_user.id)
    await query.message.edit_text(
        text=AdminBroadcastText.BROADCAST_MENU,
        reply_markup=build_broadcast_keyboard(),
    )

@router.callback_query(BroadcastCB.filter(F.action == AdminBroadcastActions.START))
async def broadcast_start(
        query: CallbackQuery,
        state: FSMContext
):
    logger.info("Started creating broadcast | by %s", query.from_user.id)
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

    await state.set_state(BroadcastState.waiting_for_photo)

    await message.answer(
        text=AdminBroadcastText.SEND_PHOTO,
    )

    logger.info("Send message | by %s", message.from_user.id)


@router.message(BroadcastState.waiting_for_photo)
async def get_broadcast_text(
        message: Message,
        state: FSMContext,
):
    data = await state.get_data()
    await state.update_data(photo=message.photo[-1].file_id)

    await state.set_state(BroadcastState.confirm)

    await message.reply_photo(
        photo=message.photo[-1].file_id,
        caption=data['message'],

    )

    await message.answer(
        text=AdminBroadcastText.CONFIRM_MESSAGE.format(message=message.text),
        reply_markup=builder_confirm_broadcast_keyboard(),
    )
    logger.info("Send photo | by %s", message.from_user.id)



@router.callback_query(BroadcastCB.filter(F.action == AdminBroadcastActions.CONFIRM))
async def confirm_broadcast(
        query: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    data = await state.get_data()
    text = data.get("message")
    photo = data.get("photo")

    users = await get_all_users(
        session=session
    )

    for user in users:
        try:
            if photo is None:
                await bot.send_message(user.id, text)
            else:
                await bot.send_photo(
                    user.id,
                    photo,
                    caption=text,
                )
        except Exception as error:
            logger.error("Cannot sent message to user", exc_info=error)

    await state.clear()
    await query.message.edit_text(
        text=AdminBroadcastText.BROADCAST_SENT,
        reply_markup=back_to_admin_menu_keyboard()
    )

    logger.info("Broadcast has been sent | by %s", query.from_user.id)


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

    logger.info("Broadcast has been canceled | by %s", query.from_user.id)