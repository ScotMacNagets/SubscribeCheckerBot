import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.bot_instance import bot
from core.text import StartHandler
from keyboards.start_keyboard import build_start_keyboard


router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start(message: Message):
    logger.info(
        "User started bot| by username %s | id %s",
        message.from_user.username,
        message.from_user.id,
    )
    await message.answer(
        text=StartHandler.START,
        reply_markup=build_start_keyboard(),
    )

# @router.message(Command("подписка"))
# async def subscribe_commands(message: Message, session: AsyncSession):
#     new_end_date = await add_or_update_subscription(
#         session=session,
#         user_id=message.from_user.id
#     )
#     try:
#         await bot.unban_chat_member(int(settings.channel.chan_id), message.from_user.id)
#         await message.answer(f"Подписка активирована до {new_end_date}")
#     except Exception as e:
#         await message.answer(f"Ошибка при добавлении в канал")
#         print(e)
