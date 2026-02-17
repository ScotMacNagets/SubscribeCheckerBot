from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.admin_tariff_callbackdata import AdminTariffCB
from core.models import Tariff
from core.text import AdminTariffMenu
from keyboards.admin_tariffs_keyboard import build_admin_tariffs_list_keyboard


async def get_specific_tariff(
        session: AsyncSession,
        callback_data: AdminTariffCB,
        query: CallbackQuery,
        deleting: bool = False,
) -> Tariff | None:

    tariff = await get_tariff_by_field(
        session=session,
        field=Tariff.id,
        value=callback_data.tariff_id,
    )
    if tariff is None:
        if deleting:
            return query.message.answer(
                text="Тариф уже удалён или не найден"
            )
        return query.message.answer(
            text="Тариф не найден"
        )
    return tariff


async def toggle_tariff_field(
        query: CallbackQuery,
        callback_data: AdminTariffCB,
        session: AsyncSession,
        field_name: str,
):
    tariff = await get_specific_tariff(
        session=session,
        callback_data=callback_data,
        query=query,
    )

    current_value = getattr(tariff, field_name)
    setattr(tariff, field_name, not bool(current_value))

    await session.commit()
    await session.refresh(tariff)


async def get_all_active_tariffs(session: AsyncSession) -> list[Tariff]:

    stmt = (
        select(Tariff)
        .where(Tariff.is_active == True)
        .order_by(Tariff.sort_order, Tariff.id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_all_tariffs(session: AsyncSession) -> list[Tariff]:

    stmt = select(Tariff).order_by(Tariff.sort_order, Tariff.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_tariff_by_field(
        session: AsyncSession,
        field,
        value,
) -> Tariff | None:
    stmt = select(Tariff).where(field == value)
    result = await session.execute(stmt)
    return result.scalars().one_or_none()


async def render_tariffs_list(
        query: CallbackQuery,
        session: AsyncSession,
        text: str = AdminTariffMenu.TARIFF_MENU,
):
    tariffs = await get_all_tariffs(session=session)
    keyboard = build_admin_tariffs_list_keyboard(tariffs=tariffs)

    text = text

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )
    await query.answer()


async def create_tariff(
        session: AsyncSession,
        data: dict,
) -> Tariff:
    days = int(data["days"])
    months = days // 30

    month_label = "month" if months == 1 else "months"
    if months >= 1:
        payload = f"sub_{months}_{month_label}"
    else:
        payload = f"sub_{days}_days"


    tariff = Tariff(
        **data,
        payload=payload
    )
    session.add(tariff)
    await session.commit()
    await session.refresh(tariff)
    return tariff
