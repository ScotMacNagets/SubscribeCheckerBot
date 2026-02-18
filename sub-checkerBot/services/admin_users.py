import logging
from datetime import date, timedelta
from typing import Optional

from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.text import AdminUsersHelpersText
from handlers.admin.users.helpers import format_user_short, format_user_detail
from keyboards.admin_users_keyboard import build_user_actions_keyboard

logger = logging.getLogger(__name__)


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    """
    Возвращает пользователя по username или None, если не найден.
    """
    try:
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user
    except ValueError as error:
        logger.error(
            "User with %s not found: %s",
            username,
            error,
        )
        return None


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
        text = format_user_short(user)
    else:
        text = format_user_detail(user)

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
