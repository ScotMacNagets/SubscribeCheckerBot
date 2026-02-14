from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.admin_tariff_callbackdata import AdminTariffCB
from core.models import Tariff
from core.tariff import get_tariff_by_field


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