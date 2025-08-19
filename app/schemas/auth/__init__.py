from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.users import UserSchema
from app.types.enums import GenderEnum


class SignInSchema(BaseModel):
    login: str
    password: str


class SignUpSchema(BaseModel):
    name: str
    password: str = Field(..., min_length=6)
    email: EmailStr
    gender: GenderEnum
    date_of_birth: datetime | None
    phone: str
    address: str | None

class SignInResponse(BaseModel):
    token: str
    user: UserSchema | None