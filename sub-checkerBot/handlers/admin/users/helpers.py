from datetime import date

from core.models import User
from core.text import AdminUsersHelpersText


def format_user_short(user: User) -> str:
    status: str
    if user.subscription_end:
        days_left = (user.subscription_end - date.today()).days
        status = (
            AdminUsersHelpersText.FORMAT_SHORT.format(
                date=user.subscription_end.strftime('%d.%m.%Y'),
                days_left=abs(days_left),
            ),
        )
    else:
        status = AdminUsersHelpersText.SHORT_NO_SUB

    username = f"@{user.username}" if user.username else "-"
    return f"ID: {user.id} | {username} | {status}"


def format_user_detail(user: User) -> str:
    lines = [
        AdminUsersHelpersText.FORMAT_DETAIL.format(
            id=user.id,
            username=user.username,
            date=user.created_at.strftime('%d.%m.%Y')
        ),
    ]

    if user.subscription_end:
        days_left = (user.subscription_end - date.today()).days

        status = (
            AdminUsersHelpersText.STATUS_ACTIVE
            if days_left >= 0
            else AdminUsersHelpersText.STATUS_EXPIRED
        )

        lines.append(
            AdminUsersHelpersText.SUB_DESC.format(
                status=status,
                date=user.subscription_end.strftime('%d.%m.%Y'),
                days_left=abs(days_left),
            )
        ),
    else:
        lines.append(AdminUsersHelpersText.USER_GOT_NO_SUB)

    return "\n".join(lines)

