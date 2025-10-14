from datetime import datetime

from pydantic import EmailStr

from app.schemas.auth.password import PasswordSchema
from app.schemas.base import DBModel
from app.schemas.users.base import UserSchema, UserCreate
from app.core.types.enums.gender import GenderEnum


class SignInSchema(DBModel, PasswordSchema):
    login: str


class SignUpSchema(UserCreate):
    pass


class SignInResponse(DBModel):
    token: str
    user: UserSchema | None
