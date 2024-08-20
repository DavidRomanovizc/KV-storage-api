import dataclasses

import asynctnt

from .services import FetcherImpl, WriterImpl
from config import load_config


@dataclasses.dataclass
class TarantoolClient:
    _config = load_config()
    _client = asynctnt.Connection(host=_config.tarantool.host, port=_config.tarantool.port)

    fetcher: FetcherImpl = FetcherImpl(_client, space=_config.tarantool.space)
    writer: WriterImpl = WriterImpl(_client, space=_config.tarantool.space)


__all__ = (
    "TarantoolClient",
)
