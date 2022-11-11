"""Module for storing dependency container.

Highly suggested to use Object provider for BaseSettings as Configuration provider just
looses all typing, validation and logic that might be the part of settings.

When some dependency must be configured at startup use Abstract dependencies and
override them on application startup.
"""

from dependency_injector import containers, providers

from todo.api.common.settings import ApiSettings
from todo.core.task.repository import TaskRepository
from todo.service.mongo.settings import MongoSettings


class Container(containers.DeclarativeContainer):
    """DI container."""

    # settings
    api_settings = providers.Object(ApiSettings())
    mongo_settings = providers.Object(MongoSettings())

    # repositories
    task_repository = providers.AbstractSingleton(TaskRepository)
