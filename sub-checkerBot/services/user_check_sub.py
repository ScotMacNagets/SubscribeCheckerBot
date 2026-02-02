import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User

logger = logging.getLogger(__name__)


async def self_check(user_id, session: AsyncSession):
    try:
        result = await session.execute(select(User.subscription_end).where(User.id == user_id))
        sub_end = result.scalars().one_or_none()
        return sub_end
    except Exception as db_error:
        logger.error(
            "Ошибка при выборке пользователя из бд: %s",
            db_error,
        )
        return None

