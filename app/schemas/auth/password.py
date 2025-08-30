from pydantic import BaseModel, Field, field_validator

from app.core.types.constants import rules
from app.core.types.exceptions.password import PasswordValidationError
from app.utils.auth.password import validate_password


class PasswordSchema(BaseModel):
    password: str

    @field_validator('password', mode='after')
    @classmethod
    def password_validator(cls, value: str) -> str:
        if validate_password(value):
            return value
        raise PasswordValidationError(rules.NOT_VALID_PASSWORD, rules.PASSWORD_REQUIREMENTS)


class ChangePasswordSchema(PasswordSchema):
    code: int = Field(ge=100_000, le=999_999)
