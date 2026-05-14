from sqlalchemy import select, or_

from app.db.connection import async_session
from app.db.models.auth.auth import User, Token


class TokenRepository:
    @staticmethod
    async def get_by_id(user_id: int) -> User:
        async with async_session() as session:
            stmt = select(User).where(User.id == user_id)
            user = (await session.execute(stmt)).scalar()
            return user

    @staticmethod
    async def get_by_login(login: str, phone: str | None = None) -> User:
        async with async_session() as session:
            query = select(User).where(or_(User.email == login, User.phone == (phone or login)))
            user = (await session.execute(query)).scalar()
            return user

    @staticmethod
    async def create(user_id: int, access_token: str) -> None:
        async with async_session() as session:
            token = Token(access_token=access_token, user_id=user_id)
            session.add(token)
            await session.commit()
