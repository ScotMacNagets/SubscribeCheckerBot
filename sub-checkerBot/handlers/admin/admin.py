from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.constants import CommandText
from core.text import AdminMenu
from handlers.admin.tariffs.fsm_states import CreateTariff
from keyboards.admin_main_menu import build_main_menu

router = Router()

@router.message(Command(CommandText.ADMIN_MENU))
async def open_admin_menu(message: Message):

    await message.answer(
        text=AdminMenu.MENU,
        reply_markup=build_main_menu(),
    )
