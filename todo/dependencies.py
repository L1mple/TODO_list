from dependency_injector import containers, providers

from todo.domain.task.repository import AbstractTaskRepository
from todo.service.mongo.connection import Database


class Container(containers.DeclarativeContainer):
    """DI container."""

    config = providers.Object()

    database_client = providers.Singleton(Database, config.MONGODB_URL)

    task_repository = providers.AbstractSingleton(AbstractTaskRepository)
