import httpx
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, verify_access_url: str):
        super().__init__(app)
        self.verify_access_url = verify_access_url

    # TODO: Заменить JSONResponse на HTTPException
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")

        if not token:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)

        async with httpx.AsyncClient() as client:
            response = await client.post(self.verify_access_url, headers={"Authorization": token})
            if response.status_code != 200:
                return JSONResponse({"error": "Unauthorized"}, status_code=401)

            data = response.json()
            if not data.get("access_granted", False):
                return JSONResponse({"error": "Unauthorized"}, status_code=401)

        response = await call_next(request)
        return response
