from datetime import date

from aiogram.types import CallbackQuery, Message

from core.models import User
from keyboards.admin_users_keyboard import build_user_actions_keyboard


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

async def render_user(
        username: str,
        target: CallbackQuery | Message,
        user: User = None,
        is_callback: bool = False,
        delete: bool = False,
        short: bool = False,
        reply_markup=None,
):
    if not user:
        if is_callback:
            await target.message.edit_text(
                text="Пользователь не найден",
                reply_markup=reply_markup,
            )
        else:
            await target.answer(
                text="Пользователь не найден",
                reply_markup=reply_markup,
            )
        if delete:
            await target.message.edit_text(
                text="Пользователь успешно удален",
                reply_markup=reply_markup,
            )
        return

    if short:
        text = _format_user_short(user)
    else:
        text = _format_user_detail(user)

    if isinstance(target, CallbackQuery):
        method = target.message.edit_text
    else:
        method = target.answer

    if is_callback and target == CallbackQuery:
        await target.answer()

    await method(
        text=text,
        reply_markup=build_user_actions_keyboard(username=username),
        parse_mode="HTML",
    )

def get_user_and_days(query: CallbackQuery):
    _, useful = query.data.split("_")
    days, username = useful.split(":")
    return days, username
