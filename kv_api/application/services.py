import json
from typing import (
    Any,
)

import asynctnt
from asynctnt import (
    Response,
)

from .exceptions import (
    ConnectionErrorException,
    DomainException,
    DuplicateKeyException,
    IntegrityErrorException,
)


class FetcherImpl:
    def __init__(self, tarantool_client: asynctnt.Connection, space: str) -> None:
        self.conn = tarantool_client
        self._space = space

    async def fetch(self, key: str) -> Response:
        async with self.conn as accessor:
            try:
                result = await accessor.select(self._space, key=[key])
            except Exception:
                raise DomainException()
            return result

    async def fetch_all(self, keys: list[str]) -> dict[str, Any]:
        data = {}
        for key in keys:
            result = await self.fetch(key)
            if result:
                key, serialized_data = result[0]
                data[key] = json.loads(serialized_data)
        return data


class WriterImpl:
    def __init__(self, tarantool_client: asynctnt.Connection, space: str) -> None:
        self.conn = tarantool_client
        self._space = space

    async def write(self, data: dict[str, str | int]) -> None:
        async with self.conn as accessor:
            for key, value in data.items():
                serialized_data = json.dumps(value)
                try:
                    await accessor.insert(self._space, (key, serialized_data))
                except Exception as ex:
                    try:
                        f_error_msg = (ex.message.split()[0]).lower()  # type: ignore
                    except Exception:
                        raise DomainException()
                    if "duplicate" in f_error_msg:
                        raise DuplicateKeyException() from ex
                    elif "integrity" in f_error_msg:
                        raise IntegrityErrorException() from ex
                    else:
                        raise ConnectionErrorException() from ex
