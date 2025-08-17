from fastapi import APIRouter
import secrets

from app.schemas.auth import SignInSchema

router = APIRouter()


@router.get("/sign-in", response_model=SignInSchema)
async def sign_in(form: SignInSchema):

    pass
