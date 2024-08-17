import dataclasses
from typing import (
    Any,
)


@dataclasses.dataclass
class BaseModel:
    def model_dump(self, exclude_none: bool = False) -> dict[Any, Any]:
        if exclude_none:
            return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}
        return dataclasses.asdict(self)


@dataclasses.dataclass
class TokenRequest(BaseModel):
    username: str
    password: str


@dataclasses.dataclass
class TokenResponse(BaseModel):
    token: str


@dataclasses.dataclass
class AccessRequest(BaseModel):
    token: str


@dataclasses.dataclass
class AccessResponse(BaseModel):
    access_granted: bool
