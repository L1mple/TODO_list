"""Common actions to perform on startup and shutdown of FastAPI.

There we usually initialize some resources (database connections or in this case beanie)
or on the other hand free resources for graceful shutdown.
"""

from beanie import init_beanie
from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from todo.dependencies import Container
from todo.service.mongo.settings import MongoSettings
from todo.service.mongo.task_repository import TaskDocument


def bootstrap(app: FastAPI) -> FastAPI:
    """Bootstrap general event handlers."""
    app.add_event_handler("startup", initialize_beanie)
    return app


@inject
async def initialize_beanie(  # noqa
    mongo_settings: MongoSettings = Provide[Container.mongo_settings],
) -> None:
    connection_str = mongo_settings.connection_str()
    client = AsyncIOMotorClient(connection_str)

    await init_beanie(
        database=client[mongo_settings.DATABASE],
        document_models=[TaskDocument],  # type: ignore
    )
