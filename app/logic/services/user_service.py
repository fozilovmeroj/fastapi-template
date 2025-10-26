import secrets

from fastapi import Request, HTTPException
from passlib.hash import bcrypt
from pydantic import EmailStr

from app.db.models.auth.auth import User, Token, UserLogin
from app.logic.repositories.token_repository import TokenRepository
from app.logic.repositories.user_repository import UserRepository
from app.logic.services.base import WithSession
from app.logic.services.log_service import LogService
from app.schemas.auth.base import SignUpSchema, SignInSchema, SignInResponse
from app.schemas.users.base import UserSchema
from app.utils.request.base import get_log_data


class UserService(WithSession):
    @staticmethod
    async def is_unique(email: EmailStr, phone: str):
        user = await UserRepository.get_by_login(str(email), phone)

        if user:
            if user.email == email:
                raise HTTPException(status_code=400, detail="Email already exists")
            if user.phone == phone:
                raise HTTPException(status_code=400, detail="Phone already exists")

    @classmethod
    async def sign_up(cls, form: SignUpSchema) -> UserSchema:
        await cls.is_unique(email=form.email, phone=form.phone)

        user = await UserRepository.create(form.model_dump())
        return UserSchema.model_validate(user)

    async def sign_in(self, form: SignInSchema, request: Request) -> SignInResponse:
        user = await UserRepository.get_by_login(form.login)

        if bcrypt.verify(form.password, user.password):
            access_token = secrets.token_hex(32)
            await TokenRepository.create(user.id, access_token)

            user_login = UserLogin(**get_log_data(request), user_id=user.id)

            self.session.add(user_login)
            await self.session.commit()

            log_service = LogService()
            await log_service.info(user_id=user.id, object_model=user_login, action="sign in", request=request)

            return SignInResponse(user=UserSchema.model_validate(user), token=access_token)
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
