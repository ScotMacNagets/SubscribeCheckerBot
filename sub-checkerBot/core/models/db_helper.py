from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import settings
from core.models.base import Base


class DatabaseHelper:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )


    async def dispose(self):
        await self.engine.dispose()


    async def session_setter(self):
        async with self.session_factory() as session:
            yield session

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db_helper = DatabaseHelper(
    url=str(settings.db.db_url),
)
