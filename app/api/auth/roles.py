from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_session
from app.db.models.logging import Log

router = APIRouter(tags=["roles"])


@router.get("/")
async def get_roles(session: AsyncSession = Depends(get_session)):
    query = select(Log)
    log = (await session.execute(query)).scalars().first()
    return log
