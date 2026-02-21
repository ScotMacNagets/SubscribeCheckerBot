import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.admin_callback_text import AdminTariffsActions
from core.text import AdminAllTariffText, AdminTariffKeyboard
from handlers.admin.tariffs.fsm_states import CreateTariff
from keyboards.admin_tariffs_keyboard import create_tariff_confirmation_keyboard, back_to_admin_menu_keyboard
from services.admin_tariffs import create_tariff

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == AdminTariffsActions.START_CREATING)
async def start_create_tariff(
        query: CallbackQuery,
        state: FSMContext,
):
    logger.info("New tariff creating started | by %s", query.from_user.id)
    await state.set_state(CreateTariff.title)
    await query.message.edit_text(
        text=AdminAllTariffText.START_MESSAGE
    )

@router.message(CreateTariff.title)
async def get_title(
        message: Message,
        state: FSMContext,
):
    logger.info("Set a title | by %s", message.from_user.id)
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
    logger.info("Set a price | by %s", message.from_user.id)
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
    logger.info("Set number of days | by %s", message.from_user.id)
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
        query: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    data = await state.get_data()
    try:
        await create_tariff(
            session=session,
            data=data,
        )
    except ValueError as error:
        logger.error(
            "Ошибка при создании пользователя: %s",
            error
        )
        await query.message.edit_text(AdminAllTariffText.CREATING_ERROR)


    await query.message.edit_text(
        text=AdminTariffKeyboard.CONFIRMED,
        reply_markup=back_to_admin_menu_keyboard(),
    )
    logger.info("Новый тариф успешно создан")
    await state.clear()
    await query.answer()


@router.callback_query(
    F.data == AdminTariffsActions.CANCEL,
    CreateTariff.confirm
)
async def canceled_tariff(
        query: CallbackQuery,
        state: FSMContext,
):

    await query.answer()
    await query.message.edit_text(
        text=AdminTariffKeyboard.CANCELED,
        reply_markup=back_to_admin_menu_keyboard()
    )
    logger.info("Создание нового тарифа было отменено")
    await state.clear()


