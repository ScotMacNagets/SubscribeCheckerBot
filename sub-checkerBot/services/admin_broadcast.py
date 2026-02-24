from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def get_all_users(session: AsyncSession):
    today = date.today()
    stmt = select(User).where(User.subscription_end >= today)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users