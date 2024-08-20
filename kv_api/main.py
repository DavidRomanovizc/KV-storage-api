import asyncio

from presentation import (
    setup_exception_handler,
    setup_middlewares,
    setup_routes,
)
from starlette.applications import (
    Starlette,
)
import uvicorn


async def start_server(app: Starlette) -> None:
    app_config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8001,
        reload=True,
        use_colors=True,
        log_level="debug",
    )
    server = uvicorn.Server(config=app_config)
    await server.serve()


application = Starlette(
    debug=True,
    routes=setup_routes(),
    middleware=setup_middlewares(),
)
setup_exception_handler(application)

if __name__ == '__main__':
    with asyncio.Runner() as runner:
        try:
            runner.run(start_server(app=application))
        except KeyboardInterrupt:
            pass
