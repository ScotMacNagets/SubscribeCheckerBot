import asyncio
import logging

from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot_instance import bot
from core.models.db_helper import db_helper
from middleware import DBMiddleware
from handlers import subscription_router
from services import subscription_checker

dp = Dispatcher()

dp.include_router(subscription_router)

@dp.startup()
async def on_startup():
    await db_helper.create_tables()
    dp.update.middleware(DBMiddleware(db=db_helper))
    # asyncio.create_task(subscription_checker(db=db_helper))

@dp.shutdown()
async def on_shutdown():
    await db_helper.dispose()

async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        await dp.start_polling(
            bot,
            skip_updates=True,
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("Shutting down")
    except Exception as error:
        print(f"The bot has been stopped due to error {error}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
