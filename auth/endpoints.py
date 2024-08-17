import datetime
from typing import (
    Any,
)

from jose import (
    JWTError,
    jwt,
)
from starlette import (
    status,
)
from starlette.exceptions import (
    HTTPException,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
)
from starlette.routing import Route

from auth import (
    config,
    dto,
)

__all__ = (
    "setup_routes",
)


def setup_routes() -> list[Route]:
    routes = [
        Route("/api/login", login, methods=["POST"]),
        Route("/api/verify-access", verify_access, methods=["POST"]),
    ]
    return routes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password


def authenticate_user(
        fake_db: dict[str, dict[str, Any]],
        username: str,
        password: str,
) -> dict[str, Any] | None:
    user = fake_db.get(username)
    if not user or not verify_password(password, user["password"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: datetime.timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


async def login(request: Request) -> JSONResponse:
    body = await request.json()
    try:
        token_request = dto.TokenRequest(**body)
    except AttributeError:
        raise HTTPException(
            detail="Invalid login data", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    user = authenticate_user(config.fake_users_db, token_request.username, token_request.password)
    if not user:
        raise HTTPException(detail="Invalid credentials", status_code=401)

    access_token_expires = config.get_token_expiration()
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    token = dto.TokenResponse(token=access_token)
    return JSONResponse(token.model_dump())


async def verify_access(request: Request) -> JSONResponse:
    auth_header = request.headers.get("Authorization")
    token = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[len("Bearer "):]

    if not token:
        raise HTTPException(detail="Token not founded", status_code=401)

    try:
        jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        response = dto.AccessResponse(access_granted=True)
    except JWTError:
        response = dto.AccessResponse(access_granted=False)

    return JSONResponse(response.model_dump())
