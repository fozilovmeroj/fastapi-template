from datetime import datetime

from pydantic import EmailStr

from app.schemas.auth.password import PasswordSchema
from app.schemas.base import DBModel
from app.schemas.users.base import UserSchema
from app.types.enums.gender import GenderEnum


class SignInSchema(DBModel, PasswordSchema):
    login: str


class SignUpSchema(DBModel, PasswordSchema):
    name: str
    email: EmailStr
    gender: GenderEnum
    date_of_birth: datetime | None
    phone: str
    address: str | None


class SignInResponse(DBModel):
    token: str
    user: UserSchema | None
