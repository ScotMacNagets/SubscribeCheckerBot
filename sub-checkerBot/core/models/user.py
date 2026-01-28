from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from .base import Base

class User(Base):

   user_id: Mapped[int] = mapped_column(primary_key=True)
   subscription_end: Mapped[datetime | None]