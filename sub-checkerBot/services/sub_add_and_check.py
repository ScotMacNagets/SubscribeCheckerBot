import asyncio
import datetime
import logging
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User
from core.bot_instance import bot
from core.models.db_helper import DatabaseHelper

logger = logging.getLogger(__name__)


async def add_or_update_subscription(
        session: AsyncSession,
        user_id: int,
        username: str,
        days: int = 3,

):
    #Добавляет или продлевает подписку
    now = datetime.datetime.now().date()

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        user = User(
            id=user_id,
            subscription_end=now + datetime.timedelta(days=days),
            username=username,

        )
        session.add(user)
    else:
        if user.subscription_end is not None and user.subscription_end > now:
            user.subscription_end += timedelta(days=days)
        else:
            user.subscription_end = now + timedelta(days=days)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    new_end_date = user.subscription_end
    return new_end_date


async def add_user_to_channel(user_id: int) -> bool:
    """
    Добавляет пользователя в закрытый канал.
    Возвращает True если операция успешна, False в противном случае.
    """
    try:
        # Используем unban_chat_member для добавления пользователя в канал
        # Это работает даже если пользователь не был забанен
        await bot.unban_chat_member(
            chat_id=settings.channel.chan_id,
            user_id=user_id,
            only_if_banned=False
        )
        logger.info(
            "Пользователь %s успешно добавлен в канал %s",
            user_id,
            settings.channel.chan_id,
        )
        return True
    except Exception as e:
        error_msg = str(e)
        # Обрабатываем различные типы ошибок
        if "CHAT_ADMIN_REQUIRED" in error_msg or "not enough rights" in error_msg.lower():
            logger.error(f"Бот не имеет прав администратора в канале {settings.channel.chan_id}")
        elif "USER_ALREADY_PARTICIPANT" in error_msg or "user is already a participant" in error_msg.lower():
            logger.info(
                "Пользователь %s уже является участником канала",
                user_id,
            )
            return True  # Считаем это успехом
        elif "USER_NOT_MUTED_CONTACT" in error_msg:
            logger.info(
                "Пользователь %s уже разбанен в канале",
                user_id,
            )
            return True  # Считаем это успехом
        else:
            logger.error(
                "Ошибка при добавлении пользователя %s в канал: %s",
                user_id,
                e
            )
        return False


async def create_channel_invite_link(user_id: int | None = None) -> str | None:
    """
    Создаёт инвайт-ссылку на закрытый канал.

    Возвращает ссылку (str) при успехе, иначе None.
    Примечание: чтобы ссылка создавалась, бот должен быть админом канала
    с правом "Invite Users".
    """
    try:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        invite = await bot.create_chat_invite_link(
            chat_id=settings.channel.chan_id,
            name=f"sub_invite_{user_id}" if user_id else "sub_invite",
            expire_date=now_utc + timedelta(days=1),
            member_limit=1,
        )
        logger.info(
            "Создана инвайт-ссылка для канала %s (user_id=%s)",
            settings.channel.chan_id,
            user_id,
        )
        return invite.invite_link
    except Exception as e:
        error_msg = str(e)
        if "CHAT_ADMIN_REQUIRED" in error_msg or "not enough rights" in error_msg.lower():
            logger.error(
                "Бот не имеет прав администратора/инвайта в канале %s",
                settings.channel.chan_id,
            )
        else:
            logger.error(f"Ошибка при создании инвайт-ссылки: {e}")
        return None


async def subscription_checker(db: DatabaseHelper):
    """
    Проверка подписок и уведомления пользователей.
    Запускается в фоновом режиме и проверяет подписки раз в день.
    """
    logger.info("Запуск проверки подписок")

    try:
        today = datetime.datetime.now(datetime.timezone.utc).date()

        async with db.session_factory() as session:
            try:
                result = await session.execute(
                    select(User).where(User.subscription_end != None)
                )
                users = result.scalars().all()

                logger.info(f"Проверка подписок для {len(users)} пользователей")

                for user in users:
                    days_left = (user.subscription_end - today).days

                    try:
                        if days_left == 3:
                            await bot.send_message(
                                user.id,
                                "⏰ Ваша подписка заканчивается через 3 дня! Продлите её, чтобы не потерять доступ."
                            )
                            logger.info(
                                "Отправлено уведомление пользователю %s (осталось 3 дня)",
                                user.id
                            )

                        elif days_left == 1:
                            await bot.send_message(
                                user.id,
                                "⚠️ Ваша подписка заканчивается завтра! Продлите её сейчас."
                            )
                            logger.info(
                                "Отправлено уведомление пользователю %s (осталось 1 день)",
                                user.id
                            )

                        elif days_left == 0:
                            await bot.send_message(
                                user.id,
                                "❌ Ваша подписка истекла сегодня. Доступ к каналу будет закрыт."
                            )
                            logger.info(
                                "Отправлено уведомление пользователю %s (подписка истекла)",
                                user.id
                            )

                        elif days_left < 0:
                            # Удаляем пользователя из канала
                            try:
                                await bot.ban_chat_member(
                                    chat_id=settings.channel.chan_id,
                                    user_id=user.id
                                )
                                logger.info(
                                    "Пользователь %s удален из канала (подписка истекла %s дней назад)",
                                    user.id,
                                    abs(days_left)
                                )
                            except Exception as ban_error:
                                error_msg = str(ban_error)
                                if "CHAT_ADMIN_REQUIRED" in error_msg:
                                    logger.error(
                                        "Бот не имеет прав администратора для бана пользователя %s",
                                        user.id
                                    )
                                elif "USER_NOT_PARTICIPANT" in error_msg:
                                    logger.info(
                                        "Пользователь %s уже не является участником канала",
                                        user.id
                                    )
                                else:
                                    logger.error(
                                        "Ошибка при удалении пользователя %s из канала: %s",
                                        user.id,
                                        ban_error
                                    )

                    except Exception as user_error:
                        error_msg = str(user_error)
                        if "chat not found" in error_msg.lower() or "user not found" in error_msg.lower():
                            logger.warning(
                                "Не удалось отправить сообщение пользователю %s: пользователь не найден",
                                user.id
                            )
                        elif "blocked" in error_msg.lower():
                            logger.warning(
                                "Пользователь %s заблокировал бота",
                                user.id
                            )
                        else:
                            logger.error(
                                "Ошибка при обработке пользователя %s: %s",
                                user.id,
                                user_error
                            )

            except Exception as db_error:
                logger.error(
                    "Ошибка при выборке пользователей из БД: %s",
                    db_error
                )

    except Exception as e:
        logger.error(
            "Критическая ошибка в subscription_checker: %s",
            e
        )