from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, CallbackQuery, InlineQuery
from redis.asyncio import Redis

from core.config import settings
from core.models.db_helper import DatabaseHelper
from core.text import RedisAnswers


class RateLimiterMiddleware(BaseMiddleware):
    def __init__(
            self,
            redis: Redis,
            limit: int = settings.redis.rate_limiter.limit,
            window: int = settings.redis.rate_limiter.window,
            key_prefix: str = settings.redis.rate_limiter.key_prefix,
    ):
        self.redis = redis
        self.limit = limit
        self.window = window
        self.key_prefix = key_prefix

    async def __call__(
            self,
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any],
    ):
        user_id = event.from_user.id
        event_type = type(event).__name__.lower()

        key = f"{self.key_prefix}{event_type}:{user_id}"

        current = await self.redis.incr(key)

        if current == 1:
            await self.redis.expire(key, self.window)

        if current > self.limit:
            if isinstance(event, Message):
                await event.answer(
                    text=RedisAnswers.TOO_MANY_REQUESTS
                )
            elif isinstance(event, CallbackQuery):
                await event.message.answer(
                    text=RedisAnswers.TOO_MANY_REQUESTS,
                )
                await event.answer()
            return

        return await handler(event, data)
        

class DBMiddleware(BaseMiddleware):
    def __init__(self, db: DatabaseHelper):
        self.db = db

    async def __call__(
            self,
            handler: Callable,
            event,
            data: Dict[str, Any],
    ):
        async with self.db.session_factory() as session:
            data["session"] = session
            return await handler(event, data)