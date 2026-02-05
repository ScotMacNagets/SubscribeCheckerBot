from datetime import date, datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    """
    Модель пользователя бота.

    id – Telegram user_id (унаследован от Base).
    subscription_end – дата окончания подписки (None, если подписки нет).
    created_at – дата/время первой регистрации в системе.
    username – username пользователя (если есть), для удобства админ-поиска.
    """

    subscription_end: Mapped[date | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now().date())
    username: Mapped[str | None] = mapped_column(nullable=True)