from datetime import datetime

from pydantic import EmailStr

from app.schemas.auth.password import PasswordSchema
from app.schemas.base import DBModel
from app.core.types.enums.gender import GenderEnum


class UserSchema(DBModel):
    id: int
    email: EmailStr
    name: str
    gender: GenderEnum
    date_of_birth: datetime | None
    phone: str | None
    address: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None


class UserCreate(DBModel, PasswordSchema):
    name: str
    email: EmailStr
    gender: GenderEnum
    date_of_birth: datetime | None
    phone: str
    address: str | None


class UserUpdate(DBModel, PasswordSchema):
    name: str | None = None
    email: EmailStr | None = None
    gender: GenderEnum | None = None
    date_of_birth: datetime | None
    phone: str | None = None
    address: str | None


class UserWithPasswordSchema(UserSchema):
    password: str
