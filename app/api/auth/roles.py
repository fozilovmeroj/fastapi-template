from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import get_session
from app.db.models.auth.roles import Role

router = APIRouter(tags=["roles"])


@router.get("/")
async def get_roles(session=Depends(get_session)):
    query = select(Role).options(selectinload(Role.permissions))
    role = (await session.execute(query)).scalar_one()
    await session.commit()
    return {"roles": role}
