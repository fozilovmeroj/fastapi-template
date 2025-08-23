from pydantic import BaseModel, Field, field_validator

from app.utils.auth.password import validate_password


class ChangePasswordSchema(BaseModel):
    code: int = Field(max_digits=6)
    password: str

    @field_validator('password', mode='after')
    @classmethod
    def password_validator(cls, value: str) -> str:
        if validate_password(value):
            return value
        raise ValueError("Not a valid password")
