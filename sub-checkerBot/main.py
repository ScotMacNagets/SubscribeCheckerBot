import asyncio
import logging

from aiogram import Dispatcher

from core.bot_instance import bot
from core.logging_config import configure_logging
from core.models.db_helper import db_helper
from core.scheduler import create_scheduler
from middleware import DBMiddleware
from handlers import start_router, buy_subscription_router, check_sub_router, admin_router


logger = logging.getLogger(__name__)
scheduler = create_scheduler(bot, db_helper)

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(buy_subscription_router)
dp.include_router(check_sub_router)
dp.include_router(admin_router)

@dp.startup()
async def on_startup():
    configure_logging(level=logging.INFO)
    logger.info("Bot starting...")
    await db_helper.create_tables()
    logger.info("DB table checked/created")
    
    dp.update.middleware(DBMiddleware(db=db_helper))
    logger.info("Middleware connected")
    
    # Запускаем фоновую задачу проверки подписок
    scheduler.start()
    logger.info("SubChecker background task started")

@dp.shutdown()
async def on_shutdown():
    logger.info("Bot shutdown...")

    await db_helper.dispose()
    logger.info("DB connection closed")

    scheduler.shutdown()
    logger.info("SubChecker background task shutdown")


async def main():
    try:
        logger.info("Bot started and ready to work")
        await dp.start_polling(
            bot,
            skip_updates=True,
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Got stop signal. Shutting down...")
    except Exception as e:
        logger.critical(
            "Critical error while bot working: %s",
            e,
            exc_info=True
        )
    finally:
        await bot.session.close()
        logger.info("Bot session closed")

if __name__ == "__main__":
    asyncio.run(main())
