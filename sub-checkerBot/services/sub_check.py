from datetime import datetime, timezone

from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.config import settings
from core.models import User, Subscription
from core.models.db_helper import DatabaseHelper
from core.text import CheckSubServices
from services.sub_add import logger


async def subscription_checker(bot: Bot, db: DatabaseHelper):
    now = datetime.now(timezone.utc)

    logger.info(f"Subscription checker started at %s", now.isoformat())
    async with db.session_factory() as session:
        try:
            result = await session.execute(
                select(Subscription)
                .where(Subscription.is_active == True)
                .options(selectinload(Subscription.user))
            )

            subs = result.scalars().all()
            logger.info("Checking %d active subscriptions", len(subs))

            for sub in subs:
                user = sub.user
                days_left = (sub.expires_at.date() - now.date()).days

                try:
                    if days_left == 3 and not sub.notified_3_days:
                        await bot.send_message(user.id, CheckSubServices.THREE_DAYS_LEFT)
                        sub.notified_3_days = True
                        logger.info("Notification sent to user %s: 3 days left", user.id)

                    elif days_left == 1 and not sub.notified_1_days:
                        await bot.send_message(user.id, CheckSubServices.ONE_DAY_LEFT)
                        sub.notified_1_day = True
                        logger.info("Notification sent to user %s: 1 day left", user.id)

                    elif days_left == 0 and not sub.notified_expired:
                        await bot.send_message(user.id, CheckSubServices.SUBSCRIBE_EXPIRED)
                        sub.notified_expired = True
                        logger.info("Notification sent to user %s: subscription expired today", user.id)


                    elif days_left < 0:
                        sub.is_active = False
                        logger.info("Deactivating subscription for user %s (expired %d days ago)", user.id, abs(days_left))

                        active_check = await session.execute(
                            select(Subscription).where(
                                Subscription.user_id == user.id,
                                Subscription.is_active == True,
                                Subscription.expires_at > now,
                            )
                        )

                        if not active_check.scalars().first():
                            try:
                                await bot.ban_chat_member(
                                    chat_id=settings.channel.chan_id,
                                    user_id=user.id,
                                )
                                logger.info("User %s banned from channel due to expired subscription", user.id)
                            except Exception as ban_error:
                                error_msg = str(ban_error)
                                if "CHAT_ADMIN_REQUIRED" in error_msg:
                                    logger.error("Bot has no rights to ban user %s", user.id)
                                elif "USER_NOT_PARTICIPANT" in error_msg:
                                    logger.info("User %s already removed from channel", user.id)
                                else:
                                    logger.error("Error banning user %s: %s", user.id, ban_error)
                except Exception as e:
                    logger.error("Error processing subscription check for user %s", user.id, exc_info=e)
            await session.commit()
            logger.info("Subscription checker completed successfully")
        except Exception as db_error:
            logger.error("DB error during subscription check", exc_info=db_error)



