import datetime

from aiogram import Bot
from sqlalchemy import select

from core.config import settings
from core.models import User
from core.models.db_helper import DatabaseHelper
from core.text import CheckSubServices
from services.sub_add import logger


async def subscription_checker(bot: Bot, db: DatabaseHelper):
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
                    select(User).where(
                        User.subscription_end.between(
                            today - datetime.timedelta(days=1),
                            today + datetime.timedelta(days=3)
                        ),
                    )
                )
                users = result.scalars().all()

                logger.info(f"Проверка подписок для {len(users)} пользователей")

                for user in users:
                    days_left = (user.subscription_end - today).days

                    try:
                        if days_left == 3:
                            await bot.send_message(
                                user.id,
                                CheckSubServices.THREE_DAYS_LEFT
                            )
                            logger.info(
                                "Отправлено уведомление пользователю %s (осталось 3 дня)",
                                user.id
                            )

                        elif days_left == 1:
                            await bot.send_message(
                                user.id,
                                CheckSubServices.ONE_DAY_LEFT
                            )
                            logger.info(
                                "Отправлено уведомление пользователю %s (осталось 1 день)",
                                user.id
                            )

                        elif days_left == 0:
                            await bot.send_message(
                                user.id,
                                CheckSubServices.SUBSCRIBE_EXPIRED
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

    except Exception as error:
        logger.error(
            "Критическая ошибка в subscription_checker: %s",
            error
        )
