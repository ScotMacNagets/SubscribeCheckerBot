import asyncio
import datetime
from _datetime import timedelta

from poetry.console.commands import self
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User
from core.bot_instance import bot
from core.models.db_helper import DatabaseHelper


async def add_or_update_subscription(session: AsyncSession, user_id: int, days: int = 3):
    #Добавляет или продлевает подписку
    now = datetime.datetime.now().date()

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        user = User(
            id=user_id,
            subscription_end=now + datetime.timedelta(days=days)
        )
        session.add(user)
    else:
        if user.subscription_end > now:
            user.subscription_end += timedelta(days=days)
        else:
            user.subscription_end = now + timedelta(days=days)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    new_end_date = user.subscription_end
    return new_end_date


async def subscription_checker(db: DatabaseHelper):
    #Проверка подписки и уведомления
    while True:
        today = datetime.datetime.now(datetime.timezone.utc).date()


        async with db.session_factory() as session:
            try:
                result = await session.execute(select(User).where(User.subscription_end != None))
                users = result.scalars().all()

                for user in users:
                    days_left = (user.subscription_end - today).days

                    try:
                        if days_left == 3:
                            await bot.send_message(user.id, "Ваша подписка заканчивается через 3 дня!")
                        elif days_left < 0:
                            await bot.ban_chat_member(settings.channel.chan_id, user.id)
                    except Exception as e:
                        print(f"Ошибка при обработке пользователя {user.id}: {e}")
            except Exception as e:
                print(f"Ошибка при выборке пользователей: {e}")
        await asyncio.sleep(timedelta(days=1).total_seconds())