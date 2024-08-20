import asyncio

from starlette.applications import (
    Starlette,
)
import uvicorn

from endpoints import (
    setup_routes,
)


async def start_server(app: Starlette) -> None:
    app_config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
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
