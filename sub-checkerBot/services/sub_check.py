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
    logger.info("Subscription checker started")

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

                logger.info(
                    "Subscription checking for %s users",
                    len(users)
                )

                for user in users:
                    days_left = (user.subscription_end - today).days

                    try:
                        if days_left == 3:
                            await bot.send_message(
                                user.id,
                                CheckSubServices.THREE_DAYS_LEFT
                            )
                            logger.info(
                                "Notification sent to %s user (3 days left)",
                                user.id
                            )

                        elif days_left == 1:
                            await bot.send_message(
                                user.id,
                                CheckSubServices.ONE_DAY_LEFT
                            )
                            logger.info(
                                "Notification sent to %s user (1 days left)",
                                user.id
                            )

                        elif days_left == 0:
                            await bot.send_message(
                                user.id,
                                CheckSubServices.SUBSCRIBE_EXPIRED
                            )
                            logger.info(
                                "Notification sent to %s user (subscribe expired)",
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
                                    "User %s has been removed from channel (subscribe expired %s days ago)",
                                    user.id,
                                    abs(days_left)
                                )
                            except Exception as ban_error:
                                error_msg = str(ban_error)
                                if "CHAT_ADMIN_REQUIRED" in error_msg:
                                    logger.error(
                                        "Bot got no sufficient rights to user %s ban",
                                        user.id
                                    )
                                elif "USER_NOT_PARTICIPANT" in error_msg:
                                    logger.info(
                                        "User %s is already removed",
                                        user.id
                                    )
                                else:
                                    logger.error(
                                        "User %s removed error: %s",
                                        user.id,
                                        ban_error
                                    )

                    except Exception as user_error:
                        error_msg = str(user_error)
                        if "chat not found" in error_msg.lower() or "user not found" in error_msg.lower():
                            logger.warning(
                                "Cannot sent message to %s user: user not found",
                                user.id
                            )
                        elif "blocked" in error_msg.lower():
                            logger.warning(
                                "Bot has been blocked by user: %s",
                                user.id
                            )
                        else:
                            logger.error(
                                "Processing error: %s",
                                user.id,
                                user_error
                            )

            except Exception as db_error:
                logger.error(
                    "Database error: %s",
                    db_error
                )

    except Exception as error:
        logger.error(
            "Critical error: %s",
            error
        )
