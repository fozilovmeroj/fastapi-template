from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                {"detail": "Missing or invalid Authorization header"}, status_code=401
            )

        token = auth_header.split(" ")[1]
        user = verify_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Добавляем user в request.state
        request.state.user = user
        response = await call_next(request)
        return response
