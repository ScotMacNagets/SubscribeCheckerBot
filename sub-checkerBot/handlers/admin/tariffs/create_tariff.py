from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.admin_callback_text import AdminTariffsActions
from core.constants import CommandText
from core.text import AdminAllTariffText, AdminTariffKeyboard
from handlers.admin.helpers import open_admin_menu_helper
from handlers.admin.tariffs.fsm_states import CreateTariff
from keyboards.admin_tariffs_keyboard import create_tariff_confirmation_keyboard, back_to_admin_menu_keyboard
from services.admin_tariffs import create_tariff

router = Router()


@router.callback_query(F.data == AdminTariffsActions.START_CREATING)
async def stat_create_tariff(
        query: CallbackQuery,
        state: FSMContext,
):
    await state.set_state(CreateTariff.title)
    await query.message.edit_text(
        text=AdminAllTariffText.START_MESSAGE
    )

@router.message(CreateTariff.title)
async def get_title(
        message: Message,
        state: FSMContext,
):
    await state.update_data(
        title=message.text,
    )
    await state.set_state(CreateTariff.price)
    await message.answer(AdminAllTariffText.SET_TARIFF_PRICE)


@router.message(CreateTariff.price)
async def get_price(
        message: Message,
        state: FSMContext,
):
    price = int(message.text)
    await state.update_data(
        price=price,
    )

    await state.set_state(CreateTariff.days)
    await message.answer(AdminAllTariffText.SET_DURATION_IN_DAYS)


@router.message(CreateTariff.days)
async def get_days_and_confirming(
        message: Message,
        state: FSMContext,
):
    days = int(message.text)
    await state.update_data(
        days=days,
    )

    data = await state.get_data()

    text = (
        AdminAllTariffText.CONFIRMING_TEXT.format(
            title=data['title'],
            price=data['price'],
            days=data['days'],
        )
    )
    await state.set_state(CreateTariff.confirm)
    await message.answer(
        text=text,
        reply_markup=create_tariff_confirmation_keyboard()
    )


@router.callback_query(
    F.data == AdminTariffsActions.CONFIRM,
    CreateTariff.confirm
)
async def confirmed_tariff(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    data = await state.get_data()

    await create_tariff(
        session=session,
        data=data,
    )

    await state.clear()
    await callback.message.edit_text(
        text=AdminTariffKeyboard.CONFIRMED
    )
    await callback.answer()


@router.callback_query(
    F.data == AdminTariffsActions.CANCEL,
    CreateTariff.confirm
)
async def canceled_tariff(
        callback: CallbackQuery,
        state: FSMContext,
):
    await state.clear()
    await callback.message.edit_text(
        text=AdminTariffKeyboard.CANCELED
    )
    await callback.answer()

