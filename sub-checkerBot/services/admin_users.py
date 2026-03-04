import logging
from datetime import timedelta, datetime
from typing import Optional

from aiogram.types import CallbackQuery, Message
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Subscription
from core.text import AdminUsersHelpersText
from handlers.admin.users.helpers import format_user_short, format_user_detail
from keyboards.admin_users_keyboard import build_user_actions_keyboard

logger = logging.getLogger(__name__)


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
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

async def _get_user_sub(
        session: AsyncSession,
        user: User,
) -> Optional[Subscription]:
    now = datetime.now()
    try:
        stmt = select(Subscription).where(
            and_(
                Subscription.user_id == user.id,
                Subscription.is_active == True,
                Subscription.expires_at > now,
            )
        )
        result = await session.execute(stmt)
        subscription = result.scalars().one_or_none()
        return subscription
    except ValueError as error:
        logger.error(
            "Cannot load subscription for user with id %s: %s", user.id, error
        )


async def extend_subscription(
    session: AsyncSession,
    username: str,
    days: int,
) -> Optional[User]:
    user = await get_user_by_username(
        session=session,
        username=username,
    )
    active_subscription = await _get_user_sub(
        session=session,
        user=user,
    )


    if not active_subscription:
        return None

    active_subscription.expires_at = active_subscription.expires_at + timedelta(days=days)

    session.add(active_subscription)
    await session.commit()
    await session.refresh(active_subscription)
    return user





async def set_subscription_end(
    session: AsyncSession,
    username: str,
    new_end: datetime | None = None,
    cancel: bool = False,
) -> Optional[User]:
    user = await get_user_by_username(
        session=session,
        username=username,
    )
    active_subscription = await _get_user_sub(
        session=session,
        user=user,
    )

    if not active_subscription:
        return None

    if cancel:
        active_subscription.is_active = False
    else:
        active_subscription.expires_at = new_end

    session.add(active_subscription)
    await session.commit()
    await session.refresh(active_subscription)

    return user


# async def delete_user(
#     session: AsyncSession,
#     username: str,
# ) -> bool:
#     """
#     Удаляет пользователя из БД.
#     Возвращает True, если пользователь был найден и удалён.
#     """
#     user = await get_user_by_username(session=session, username=username)
#     if not user:
#         return False
#
#     await session.delete(user)
#     await session.commit()
#     return True


async def render_user(
        username: str,
        target: CallbackQuery | Message,
        session: AsyncSession,
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
        text = await format_user_short(
            user=user,
            session=session,
        )
    else:
        text = await format_user_detail(
            user=user,
            session=session,
        )

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
