from fastapi import Request
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db.models.logging import Log
from app.core.types.enums.log_level import LogLevelEnum
from app.utils.request.base import get_log_data


class LogService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def info(self, user_id: int, object, action: str, request: Request):
        await self.log(LogLevelEnum.INFO, user_id=user_id, object=object, action=action, request=request)

    async def log(self, level: LogLevelEnum, user_id: int, object, action: str, request: Request):
        log = Log(level=level, user_id=user_id, **get_log_data(request), object=object, action=action)
        self.session.add(log)
        await self.session.commit()
