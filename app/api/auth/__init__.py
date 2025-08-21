import secrets

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt

from app.db import get_session
from app.db.models.auth.auth import User, Token, UserLogin
from app.db.models.logging import Log
from app.schemas.auth import SignInSchema, SignUpSchema, SignInResponse
from app.schemas.users import UserSchema
from app.types.enums.log_level import LogLevelEnum
from app.utils.auth import get_current_user
from app.utils.request import get_log_data

router = APIRouter(tags=["auth"])


async def check_user_unique(session: AsyncSession, email: str, phone: str):
    stmt = select(User).where(or_(User.email == email, User.phone == phone))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        if user.email == email:
            raise HTTPException(status_code=400, detail="Email already exists")
        if user.phone == phone:
            raise HTTPException(status_code=400, detail="Phone already exists")


@router.post("/sign-up", response_model=UserSchema)
async def sign_up(form: SignUpSchema, session: AsyncSession = Depends(get_session)):
    await check_user_unique(session, str(form.email), form.phone)

    user = User(**form.model_dump())
    user.password = bcrypt.hash(user.password)
    session.add(user)
    return user


@router.post("/sign-in", response_model=SignInResponse)
async def sign_in(form: SignInSchema, request: Request, session: AsyncSession = Depends(get_session)):
    query = select(User).where(or_(User.email == form.login, User.phone == form.login))
    user = (await session.execute(query)).scalars().first()
    if bcrypt.verify(form.password, user.password):
        access_token = secrets.token_hex(32)
        token = Token(access_token=access_token, user_id=user.id)

        user_login = UserLogin(**get_log_data(request), user_id=user.id)


        session.add(token)
        session.add(user_login)
        await session.commit()

        log = Log(level=LogLevelEnum.INFO, user_id=user.id, **get_log_data(request), object=user_login, action="sign in")
        session.add(log)
        await session.commit()
        return SignInResponse(token=access_token, user=user)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/me", response_model=UserSchema)
async def me(user=Depends(get_current_user)):
    return user
