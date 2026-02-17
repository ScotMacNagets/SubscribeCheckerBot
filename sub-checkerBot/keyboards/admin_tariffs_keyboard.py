from collections.abc import Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.admin_callback_text import AdminTariffs, AdminTariffsActions, AdminUserActions
from callbacks.admin_tariff_callbackdata import AdminTariffCB
from core.models.tariff import Tariff
from core.text import AdminTariffKeyboard, GeneralButtons


def build_admin_tariffs_list_keyboard(tariffs: Sequence[Tariff]) -> InlineKeyboardMarkup:
    """
    Список тарифов для админ-меню.
    Каждая кнопка открывает детали конкретного тарифа.
    """
    builder = InlineKeyboardBuilder()

    for tariff in tariffs:
        status = (
            AdminTariffKeyboard.ACTIVE_STATUS
            if tariff.is_active
            else AdminTariffKeyboard.NON_ACTIVE_STATUS
        )

        text = AdminTariffKeyboard.TARIFF_LIST_TEXT.format(
            status=status,
            title=tariff.title,
            price=tariff.price,
        )

        builder.button(
            text=text,
            callback_data=AdminTariffCB(action=AdminTariffsActions.DETAIL, tariff_id=tariff.id).pack(),
        )

    builder.button(
        text=GeneralButtons.BACK_BUTTON,
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
        text= AdminTariffKeyboard.ACTIVE
        if tariff.is_active
        else AdminTariffKeyboard.NON_ACTIVE,

        callback_data=AdminTariffCB(
            action=AdminTariffsActions.TOGGLE_ACTIVE,
            tariff_id=tariff.id,
        ).pack(),
    )
    builder.button(
        text= AdminTariffKeyboard.HOT
        if tariff.hot
        else AdminTariffKeyboard.NOT_HOT,

        callback_data=AdminTariffCB(
            action=AdminTariffsActions.TOGGLE_HOT,
            tariff_id=tariff.id,
        ).pack(),
    )
    builder.button(
        text=AdminTariffKeyboard.DELETE,
        callback_data=AdminTariffCB(
            action=AdminTariffsActions.DELETE,
            tariff_id=tariff.id,
        ).pack(),
    )
    builder.button(
        text=AdminTariffKeyboard.BACK_TO_THE_LIST,
        callback_data=AdminTariffCB(
            action=AdminTariffsActions.BACK_TO_THE_LIST,
            tariff_id=None,
        ).pack(),
    )

    builder.adjust(2, 1, 1)
    return builder.as_markup()


def create_tariff_confirmation_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text=AdminTariffKeyboard.CONFIRM,
        callback_data=AdminTariffsActions.CONFIRM
    )

    builder.button(
        text=AdminTariffKeyboard.CANCEL,
        callback_data=AdminTariffsActions.CANCEL
    )

    builder.adjust(2)
    return builder.as_markup()
