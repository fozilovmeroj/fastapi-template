from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.orm.attributes import Mapped


class Base(DeclarativeBase):
    pass


class WithTimeStamp(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())

class SoftDelete(Base):
    __abstract__ = True
    deleted_at: Mapped[datetime | None] = mapped_column()

int_pk = Annotated[int, mapped_column(primary_key=True)]