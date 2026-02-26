import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Subscription

logger = logging.getLogger(__name__)


async def self_check(user_id, session: AsyncSession):
    try:
        result = await session.execute(
            select(Subscription.expires_at)
            .where(
                Subscription.user_id == user_id,
                Subscription.is_active == True,
            )
        )
        sub_end = result.scalars().one_or_none()
        return sub_end
    except Exception as db_error:
        logger.error(
            "Ошибка при выборке пользователя из бд: %s",
            db_error,
        )
        return None

