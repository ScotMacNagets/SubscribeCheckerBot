from datetime import date, datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):

    subscription_end: Mapped[date | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    username: Mapped[str | None] = mapped_column(nullable=True)