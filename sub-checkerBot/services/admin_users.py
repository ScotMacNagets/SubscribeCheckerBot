from datetime import date, timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    """
    Возвращает пользователя по username или None, если не найден.
    """
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()


async def extend_subscription(
    session: AsyncSession,
    username: str,
    days: int,
) -> Optional[User]:
    """
    Продлевает подписку на указанное количество дней.
    Если пользователя нет — возвращает None.
    """
    user = await get_user_by_username(session=session, username=username)
    if not user:
        return None

    today = date.today()
    if user.subscription_end is not None and user.subscription_end >= today:
        base_date = user.subscription_end
    else:
        base_date = today

    user.subscription_end = base_date + timedelta(days=days)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def set_subscription_end(
    session: AsyncSession,
    username: str,
    new_end: date | None = None,
    cancel: bool = False,
) -> Optional[User]:
    """
    Устанавливает дату окончания подписки (может быть None).
    """
    user = await get_user_by_username(session=session, username=username)
    if not user:
        return None

    user.subscription_end = new_end
    if cancel:
        user.subscription_end = None
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(
    session: AsyncSession,
    username: str,
) -> bool:
    """
    Удаляет пользователя из БД.
    Возвращает True, если пользователь был найден и удалён.
    """
    user = await get_user_by_username(session=session, username=username)
    if not user:
        return False

    await session.delete(user)
    await session.commit()
    return True

