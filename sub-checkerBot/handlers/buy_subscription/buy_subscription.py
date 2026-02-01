from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.tariff import TARIFFS
from keyboards.payment_keyboard import build_payment_keyboard
from services.sub_add_and_check import add_or_update_subscription
from .helpers import show_menu
from .states import BuySubscription
from keyboards.callback_text import start, payment, back

router = Router()



@router.callback_query(F.data == start.buy_sub)
async def buy_sub_callback(query: CallbackQuery, state: FSMContext):
    await state.set_state(BuySubscription.choosing_tariff)
    await query.answer()
    await show_menu(
        callback_query=query,
        menu_key=2
    )

@router.callback_query(
    BuySubscription.choosing_tariff,
    F.data.startswith("plan_"),
)
async def tariff_callback(query: CallbackQuery, state: FSMContext):
    tariff_id = query.data
    tariff = TARIFFS[tariff_id].title

    await state.update_data(tariff_id=tariff_id)

    await state.set_state(BuySubscription.confirming_payment)


    await query.answer()
    await query.message.edit_text(
        text=f"Тариф {tariff}\n\n"
        "Подтвердить оплату?",
        reply_markup=build_payment_keyboard(),
    ),

@router.callback_query(
    BuySubscription.confirming_payment,
    F.data == payment.confirm_pay,
)
async def confirming_payment_callback(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tariff_id = data["tariff_id"]

    tariff = TARIFFS[tariff_id]

    prices = [
        LabeledPrice(
            label=f"Подписка {tariff.title}",
            amount=tariff.price
        )
    ]

    await query.message.answer_invoice(
        title=f"Подписка",
        description=tariff.title,
        payload=tariff.payload,
        provider_token=str(settings.payment.token),
        currency="RUB",
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

    tariff = next(
        (
            t for t in TARIFFS.values() if t.payload == payload
        ),
        None
    )
    print("Received payload:", message.successful_payment.invoice_payload)
    print("Available tariffs:", [t.payload for t in TARIFFS.values()])
    if tariff is None:
        await message.answer("❌ Неизвестный тариф. Обратитесь к поддержке.")
        return

    new_end_date = await add_or_update_subscription(
        session=session,
        user_id=user_id,
        days=tariff.days,
    )

    await message.answer(
        f"✅ Оплата прошла успешно!\n"
        f"Тариф: {tariff.title}\n"
        f"Подписка активна до {new_end_date}"
    )
    await state.clear()



@router.callback_query((F.data == payment.cancel_pay))
async def to_main_menu(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.answer()
    await show_menu(
        callback_query=query,
        menu_key=1,
    )


@router.callback_query(F.data == back.back)
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


