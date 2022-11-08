from dependency_injector import containers, providers

from todo.service.mongo.connection import Database
from todo.service.mongo.repositories import MongoDbTaskRepository


class Container(containers.DeclarativeContainer):
    """DI container."""

    config = providers.Configuration()

    database_client = providers.Singleton(Database, config.MONGODB_URL)

    task_repository = providers.Factory(
        MongoDbTaskRepository, task_collection=database_client.provided.task_collection
    )
