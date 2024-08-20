from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from common import DomainException
from .endpoints import read, write
from .middleware import AuthMiddleware


def setup_routes() -> list[Route]:
    routes = [
        Route("/api/read", read, methods=["GET"]),
        Route("/api/write", write, methods=["POST"])
    ]

    return routes


async def exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content={"message": exc.title},
    )


def setup_exception_handler(app: Starlette) -> None:
    app.add_exception_handler(DomainException, exception_handler)


def setup_middlewares() -> list[Middleware]:
    middlewares = [
        Middleware(AuthMiddleware, verify_access_url="http://auth:8000/api/verify-access")
    ]
    return middlewares


__all__ = (
    "setup_routes",
    "setup_exception_handler",
    "setup_middlewares",
)
