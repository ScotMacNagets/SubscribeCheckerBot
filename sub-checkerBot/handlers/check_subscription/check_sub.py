from datetime import date

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.check_subscription.messages import self_check_text
from handlers.helpers import show_menu
from callbacks.callback_text import Start, Back
from keyboards.renew_sub_keyboard import build_renew_keyboard
from services.user_check_sub import self_check

router = Router()

@router.callback_query(F.data == Start.CHECK_SUB)
async def check_subscription(query: CallbackQuery, session: AsyncSession):
    sub_end = await self_check(
        user_id=query.from_user.id,
        session=session,
    )

    text = self_check_text(
        subscription_end=sub_end,
    )

    if not sub_end or (sub_end - date.today()).days < 0:
        keyboard = build_renew_keyboard()
    else:
        keyboard = build_renew_keyboard(only_back=True)

    await query.answer()
    await query.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.callback_query(F.data == Back.CHECK_BACK)
async def to_main_menu(query: CallbackQuery):
    await show_menu(
        callback_query=query,
        menu_key=1
    )
    await query.answer()

