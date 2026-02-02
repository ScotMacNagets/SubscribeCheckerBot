import logging
from typing import Callable

from aiogram.types import CallbackQuery

from core.text import StartHandler, TariffHandler
from keyboards.start_keyboard import build_start_keyboard
from keyboards.tariff_keyboard import build_tariff_keyboard

logger = logging.getLogger(__name__)


MENUS: dict[int, tuple[str, Callable]] = {
    1: (StartHandler.START, build_start_keyboard),
    2: (TariffHandler.TARIFF, build_tariff_keyboard),
}


async def show_menu(callback_query: CallbackQuery, menu_key: int):
    if menu_key not in MENUS:
        logger.info(
            "Не удалось найти нужное меню в списке"
        )
        return

    text, keyboard = MENUS[menu_key]

    await callback_query.message.edit_text(
        text=text,
        reply_markup=keyboard(),
    )
