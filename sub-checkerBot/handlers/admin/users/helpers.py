from datetime import date

from core.models import User
from core.text import AdminUsersHelpersText


async def _get_user_sub(
        user: User,
        session: AsyncSession,
) -> Subscription:
    now = datetime.now()
    stmt = select(Subscription).where(
        and_(
            Subscription.user_id == user.id,
            Subscription.expires_at > now,
            Subscription.is_active == True,
        )
    )
    result = await session.execute(stmt)

    subscription = result.scalars().one_or_none()
    return subscription

async def format_user_short(session: AsyncSession, user: User) -> str:
    status: str
    subscription: Subscription = await _get_user_sub(user, session)
    if subscription:
        days_left = (subscription.expires_at - datetime.now()).days
        status = (
            AdminUsersHelpersText.FORMAT_SHORT.format(
                date=subscription.expires_at.strftime('%d.%m.%Y'),
                days_left=abs(days_left),
            ),
        )
    else:
        status = AdminUsersHelpersText.SHORT_NO_SUB

    username = f"@{user.username}" if user.username else "-"
    return f"ID: {user.id} | {username} | {status}"


async def format_user_detail(session: AsyncSession, user: User) -> str:
    subscription: Subscription = await _get_user_sub(user, session)

    lines = [
        AdminUsersHelpersText.FORMAT_DETAIL.format(
            id=user.id,
            username=user.username,
            date=user.created_at.strftime('%d.%m.%Y')
        ),
    ]

    if subscription:
        days_left = (subscription.expires_at - datetime.now()).days

        status = (
            AdminUsersHelpersText.STATUS_ACTIVE
            if days_left >= 0
            else AdminUsersHelpersText.STATUS_EXPIRED
        )

        lines.append(
            AdminUsersHelpersText.SUB_DESC.format(
                status=status,
                date=subscription.expires_at.strftime('%d.%m.%Y'),
                days_left=abs(days_left),
            )
        ),
    else:
        lines.append(AdminUsersHelpersText.USER_GOT_NO_SUB)

    return "\n".join(lines)

