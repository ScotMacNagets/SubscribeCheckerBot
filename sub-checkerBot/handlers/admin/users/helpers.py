from datetime import date

from aiogram.types import CallbackQuery

from core.models import User


def _format_user_short(user: User) -> str:
    status: str
    if user.subscription_end:
        days_left = (user.subscription_end - date.today()).days
        status = (
            f"активна, до {user.subscription_end.strftime('%d.%m.%Y')} ({days_left} дн.)"
            if days_left >= 0
            else f"истекла {user.subscription_end.strftime('%d.%m.%Y')} ({abs(days_left)} дн. назад)"
        )
    else:
        status = "нет подписки"

    username = f"@{user.username}" if user.username else "-"
    return f"ID: {user.id} | {username} | {status}"


def _format_user_detail(user: User) -> str:
    lines = [
        f"👤 <b>Пользователь</b>",
        f"ID: <code>{user.id}</code>",
        f"Username: @{user.username}" if user.username else "Username: -",
        f"Создан: {user.created_at.strftime('%d.%m.%Y %H:%M:%S')}",
    ]

    if user.subscription_end:
        days_left = (user.subscription_end - date.today()).days
        status = "активна" if days_left >= 0 else "истекла"
        lines.append(
            f"Подписка: {status}, до {user.subscription_end.strftime('%d.%m.%Y')} (дней: {days_left})"
        )
    else:
        lines.append("Подписка: отсутствует")

    return "\n".join(lines)

def get_user_and_days(query: CallbackQuery):
    _, useful = query.data.split("_")
    days, username = useful.split(":")
    return days, username
