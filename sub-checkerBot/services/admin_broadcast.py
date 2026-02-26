from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import User, Subscription


async def get_all_users(session: AsyncSession):
    now = datetime.now()
    stmt = select(User).join(User.subscriptions).where(
        Subscription.expires_at > now,
        Subscription.is_active == True,
    ).distinct()

    result = await session.execute(stmt)
    users = result.scalars().all()
    return users