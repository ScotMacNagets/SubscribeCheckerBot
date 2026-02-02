import asyncio
import datetime
import logging
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User
from core.bot_instance import bot
from core.models.db_helper import DatabaseHelper

logger = logging.getLogger(__name__)


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


async def add_user_to_channel(user_id: int) -> bool:
    """
    Добавляет пользователя в закрытый канал.
    Возвращает True если операция успешна, False в противном случае.
    """
    try:
        # Используем unban_chat_member для добавления пользователя в канал
        # Это работает даже если пользователь не был забанен
        await bot.unban_chat_member(
            chat_id=settings.channel.chan_id,
            user_id=user_id,
            only_if_banned=False
        )
        logger.info(
            "Пользователь %s успешно добавлен в канал %s",
            user_id,
            settings.channel.chan_id,
        )
        return True
    except Exception as e:
        error_msg = str(e)
        # Обрабатываем различные типы ошибок
        if "CHAT_ADMIN_REQUIRED" in error_msg or "not enough rights" in error_msg.lower():
            logger.error(f"Бот не имеет прав администратора в канале {settings.channel.chan_id}")
        elif "USER_ALREADY_PARTICIPANT" in error_msg or "user is already a participant" in error_msg.lower():
            logger.info(
                "Пользователь %s уже является участником канала",
                user_id,
            )
            return True  # Считаем это успехом
        elif "USER_NOT_MUTED_CONTACT" in error_msg:
            logger.info(
                "Пользователь %s уже разбанен в канале",
                user_id,
            )
            return True  # Считаем это успехом
        else:
            logger.error(
                "Ошибка при добавлении пользователя %s в канал: %s",
                user_id,
                e
            )
        return False


async def create_channel_invite_link(user_id: int | None = None) -> str | None:
    """
    Создаёт инвайт-ссылку на закрытый канал.

    Возвращает ссылку (str) при успехе, иначе None.
    Примечание: чтобы ссылка создавалась, бот должен быть админом канала
    с правом "Invite Users".
    """
    try:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        invite = await bot.create_chat_invite_link(
            chat_id=settings.channel.chan_id,
            name=f"sub_invite_{user_id}" if user_id else "sub_invite",
            expire_date=now_utc + timedelta(days=1),
            member_limit=1,
        )
        logger.info(
            "Создана инвайт-ссылка для канала %s (user_id=%s)",
            settings.channel.chan_id,
            user_id,
        )
        return invite.invite_link
    except Exception as e:
        error_msg = str(e)
        if "CHAT_ADMIN_REQUIRED" in error_msg or "not enough rights" in error_msg.lower():
            logger.error(
                "Бот не имеет прав администратора/инвайта в канале %s",
                settings.channel.chan_id,
            )
        else:
            logger.error(f"Ошибка при создании инвайт-ссылки: {e}")
        return None


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