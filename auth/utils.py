import datetime
import typing

from jose import (
    jwt,
)

import config


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password


def authenticate_user(
        fake_db: dict[str, dict[str, typing.Any]],
        username: str,
        password: str,
) -> dict[str, typing.Any] | None:
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
