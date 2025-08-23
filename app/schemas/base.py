import i18n
from typing import TypeVar, Generic

from pydantic import BaseModel, field_validator

T = TypeVar('T')


class DBModel(BaseModel):
    model_config = dict(from_attributes=True)


class ResponseSchema(BaseModel, Generic[T]):
    status: bool = True
    message: str
    data: T | None = None

    @field_validator("message", mode="after")
    @classmethod
    def i18n(cls, value: str) -> str:
        return i18n.t(value)
