from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.db.models.auth.auth import User
from app.logic.repositories.user_repository import UserRepository
from app.schemas.base import ResponseSchema
from app.schemas.users.base import UserSchema, UserCreate, UserUpdate

router = APIRouter(tags=["users"])


@router.get("/", response_model=list[UserSchema])
async def get_users():
    return await UserRepository.get_all()


@router.get("/{id}", response_model=ResponseSchema[UserSchema])
async def get_user(id: int):
    return await UserRepository.get_by_id(id)


@router.post("/", response_model=ResponseSchema[UserSchema])
async def create_user(data: UserCreate):
    return await UserRepository.create(data.model_dump())


@router.put("/{id}", response_model=ResponseSchema[UserSchema])
async def edit_user(id: int, data: UserUpdate):
    return await UserRepository.update(id, data.model_dump(exclude_unset=True))
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@router.delete("/{id}", response_model=ResponseSchema[UserSchema])
async def delete_user(id: int, session: AsyncSession = Depends(get_session)):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users
