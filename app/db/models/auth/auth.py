from datetime import datetime

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm.attributes import Mapped

from app.db.base_models import WithTimeStamp, Base, int_pk
from app.types.enums import GenderEnum
from app.utils.auth.token import default_token_expiry, default_code_expiry


class User(WithTimeStamp):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    password: Mapped[str]
    gender: Mapped[GenderEnum] = mapped_column(String(10), default="male")
    date_of_birth: Mapped[datetime | None]
    phone: Mapped[str | None] = mapped_column(String(20))
    address: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)

    tokens: Mapped[list["Token"]] = relationship("Token", back_populates="user")
    logs: Mapped[list["Log"]] = relationship("Log", back_populates="user")
    password_resets: Mapped[list["PasswordReset"]] = relationship("PasswordReset", back_populates="user")


class Token(WithTimeStamp):
    __tablename__ = "tokens"

    id: Mapped[int_pk]
    access_token: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expires_in: Mapped[datetime] = mapped_column(default=default_token_expiry)

    user: Mapped["User"] = relationship("User", back_populates="tokens")


class UserLogin(Base):
    __tablename__ = "user_logins"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    ip_address: Mapped[str | None]
    user_agent: Mapped[str | None]
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    code: Mapped[int]
    expires_in: Mapped[datetime] = mapped_column(default=default_code_expiry)

    user: Mapped["User"] = relationship("User" ,back_populates="password_resets")
