import typing

from pydantic import (
    BaseModel,
)


class BatchRequest(BaseModel):
    data: dict[str, typing.Any]


class KeysRequest(BaseModel):
    keys: list[str]
