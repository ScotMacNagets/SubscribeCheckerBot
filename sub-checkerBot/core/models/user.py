import typing
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if typing.TYPE_CHECKING:
    from .subscriptions import Subscription


class User(Base):

    subscription_end: Mapped[date | None] = mapped_column(nullable=True)
    created_at: Mapped[date] = mapped_column(default=date.today())
    username: Mapped[str | None] = mapped_column(nullable=True)
    subscriptions: Mapped["Subscription"] = relationship("Subscription", back_populates="user")