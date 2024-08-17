import asyncio

import uvicorn
from starlette.applications import (
    Starlette,
)

from auth.endpoints import (
    setup_routes,
)


async def start_server(app: Starlette) -> None:
    app_config = uvicorn.Config(
        app=app,
        host="127.0.0.1",
        port=8080,
        reload=True,
        use_colors=True,
        log_level="debug",
    )
    server = uvicorn.Server(config=app_config)
    await server.serve()


application = Starlette(debug=True, routes=setup_routes())

if __name__ == "__main__":
    with asyncio.Runner() as runner:
        try:
            runner.run(start_server(app=application))
        except KeyboardInterrupt:
            pass
