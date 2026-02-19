from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from core.models.db_helper import DatabaseHelper
from services import subscription_checker

scheduler = AsyncIOScheduler(timezone="UTC")

def create_scheduler(bot: Bot, db: DatabaseHelper) -> AsyncIOScheduler:
    scheduler.add_job(
        func=subscription_checker,
        trigger=CronTrigger(hour=3, minute=0),
        args=[bot, db],
        id="subscription_checker",
        replace_existing=True,
        misfire_grace_time=3600,
    )

    return scheduler