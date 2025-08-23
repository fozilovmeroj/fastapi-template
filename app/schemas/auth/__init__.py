from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.base import DBModel
from app.schemas.users import UserSchema
from app.types.enums import GenderEnum


class SignInSchema(DBModel):
    login: str
    password: str


class SignUpSchema(DBModel):
    name: str
    password: str = Field(..., min_length=6)
    email: EmailStr
    gender: GenderEnum
    date_of_birth: datetime | None
    phone: str
    address: str | None

class SignInResponse(DBModel):
    token: str
    user: UserSchema | None