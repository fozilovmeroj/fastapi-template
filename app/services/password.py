from datetime import datetime

import i18n
from fastapi import HTTPException
from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.auth.auth import PasswordReset
from app.schemas.auth.password import ChangePasswordSchema
from app.services import Service
from app.services.user_service import UserService
from app.utils.generators import generate_code


class PasswordService(Service):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.user_service = UserService(self.session)

    async def generate_reset_password(self, email: EmailStr) -> bool:
        user = await self.user_service.get_user(email)
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
