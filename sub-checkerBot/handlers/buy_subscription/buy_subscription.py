import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from core import constants
from core.config import settings
from core.tariff import TARIFFS
from core.text import TariffHandler, InvoiceHandler, SuccessfulPayment
from keyboards.payment_keyboard import build_payment_keyboard
from services.sub_add_and_check import (
    add_or_update_subscription,
    add_user_to_channel,
    create_channel_invite_link,
)
from handlers.helpers import show_menu
from .states import BuySubscription
from keyboards.callback_text import Start, Payment, Back

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == Start.BUY_SUB)
async def buy_sub_callback(query: CallbackQuery, state: FSMContext):
    await state.set_state(BuySubscription.choosing_tariff)
    await query.answer()
    await show_menu(
        callback_query=query,
        menu_key=2
    )


@router.callback_query(
    BuySubscription.choosing_tariff,
    F.data.startswith(constants.TARIFF_CALLBACK_PREFIX),
)
async def tariff_callback(query: CallbackQuery, state: FSMContext):
    """
    Пользователь подтверждает или отменяет оплату
    """
    tariff_id = query.data
    tariff = TARIFFS[tariff_id].title

    await state.update_data(tariff_id=tariff_id)
    await state.set_state(BuySubscription.confirming_payment)

    text = TariffHandler.TARIFF_SELECTED.format(title=tariff)

    await query.answer()
    await query.message.edit_text(
        text=text,
        reply_markup=build_payment_keyboard(),
    ),


@router.callback_query(
    BuySubscription.confirming_payment,
    F.data == Payment.CONFIRM_PAY,
)
async def confirming_payment_callback(query: CallbackQuery, state: FSMContext):
    # Генерируем счет для пользователя в соотвествии с тарифом
    data = await state.get_data()
    tariff_id = data["tariff_id"]

    tariff = TARIFFS[tariff_id]

    prices = [
        LabeledPrice(
            label=InvoiceHandler.INVOICE_LABEL,
            amount=tariff.price
        )
    ]
    await query.message.answer_invoice(
        title=InvoiceHandler.INVOICE_TITLE,
        description=tariff.title,
        payload=tariff.payload,
        provider_token=str(settings.payment.token),
        currency=InvoiceHandler.CURRENCY,
        prices=prices,
    )

    await query.answer()


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(
        message: Message,
        session: AsyncSession,
        state: FSMContext,
):
    user_id = message.from_user.id
    payload = message.successful_payment.invoice_payload
    payment_amount = message.successful_payment.total_amount

    logger.info(
        "Получена успешная оплата от пользователя %s, payload: %s, сумма: %s",
        user_id,
        payload,
        payment_amount,
    )

    tariff = next(
        (
            t for t in TARIFFS.values() if t.payload == payload
        ),
        None
    )

    if tariff is None:
        logger.error(
            "Неизвестный тариф для payload: %s. Доступные тарифы: %s",
            payload,
            [t.payload for t in TARIFFS.values()]

        )
        await message.answer(SuccessfulPayment.UNKNOWN_TARIFF)
        await state.clear()
        return

    # Проверка суммы платежа (опционально, для безопасности)
    if payment_amount != tariff.price:
        logger.warning(
            "Несоответствие суммы платежа для пользователя %s: "
            "ожидалось %s, получено %s"
            ,
            user_id,
            tariff.price,
            payment_amount
        )

    try:
        # Добавляем или продлеваем подписку
        new_end_date = await add_or_update_subscription(
            session=session,
            user_id=user_id,
            days=tariff.days,
        )
        logger.info(
            "Подписка для пользователя %s обновлена до %s",
            user_id,
            new_end_date
        )

        # Добавляем пользователя в канал
        channel_added = await add_user_to_channel(user_id)
        end_date = new_end_date.strftime('%d.%m.%Y')


        if channel_added:
            # Генерируем инвайт-ссылку для удобства пользователя)
            invite_link = await create_channel_invite_link(user_id=user_id)
            success_message = (
                SuccessfulPayment.SUCCESSFUL_INVITE.format(
                    title=tariff.title,
                    end_date=end_date,
                )
            )

            if invite_link:
                success_message += SuccessfulPayment.INVITE_LINK.format(invite_link=invite_link)
        else:
            success_message = (
                SuccessfulPayment.UNSUCCESSFUL_INVITE.format(
                    title=tariff.title,
                    end_date=end_date,
                    admin_username=settings.admin.support,
                )

            )

        await message.answer(success_message, parse_mode="HTML")
        await state.clear()

    except Exception as e:
        logger.error(
            "Ошибка при обработке оплаты для пользователя %s: %s",
            user_id,
            e,
            exc_info=True
        )
        await message.answer(
            SuccessfulPayment.ACTIVATE_ERROR.format(
                admin_username=settings.admin.support,
            ),
            parse_mode="HTML",
        )
        await state.clear()



@router.callback_query(F.data == Payment.CANCEL_PAY)
async def to_main_menu(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.answer()
    await show_menu(
        callback_query=query,
        menu_key=1,
    )


@router.callback_query(F.data == Back.BACK)
async def go_back(query: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state == BuySubscription.confirming_payment.state:
        await state.set_state(BuySubscription.choosing_tariff)
        await show_menu(
            callback_query=query,
            menu_key=2,
        )

    elif current_state == BuySubscription.choosing_tariff.state:
        await state.clear()
        await show_menu(
            callback_query=query,
            menu_key=1,
        )
    await query.answer()


