import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.admin_callback_text import AdminTariffs, AdminTariffsActions
from callbacks.admin_tariff_callbackdata import AdminTariffCB
from core.tariff import render_tariffs_list
from core.text import AdminAllTariffText
from services.admin_tariffs import get_specific_tariff, toggle_tariff_field
from keyboards.admin_main_menu import build_main_menu
from keyboards.admin_tariffs_keyboard import build_admin_tariff_detail_keyboard

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == AdminTariffs.TARIFFS_MENU)
async def open_tariffs_menu(
    query: CallbackQuery,
    session: AsyncSession,
):
    #Главное меню управления тарифами.

    await render_tariffs_list(
        query=query,
        session=session,
    )


@router.callback_query(AdminTariffCB.filter(F.action == AdminTariffsActions.DETAIL))
async def show_tariff_detail(
    query: CallbackQuery,
    callback_data: AdminTariffCB,
    session: AsyncSession,
):
    """
    Детальная информация по тарифу и действия над ним.
    """
    tariff = await get_specific_tariff(
        query=query,
        session=session,
        callback_data=callback_data,
    )


    text = AdminAllTariffText.TARIFF_DETAILED_LINE.format(
        id=tariff.id,
        title=tariff.title,
        days=tariff.days,
        price=tariff.price,
        payload=tariff.payload,
        hot="да" if tariff.hot else "нет",
        is_active="да" if tariff.is_active else "нет",
    )

    keyboard = build_admin_tariff_detail_keyboard(tariff=tariff)

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await query.answer()


@router.callback_query(AdminTariffCB.filter(F.action == AdminTariffsActions.TOGGLE_ACTIVE))
async def toggle_tariff_active(
    query: CallbackQuery,
    callback_data: AdminTariffCB,
    session: AsyncSession,
):
    await toggle_tariff_field(
        query=query,
        callback_data=callback_data,
        session=session,
        field_name="is_active",
    )

    await show_tariff_detail(query=query, callback_data=callback_data, session=session)


@router.callback_query(AdminTariffCB.filter(F.action == AdminTariffsActions.TOGGLE_HOT))
async def toggle_tariff_hot(
    query: CallbackQuery,
    callback_data: AdminTariffCB,
    session: AsyncSession,
):
    await toggle_tariff_field(
        query=query,
        callback_data=callback_data,
        session=session,
        field_name="hot",
    )

    await show_tariff_detail(query=query, callback_data=callback_data, session=session)


@router.callback_query(AdminTariffCB.filter(F.action == AdminTariffsActions.DELETE))
async def delete_tariff(
    query: CallbackQuery,
    callback_data: AdminTariffCB,
    session: AsyncSession,
):
    tariff = await get_specific_tariff(
        session=session,
        callback_data=callback_data,
        query=query,
        deleting=True
    )

    await session.delete(tariff)
    await session.commit()

    await render_tariffs_list(
        query=query,
        session=session,
        text="Тариф удалён.\n\nМеню управления тарифами:"
    )


@router.callback_query(AdminTariffCB.filter(F.action == AdminTariffsActions.BACK_TO_THE_LIST))
async def back_to_tariffs_list(
    query: CallbackQuery,
    session: AsyncSession,
):
    await render_tariffs_list(
        query=query,
        session=session,
    )


@router.callback_query(F.data == AdminTariffs.BACK_TO_ADMIN_MENU)
async def back_to_admin_main_menu(query: CallbackQuery):
    """
    Возврат в главное админ-меню.
    """
    await query.message.edit_text(
        text="Меню администратора",
        reply_markup=build_main_menu(),
    )
    await query.answer()

