from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.schemas.base import ResponseSchema
from app.logic.services.user_service import UserService
from app.schemas.auth.base import SignInSchema, SignUpSchema, SignInResponse
from app.schemas.users.base import UserSchema
from app.utils.auth.auth import get_current_user

router = APIRouter(tags=["auth"])


@router.post("/sign-up", response_model=ResponseSchema[UserSchema])
async def sign_up(form: SignUpSchema):
    user = await UserService.sign_up(form)
    return ResponseSchema(message='auth.sign_up.success', data=user)


@router.post("/sign-in", response_model=ResponseSchema[SignInResponse])
async def sign_in(form: SignInSchema, request: Request, session: AsyncSession = Depends(get_session)):
    user_service = UserService(session)
    data = await user_service.sign_in(form, request)
    return ResponseSchema(message="", data=data)


@router.get("/me", response_model=UserSchema)
async def me(user=Depends(get_current_user)):
    return user
