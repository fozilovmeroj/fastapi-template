import i18n
from fastapi import APIRouter, Depends
from pydantic import EmailStr

from app.db.connection import get_session
from app.schemas.auth.password import ChangePasswordSchema
from app.schemas.base import ResponseSchema
from app.services.password import PasswordService
from app.services.user_service import UserService

router = APIRouter(tags=["password"])


@router.get("/forget", response_model=ResponseSchema)
async def forget_password(email: EmailStr, session=Depends(get_session)):
    password_service = PasswordService(session)
    await password_service.generate_reset_password(email)
    return ResponseSchema(status=True, message='user.code_sent')


@router.post("/change", response_model=ResponseSchema)
async def change_password(form: ChangePasswordSchema, session=Depends(get_session)):
    password_service = PasswordService(session)
    await password_service.change_password(form)
    return ResponseSchema(status=True, message='user.password_changed')


@router.get("/reset", response_model=ResponseSchema)
async def reset_password(email: EmailStr, session=Depends(get_session)):
    password_service = PasswordService(session)
    await password_service.reset_password(email)
    return ResponseSchema(status=True, message='user.password_reset')
