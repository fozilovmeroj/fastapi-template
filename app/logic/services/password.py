from datetime import datetime

import i18n
from fastapi import HTTPException
from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db.models.auth.auth import PasswordReset
from app.logic.repositories.user_repository import UserRepository
from app.schemas.auth.password import ChangePasswordSchema
from app.logic.services.base import WithSession
from app.utils.generators.base import generate_code, generate_password


class PasswordService(WithSession):
    async def generate_reset_password(self, email: EmailStr) -> bool:
        user = await UserRepository.get_by_login(str(email))
        if not user:
            raise HTTPException(status_code=404, detail=i18n.t('user.not_found'))
        code = generate_code()
        reset_password = PasswordReset(code=code, user_id=user.id)
        self.session.add(reset_password)
        await self.session.commit()
        return True

    async def change_password(self, data: ChangePasswordSchema):
        query = (select(PasswordReset).filter(
            PasswordReset.expires_in > datetime.utcnow(),
            PasswordReset.code == data.code
        ).options(joinedload(PasswordReset.user)))
        code = (await self.session.execute(query)).scalar()
        if not code:
            raise HTTPException(status_code=404, detail=i18n.t('user.incorrect_code'))
        code.user.password = bcrypt.hash(data.password)
        await self.session.commit()
        return True

    async def reset_password(self, email: EmailStr):
        user = await UserRepository.get_by_login(str(email))
        if not user:
            raise HTTPException(status_code=404, detail=i18n.t('user.not_found'))
        new_password = generate_password()
        user.password = bcrypt.hash(new_password)
        await self.session.commit()
        return True
