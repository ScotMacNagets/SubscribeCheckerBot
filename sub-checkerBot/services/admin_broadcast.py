from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def get_all_users(session: AsyncSession):
    stmt = select(User)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users