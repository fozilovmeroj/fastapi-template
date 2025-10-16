from fastapi import APIRouter
from app.logic.repositories.user_repository import UserRepository
from app.schemas.base import ResponseSchema
from app.schemas.users.base import UserSchema, UserCreate, UserUpdate

router = APIRouter(tags=["users"])


@router.get("/", response_model=ResponseSchema[list[UserSchema]])
async def get_users():
    return ResponseSchema[list[UserSchema]](status=True, message="auth.users.got_all",
                                            data=await UserRepository.get_all())


@router.get("/{id}", response_model=ResponseSchema[UserSchema])
async def get_user(id: int):
    return ResponseSchema[UserSchema](status=True, message="auth.users.got",
                                      data=await UserRepository.get_by_id(id))


@router.post("/", response_model=ResponseSchema[UserSchema])
async def create_user(data: UserCreate):
    return ResponseSchema[UserSchema](status=True, message="auth.users.created",
                                      data=await UserRepository.create(data.model_dump()))


@router.put("/{id}", response_model=ResponseSchema[UserSchema])
async def edit_user(id: int, data: UserUpdate):
    return ResponseSchema[UserSchema](status=True, message="auth.users.updated",
                                      data=await UserRepository.update(id, data.model_dump(exclude_unset=True)))


@router.delete("/{id}", response_model=ResponseSchema[UserSchema])
async def delete_user(id: int):
    return ResponseSchema[UserSchema](status=True, message="auth.users.deleted",
                                      data=await UserRepository.delete(id))
