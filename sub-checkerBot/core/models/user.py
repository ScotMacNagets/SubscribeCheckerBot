from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from .base import Base

class User(Base):

   subscription_end: Mapped[date | None]