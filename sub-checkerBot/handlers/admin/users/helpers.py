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
        status = "🔴 нет подписки"

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
        status = "🟢 активна" if days_left >= 0 else "🔴 истекла"
        lines.append(
            f"Подписка: {status}, до {user.subscription_end.strftime('%d.%m.%Y')} (дней: {days_left})"
        ),
    else:
        lines.append("Подписка: отсутствует")

    return "\n".join(lines)

