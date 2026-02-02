import logging

from aiogram.types import CallbackQuery

from keyboards.start_keyboard import build_start_keyboard
from keyboards.tariff_keyboard import build_tariff_keyboard

logger = logging.getLogger(__name__)


MENUS = {
    1: [
        "Приветствую! 👋 \n"
        "Этот бот поможет Вам подключить подписку и сразу получить доступ к закрытому каналу.",
        build_start_keyboard
    ],
    2: [
        "Отлично! Теперь выбери тариф😊", build_tariff_keyboard
    ],
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
