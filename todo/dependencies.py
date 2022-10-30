from dependency_injector import containers, providers

from todo.config import Settings
from todo.database.connection import Database


class Container(containers.DeclarativeContainer):
    """DI container."""

    config = providers.Configuration(pydantic_settings=Settings())

    database_client = providers.Singleton(Database, config.MONGODB_URL)
