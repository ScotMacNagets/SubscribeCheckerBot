import asyncio
import logging

from aiogram import Bot, Dispatcher
from core.config import settings
from core.models.db_helper import db_helper
from middleware import DBMiddleware

bot = Bot(token=settings.run.token)
dp = Dispatcher()

@dp.startup()
async def on_startup():
    await db_helper.create_tables()
    dp.update.middleware(DBMiddleware(db=db_helper))

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
