from aiogram import Bot

from core.config import settings

bot = Bot(token=str(settings.run.token))