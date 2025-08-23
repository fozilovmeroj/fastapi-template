from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.schemas.base import ResponseSchema
from app.services.user_service import UserService
from app.schemas.auth.auth import SignInSchema, SignUpSchema, SignInResponse
from app.schemas.users import UserSchema
from app.utils.auth.auth import get_current_user

router = APIRouter(tags=["auth"])


@router.post("/sign-up", response_model=UserSchema)
async def sign_up(form: SignUpSchema, session: AsyncSession = Depends(get_session)):
    user_service = UserService(session)
    await user_service.is_unique(email=form.email, phone=form.phone)
    return await user_service.sign_up(form)


@router.post("/sign-in", response_model=ResponseSchema[SignInResponse])
async def sign_in(form: SignInSchema, request: Request, session: AsyncSession = Depends(get_session)):
    user_service = UserService(session)
    data = await user_service.sign_in(form, request)
    return ResponseSchema(message="", data=data)


@router.get("/me", response_model=UserSchema)
async def me(user=Depends(get_current_user)):
    return user
