from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.constants import CommandText
from handlers.admin.helpers import open_admin_menu_helper

router = Router()

@router.message(Command(CommandText.ADMIN_MENU))
async def open_admin_menu(message: Message):

    await open_admin_menu_helper(message=message)



