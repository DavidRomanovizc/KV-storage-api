import dataclasses
import http
from typing import (
    ClassVar,
)

from common import (
    DomainException,
)


@dataclasses.dataclass(eq=False)
class DuplicateKeyException(DomainException):
    """Exception for duplicate keys"""
    status: ClassVar[int] = http.HTTPStatus.CONFLICT

    @property
    def title(self) -> str:
        return "A record with the same key already exists"


@dataclasses.dataclass(eq=False)
class IntegrityErrorException(DomainException):
    """Exception for integrity errors"""
    status: ClassVar[int] = http.HTTPStatus.BAD_REQUEST

    @property
    def title(self) -> str:
        return "Integrity constraint violation"


@dataclasses.dataclass(eq=False)
class ConnectionErrorException(DomainException):
    """Exception for connection errors"""
    status: ClassVar[int] = http.HTTPStatus.SERVICE_UNAVAILABLE

    @property
    def title(self) -> str:
        return "Connection error"
