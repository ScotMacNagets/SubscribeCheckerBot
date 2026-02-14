from datetime import date

from aiogram.types import CallbackQuery, Message

from core.models import User
from core.text import AdminUsersHelpersText
from keyboards.admin_users_keyboard import build_user_actions_keyboard


def _format_user_short(user: User) -> str:
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


def _format_user_detail(user: User) -> str:
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
                text=AdminUsersHelpersText.USER_NOT_FOUND,
                reply_markup=reply_markup,
            )
        else:
            await target.answer(
                text=AdminUsersHelpersText.USER_NOT_FOUND,
                reply_markup=reply_markup,
            )
        if delete:
            await target.message.edit_text(
                text=AdminUsersHelpersText.USER_SUCCESSFULLY_DELETED,
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

    if is_callback and isinstance(target, CallbackQuery):
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
