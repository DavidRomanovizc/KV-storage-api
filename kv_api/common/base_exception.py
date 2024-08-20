import dataclasses
import http
from typing import (
    ClassVar,
)


@dataclasses.dataclass(eq=False)
class AppException(Exception):
    """Base application exception"""
    status: ClassVar[int] = http.HTTPStatus.INTERNAL_SERVER_ERROR

    @property
    def title(self) -> str:
        return "An app error occurred"


@dataclasses.dataclass(eq=False)
class DomainException(AppException):
    """Domain-specific exception"""

    @property
    def title(self) -> str:
        return "A domain error occurred"
