from collections.abc import Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.admin_callback_text import AdminTariffs
from callbacks.admin_tariff_callbackdata import AdminTariffCB
from core.models.tariff import Tariff


def build_admin_tariffs_list_keyboard(tariffs: Sequence[Tariff]) -> InlineKeyboardMarkup:
    """
    Список тарифов для админ-меню.
    Каждая кнопка открывает детали конкретного тарифа.
    """
    builder = InlineKeyboardBuilder()

    for tariff in tariffs:
        status = "🟢" if tariff.is_active else "⚪️"
        text = f"{status} {tariff.title} — {tariff.price}₽"
        builder.button(
            text=text,
            callback_data=AdminTariffCB(action="detail", tariff_id=tariff.id).pack(),
        )

    builder.button(
        text="⬅ Назад",
        callback_data=AdminTariffs.BACK_TO_ADMIN_MENU,
    )

    builder.adjust(1)
    return builder.as_markup()


def build_admin_tariff_detail_keyboard(tariff: Tariff) -> InlineKeyboardMarkup:
    """
    Клавиатура действий над конкретным тарифом.
    """
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Активен" if tariff.is_active else "🚫 Неактивен",
        callback_data=AdminTariffCB(
            action="toggle_active",
            tariff_id=tariff.id,
        ).pack(),
    )
    builder.button(
        text="🔥 Горячий" if tariff.hot else "💤 Обычный",
        callback_data=AdminTariffCB(
            action="toggle_hot",
            tariff_id=tariff.id,
        ).pack(),
    )
    builder.button(
        text="🗑 Удалить",
        callback_data=AdminTariffCB(
            action="delete",
            tariff_id=tariff.id,
        ).pack(),
    )
    builder.button(
        text="⬅ К списку тарифов",
        callback_data=AdminTariffCB(
            action="back_to_list",
            tariff_id=None,
        ).pack(),
    )

    builder.adjust(2, 1, 1)
    return builder.as_markup()

