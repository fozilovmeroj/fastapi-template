from pydantic import BaseModel


class SignInSchema(BaseModel):
    login: str
    password: str
