from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import selectinload

from app.db import get_session
from sqlalchemy import select

from app.db.models.auth.auth import Token

bearer_token = HTTPBearer(auto_error=True)


async def get_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_token)) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header"
        )
    return credentials.credentials


async def get_current_user(token=Depends(get_bearer_token), session=Depends(get_session)):
    query = select(Token).where(Token.access_token == token).options(selectinload(Token.user))
    token_obj = (await session.execute(query)).scalars().first()

    if not token_obj:
        raise HTTPException(status_code=401, detail="Invalid token")
    if token_obj.expires_in < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")
    return token_obj.user
