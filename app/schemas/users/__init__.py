from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.types.enums import GenderEnum


class UserSchema(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)
