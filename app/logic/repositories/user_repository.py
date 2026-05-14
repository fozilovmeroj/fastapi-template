from typing import Any, Sequence

from sqlalchemy import select, or_
import bcrypt

from app.core.types.exceptions.db import NotFoundModelError
from app.db.connection import async_session
from app.db.models.auth.auth import User


class UserRepository:
    @staticmethod
    async def get_all() -> Sequence[User]:
        async with async_session() as session:
            stmt = select(User)
            users = (await session.execute(stmt)).scalars().all()
            return users

    @staticmethod
    async def get_by_id(user_id: int) -> User:
        async with async_session() as session:
            stmt = select(User).where(User.id == user_id)
            user = (await session.execute(stmt)).scalar()
            return user

    @staticmethod
    async def get_by_login(login: str, phone: str | None = None) -> User:
        async with async_session() as session:
            stmt = select(User).where(or_(User.email == login, User.phone == (phone or login)))
            user = (await session.execute(stmt)).scalar()
            return user

    @staticmethod
    async def create(data: dict[str, Any]) -> User:
        async with async_session() as session:
            user = User(**data)
            user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf8")
            session.add(user)
            await session.commit()
        return user

    @classmethod
    async def update(cls, user_id: int, data: dict[str, Any]) -> User:
        async with async_session() as session:
            user = await cls.get_by_id(user_id)
            if not user:
                raise NotFoundModelError(id=user_id, model="user")

            for key, value in data.items():
                setattr(user, key, value)
            if data["password"]:
                user.password = bcrypt.hash(user.password)

            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

    @classmethod
    async def delete(cls, user_id: int) -> User:
        async with async_session() as session:
            user = await cls.get_by_id(user_id)
            if not user:
                raise NotFoundModelError(id=user_id, model="user")

            await session.delete(user)
            await session.commit()
        return user
