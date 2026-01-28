from typing import Callable, Dict, Any

from aiogram import BaseMiddleware

from core.models.db_helper import DatabaseHelper


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