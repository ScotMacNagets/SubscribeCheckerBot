from aiogram.types import CallbackQuery, Message

from core.text import AdminMenu
from keyboards.admin_main_menu import build_main_menu


async def open_admin_menu_helper(
        query: CallbackQuery = None,
        message: Message = None,
):
    if query:
        value = query.message.edit_text
        username = query.from_user.username
    else:
        value = message.answer
        username = message.from_user.username

    await value(
        text=AdminMenu.MENU,
        reply_markup=build_main_menu(username=username),
    )