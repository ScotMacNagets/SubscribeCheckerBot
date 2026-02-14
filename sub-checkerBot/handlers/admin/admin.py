from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.text import AdminMenu
from keyboards.admin_main_menu import build_main_menu

router = Router()

@router.message(Command("admin_users"))
async def open_admin_menu(message: Message):

    await message.answer(
        text=AdminMenu.MENU,
        reply_markup=build_main_menu(),
    )
