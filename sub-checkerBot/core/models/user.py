from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):

    subscription_end: Mapped[date | None] = mapped_column(nullable=True)
    created_at: Mapped[date] = mapped_column(default=date.today())
    username: Mapped[str | None] = mapped_column(nullable=True)