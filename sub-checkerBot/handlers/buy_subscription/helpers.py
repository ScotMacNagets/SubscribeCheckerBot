from aiogram.types import CallbackQuery

from keyboards.start_keyboard import build_start_keyboard
from keyboards.tariff_keyboard import build_tariff_keyboard


MENUS = {
    1: [
        "Приветствую в моем тг боте. Тут ты можешь купить подписку в закрытый тг канал",
        build_start_keyboard
    ],
    2: [
        "Отлично! Теперь выбери тариф😊", build_tariff_keyboard
    ],
}


async def show_menu(callback_query: CallbackQuery, menu_key: int):
    if menu_key not in MENUS:
        #вставить логи
        return

    text, keyboard = MENUS[menu_key]

    await callback_query.message.edit_text(
        text=text,
        reply_markup=keyboard(),
    )
