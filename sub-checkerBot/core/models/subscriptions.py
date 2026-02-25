import typing
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if typing.TYPE_CHECKING:
    from . import Tariff
    from . import User



class Subscription(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    tariff_id: Mapped[int] = mapped_column(ForeignKey("tariffs.id"))

    started_at: Mapped[datetime]
    expires_at: Mapped[datetime]

    is_active: Mapped[bool] = mapped_column(default=True)

    notified_3_days: Mapped[bool] = mapped_column(default=False)
    notified_1_day: Mapped[bool] = mapped_column(default=False)
    notified_expired: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship("User", back_populates="subscriptions")
    tariff: Mapped["Tariff"] = relationship("Tariff")