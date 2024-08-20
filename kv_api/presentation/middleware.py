import httpx
from starlette.exceptions import (
    HTTPException,
)
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)
from starlette.requests import (
    Request,
)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, verify_access_url: str):
        super().__init__(app)
        self.verify_access_url = verify_access_url

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")

        if not token:
            return HTTPException(detail="Unauthorized", status_code=401)

        async with httpx.AsyncClient() as client:
            response = await client.post(self.verify_access_url, headers={"Authorization": token})
            if response.status_code != 200:
                return HTTPException(detail="Unauthorized", status_code=401)

            data = response.json()
            if not data.get("access_granted", False):
                return HTTPException(detail="Unauthorized", status_code=401)

        response = await call_next(request)
        return response
