from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.tariff import Tariff
from keyboards.admin_tariffs_keyboard import build_admin_tariffs_list_keyboard


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
        text: str = "Меню управления тарифами"
):
    tariffs = await get_all_tariffs(session=session)
    keyboard = build_admin_tariffs_list_keyboard(tariffs=tariffs)

    text = text

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )
    await query.answer()

