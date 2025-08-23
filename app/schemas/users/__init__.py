from datetime import datetime

from pydantic import EmailStr

from app.schemas.base import DBModel
from app.types.enums import GenderEnum


class UserSchema(DBModel):
    id: int
    email: EmailStr
    name: str
    gender: GenderEnum
    date_of_birth: datetime | None
    phone: str
    address: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None