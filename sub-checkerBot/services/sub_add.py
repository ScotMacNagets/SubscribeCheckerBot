from datetime import datetime, timezone
import logging
from datetime import timedelta

from sqlalchemy import select, and_, update, values
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User, Subscription
from core.bot_instance import bot

logger = logging.getLogger(__name__)


async def add_or_update_subscription(
        session: AsyncSession,
        user_id: int,
        username: str,
        tariff_id: int,
        days: int = 3,

):
    #Добавляет или продлевает подписку
    today = datetime.now(timezone.utc)

    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        user = User(
            id=user_id,
            username=username,
        )
        session.add(user)
        await session.flush()

    stmt = select(Subscription).where(
        and_(
            Subscription.user_id == user.id,
            Subscription.is_active == True,
            Subscription.expires_at > today,
        )
    )
    result = await session.execute(stmt)
    subscription = result.scalars().first()

    if subscription:
        current_expire = subscription.expires_at.astimezone(timezone.utc)
        new_expire = current_expire + timedelta(days=days)
        subscription.expires_at = new_expire.replace(hour=0, minute=0, second=0, microsecond=0)

        subscription.notified_3_days = False
        subscription.notified_1_day = False
        subscription.notified_expired = False
    else:
        await session.execute(
            update(Subscription)
            .where(Subscription.user_id == user.id)
            .values(is_active=False)
        )

        subscription = Subscription(
            user_id=user.id,
            tariff_id=tariff_id,
            started_at=today,
            expires_at=(today + timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0),
            is_active=True,
        )
        session.add(subscription)

    await session.commit()
    await session.refresh(subscription)

    return subscription.expires_at


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
        now_utc = datetime.now(timezone.utc)
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


