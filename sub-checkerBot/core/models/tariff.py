from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Tariff(Base):

    title: Mapped[str]
    days: Mapped[int]
    price: Mapped[int]
    payload: Mapped[str] = mapped_column(unique=True)
    hot: Mapped[bool | None]
    emoji: Mapped[str | None]
    is_active: Mapped[bool | None] = mapped_column(default=True)
    sort_order: Mapped[int] = mapped_column(default=0)
