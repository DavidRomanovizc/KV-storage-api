import http

from application import (
    TarantoolClient,
)
from pydantic import (
    ValidationError,
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

from . import (
    dto,
)

__all__ = (
    "read",
    "write",
)

client = TarantoolClient()


async def read(request: Request) -> JSONResponse:
    body = await request.json()
    try:
        keys_req = dto.KeysRequest(**body)
    except ValidationError:
        raise HTTPException(status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY, detail="Input should be a valid list")
    data = await client.fetcher.fetch_all(keys=keys_req.keys)
    if not data:
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail="Value not founded")
    return JSONResponse({"data": data})


async def write(request: Request) -> JSONResponse:
    body = await request.json()
    batch_req = dto.BatchRequest(**body)

    await client.writer.write(data=batch_req.data)
    return JSONResponse({"status": "success"})
