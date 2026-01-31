from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.payment_keyboard import build_payment_keyboard, confirm_pay, cancel_pay, back
from .helpers import show_menu
from .states import BuySubscription
from keyboards.start_keyboard import buy_sub

router = Router()



@router.callback_query(F.data == buy_sub)
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
    tariff = query.data.split("_")[1]

    await state.update_data(tariff=tariff)

    await state.set_state(BuySubscription.confirming_payment)


    await query.answer()
    await query.message.edit_text(
        text=f"Тариф {tariff}\n\n"
        "Подтвердить оплату?",
        reply_markup=build_payment_keyboard(),
    ),

@router.callback_query(
    BuySubscription.confirming_payment,
    F.data == confirm_pay,
)
async def confirming_payment_callback(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tariff = data["tariff"]

    # Вставить логику оплаты и работы с бд

    await query.answer()
    await query.message.edit_text(
        f"Оплата прошла успешно!\n Тариф на {tariff}"
    )

    await state.clear()

@router.callback_query((F.data == cancel_pay))
async def to_main_menu(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.answer()
    await show_menu(
        callback_query=query,
        menu_key=1,
    )


@router.callback_query(F.data == back)
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


