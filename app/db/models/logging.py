from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy_utils import generic_relationship

from app.db.base_models import WithTimeStamp, int_pk
from app.core.types.enums.log_level import LogLevelEnum


class Log(WithTimeStamp):
    __tablename__ = "logs"

    id: Mapped[int_pk]
    level: Mapped[LogLevelEnum] = mapped_column(String(50), default=LogLevelEnum.INFO)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str]
    object_type: Mapped[str]
    object_id: Mapped[int]
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None]
    message: Mapped[str | None] = mapped_column(Text)

    user: Mapped["User"] = relationship("User", back_populates="logs")
    object = generic_relationship("object_type", "object_id")
