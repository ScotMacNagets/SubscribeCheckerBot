import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.constants import CommandText
from handlers.admin.helpers import open_admin_menu_helper

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command(CommandText.ADMIN_MENU))
async def open_admin_menu(message: Message):
    user_id = message.from_user.id

    try:
        await open_admin_menu_helper(message=message)
    except ValueError as error:
        logger.exception("Admin menu opening error: %s", error)
        await message.answer("Ошибка при открытии меню, обратитесь к администратору")
        return

    logger.info("Admin menu opened | by %s", user_id)



