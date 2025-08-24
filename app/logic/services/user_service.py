import secrets

from fastapi import Request, HTTPException
from passlib.hash import bcrypt
from sqlalchemy import select, or_

from app.db.models.auth.auth import User, Token, UserLogin
from app.logic.services.base import Service
from app.logic.services.log_service import LogService
from app.schemas.auth.base import SignUpSchema, SignInSchema, SignInResponse
from app.utils.request.base import get_log_data


class UserService(Service):
    async def get_user(self, login: str) -> User | None:
        query = select(User).where(or_(User.email == login, User.phone == login))
        user = (await self.session.execute(query)).scalars().first()
        return user

    async def is_unique(self, email: str, phone: str):
        stmt = select(User).where(or_(User.email == email, User.phone == phone))

        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            if user.email == email:
                raise HTTPException(status_code=400, detail="Email already exists")
            if user.phone == phone:
                raise HTTPException(status_code=400, detail="Phone already exists")

    async def sign_up(self, form: SignUpSchema) -> User:
        user = User(**form.model_dump())
        user.password = bcrypt.hash(user.password)
        self.session.add(user)
        return user

    async def sign_in(self, form: SignInSchema, request: Request) -> SignInResponse:
        user = await self.get_user(form.login)
        if bcrypt.verify(form.password, user.password):
            access_token = secrets.token_hex(32)
            token = Token(access_token=access_token, user_id=user.id)

            user_login = UserLogin(**get_log_data(request), user_id=user.id)

            self.session.add(token)
            self.session.add(user_login)
            await self.session.commit()

            log_service = LogService(self.session)
            await log_service.info(user_id=user.id, object=user_login, action="sign in", request=request)

            return SignInResponse(user=user, token=access_token)
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
