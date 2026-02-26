import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.config import settings
from core.constants import CommandText
from core.text import AdminMenu
from handlers.admin.helpers import open_admin_menu_helper

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command(CommandText.ADMIN_MENU))
async def open_admin_menu(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    if username != settings.admin.support or username != settings.admin.super_user:
        logger.warning("User with id: %s tried to access admin menu", user_id)
        await message.answer(
            text=AdminMenu.ACCESS_RESTRICTED
        )
        return

    try:
        await open_admin_menu_helper(message=message)
    except ValueError as error:
        logger.exception("Admin menu opening error: %s", error)
        await message.answer(
            text=AdminMenu.OPEN_ADMIN_MENU_ERROR
        )
        return

    logger.info("Admin menu opened | by %s", user_id)



