from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.bot_instance import bot
from services.sub_add_and_check import add_or_update_subscription

router = Router()

@router.message(Command("подписка"))
async def subscribe_commands(message: types.Message, session: AsyncSession):
    new_end_date = await add_or_update_subscription(
        session=session,
        user_id=message.from_user.id
    )
    try:
        await bot.unban_chat_member(int(settings.channel.chan_id), message.from_user.id)
        await message.answer(f"Подписка активирована до {new_end_date}")
    except Exception as e:
        await message.answer(f"Ошибка при добавлении в канал")
        print(e)
