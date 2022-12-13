from beanie import init_beanie
from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from todo.dependencies import Container
from todo.service.mongo.identity.models import IdentityMongoDb
from todo.service.mongo.settings import MongoSettings
from todo.service.mongo.task.models import TaskMongoDb
from todo.service.mongo.user.models import UserMongoDb


def bootstrap(app: FastAPI) -> FastAPI:
    """Bootstrap general event handlers."""
    app.add_event_handler("startup", initialize_beanie)
    return app


@inject
async def initialize_beanie(
    mongo_settings: MongoSettings = Provide[Container.mongo_settings],
) -> None:
    """Initialize beanie function."""
    connection_str = mongo_settings.connection_str()
    client = AsyncIOMotorClient(connection_str)

    await init_beanie(
        database=client[mongo_settings.DATABASE],
        document_models=[TaskMongoDb, UserMongoDb, IdentityMongoDb],
    )
