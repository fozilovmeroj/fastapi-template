from fastapi import APIRouter

from app.logic.repositories.role_repository import RoleRepository
from app.schemas.auth.roles import RoleSchema, RoleCreateUpdate
from app.schemas.base import ResponseSchema

router = APIRouter(tags=["roles"])


@router.get("/", response_model=ResponseSchema[list[RoleSchema]])
async def get_roles():
    return ResponseSchema[list[RoleSchema]](status=True, message="auth.roles.got_all",
                                            data=await RoleRepository.get_all())


@router.get("/{id}", response_model=ResponseSchema[RoleSchema])
async def get_role(id: int):
    return ResponseSchema[RoleSchema](status=True, message="auth.roles.got",
                                      data=await RoleRepository.get_by_id(id))


@router.post("/", response_model=ResponseSchema[RoleSchema])
async def create_role(data: RoleCreateUpdate):
    return ResponseSchema[RoleSchema](status=True, message="auth.roles.created",
                                      data=await RoleRepository.create(data))


@router.put("/{id}", response_model=ResponseSchema[RoleSchema])
async def edit_role(id: int, data: RoleCreateUpdate):
    return ResponseSchema[RoleSchema](status=True, message="auth.roles.updated",
                                      data=await RoleRepository.update(id, data))


@router.delete("/{id}", response_model=ResponseSchema[RoleSchema])
async def delete_role(id: int):
    return ResponseSchema[RoleSchema](status=True, message="auth.roles.deleted",
                                      data=await RoleRepository.delete(id))
