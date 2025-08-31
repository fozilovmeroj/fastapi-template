from typing import Any

from fastapi import Request

from app.core.types.enums.log_level import LogLevelEnum
from app.logic.repositories.log_repository import LogRepository


class LogService:
    @classmethod
    async def create(cls, user_id: int, object_model: Any, action: str, request: Request):
        await cls.log(LogLevelEnum.CREATE, user_id=user_id, object_model=object_model, action=action, request=request)

    @classmethod
    async def update(cls, user_id: int, object_model: Any, action: str, request: Request):
        await cls.log(LogLevelEnum.UPDATE, user_id=user_id, object_model=object_model, action=action, request=request)

    @classmethod
    async def delete(cls, user_id: int, object_model: Any, action: str, request: Request):
        await cls.log(LogLevelEnum.DELETE, user_id=user_id, object_model=object_model, action=action, request=request)

    @classmethod
    async def info(cls, user_id: int, object_model: Any, action: str, request: Request):
        await cls.log(LogLevelEnum.INFO, user_id=user_id, object_model=object_model, action=action, request=request)

    @classmethod
    async def warning(cls, user_id: int, object_model: Any, action: str, request: Request):
        await cls.log(LogLevelEnum.WARNING, user_id=user_id, object_model=object_model, action=action, request=request)

    @classmethod
    async def error(cls, user_id: int, object_model: Any, action: str, request: Request):
        await cls.log(LogLevelEnum.ERROR, user_id=user_id, object_model=object_model, action=action, request=request)

    @classmethod
    async def critical(cls, user_id: int, object_model: Any, action: str, request: Request):
        await cls.log(LogLevelEnum.CRITICAL, user_id=user_id, object_model=object_model, action=action, request=request)

    @staticmethod
    async def log(level: LogLevelEnum, user_id: int, object_model: Any, action: str, request: Request) -> None:
        await LogRepository.create(level=level, user_id=user_id, object_model=object_model, action=action,
                                   request=request)
