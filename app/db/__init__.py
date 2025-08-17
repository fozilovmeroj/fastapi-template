from typing import AsyncGenerator

from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase

from ..core import config as db_config

engine: AsyncEngine = create_async_engine(db_config.DATABASE_URL)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False
)

class Base(DeclarativeBase):
    pass


class WithTimeStamp(Base):
    __abstract__ = True
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
