from fastapi import FastAPI

from todo.api.endpoints import router
from todo.config import Settings
from todo.dependencies import Container


def create_api() -> FastAPI:
    """Init FastAPI instance."""
    di_container = Container()
    di_container.config.from_pydantic(Settings())
    di_container.wire(modules=["todo.api.endpoints"])

    api = FastAPI()
    api.include_router(router)
    return api
