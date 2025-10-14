from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.connection import get_session
from app.db.models.auth.roles import Role
from app.schemas.auth.roles import RoleSchema
from app.schemas.base import ResponseSchema

router = APIRouter(tags=["roles"])


@router.get("/", response_model=ResponseSchema[list[RoleSchema]])
async def get_roles(session=Depends(get_session)):
    query = select(Role).options(selectinload(Role.permissions))
    roles = (await session.execute(query)).scalars().all()
    await session.commit()
    return ResponseSchema[list[RoleSchema]](status=True, message="auth.roles.got_all", data=roles)
