from dependency_injector import containers, providers

from todo.api.common.settings import ApiSettings
from todo.core.task.repository import AbstractTaskRepository
from todo.core.task.services import AbstractTaskService
from todo.service.mongo.settings import MongoSettings


class Container(containers.DeclarativeContainer):
    """DI container."""

    mongo_settings = providers.Object(MongoSettings())
    api_settings = providers.Object(ApiSettings())

    task_repository = providers.AbstractSingleton(AbstractTaskRepository)
    task_service = providers.AbstractSingleton(AbstractTaskService)
