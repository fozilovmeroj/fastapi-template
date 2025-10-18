from typing import Any, Sequence

from sqlalchemy import select

from app.core.types.exceptions.db import NotFoundModelError
from app.db.connection import async_session
from app.db.models.auth.roles import Role
from app.schemas.auth.roles import RoleCreateUpdate


class RoleRepository:
    @staticmethod
    async def get_all() -> Sequence[Role]:
        async with async_session() as session:
            stmt = select(Role)
            roles = (await session.execute(stmt)).scalars().all()
            return roles

    @staticmethod
    async def get_by_id(role_id: int) -> Role:
        async with async_session() as session:
            stmt = select(Role).where(Role.id == role_id)
            role = (await session.execute(stmt)).scalar()
            return role

    @staticmethod
    async def create(data: RoleCreateUpdate) -> Role:
        async with (async_session() as session):
            role = Role(name=data.name)
            session.add(role)
            await session.commit()
        return role

    @classmethod
    async def update(cls, role_id: int, data: RoleCreateUpdate) -> Role:
        async with (async_session() as session):
            role = await cls.get_by_id(role_id)
            if not role:
                raise NotFoundModelError(id=role_id, model="role")

            role.name = data.name
            session.add(role)
            await session.commit()
            await session.refresh(role)
        return role
    
    @classmethod
    async def delete(cls, role_id: int) -> Role:
        async with (async_session() as session):
            role = await cls.get_by_id(role_id)
            if not role:
                raise NotFoundModelError(id=role_id, model="role")

            await session.delete(role)
            await session.commit()
        return role
