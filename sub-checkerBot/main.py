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
    logger.info("Запуск бота...")
    await db_helper.create_tables()
    logger.info("Таблицы БД созданы/проверены")
    
    dp.update.middleware(DBMiddleware(db=db_helper))
    logger.info("Middleware подключен")
    
    # Запускаем фоновую задачу проверки подписок
    scheduler.start()
    logger.info("Фоновая задача проверки подписок запущена")

@dp.shutdown()
async def on_shutdown():
    logger.info("Остановка бота...")

    await db_helper.dispose()
    logger.info("Соединения с БД закрыты")

    scheduler.shutdown()
    logger.info("Фоновая задача проверки подписок остановлена")


async def main():
    try:
        logger.info("Бот запущен и готов к работе")
        await dp.start_polling(
            bot,
            skip_updates=True,
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Получен сигнал остановки. Завершение работы...")
    except Exception as e:
        logger.critical(
            "Критическая ошибка при работе бота: %s",
            e,
            exc_info=True
        )
    finally:
        await bot.session.close()
        logger.info("Сессия бота закрыта")

if __name__ == "__main__":
    asyncio.run(main())
