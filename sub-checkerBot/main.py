import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from core.config import settings

bot = Bot(token=settings.run.token)
dp = Dispatcher()

@dp.message()
async def echo_message(message: types.Message):
    await message.answer(text=message.text)


async def main():
    try:
        logging.basicConfig(level=logging.INFO)
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
