import secrets

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt

from app.db import get_session
from app.db.models.auth import User, Token, UserLogin
from app.schemas.auth import SignInSchema, SignUpSchema, SignInResponse
from app.schemas.users import UserSchema
from app.utils.auth import get_current_user

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

        client_host = request.client.host
        user_agent = request.headers.get("user-agent")
        user_login = UserLogin(user_agent=user_agent, ip_address=client_host, user_id=user.id)

        session.add(token)
        session.add(user_login)
        await session.commit()
        return SignInResponse(token=access_token, user=user)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/me", response_model=UserSchema)
async def me(user=Depends(get_current_user)):
    return user
