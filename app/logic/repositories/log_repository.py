from typing import Any
from urllib.request import Request

from app.core.types.enums.log_level import LogLevelEnum
from app.db.connection import async_session
from app.db.models.logging import Log
from app.utils.request.base import get_log_data


class LogRepository:
    @classmethod
    async def create(cls, level: LogLevelEnum, user_id: int, object_model: Any, action: str, request: Request):
        async with async_session() as session:
            log = Log(level=level, user_id=user_id, **get_log_data(request), object=object_model, action=action)
            session.add(log)
