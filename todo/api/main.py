from dependency_injector import providers
from fastapi import FastAPI
from toolz import pipe

from todo.core.task.services import DatabaseTaskService
from todo.dependencies import Container
from todo.service.mongo.task.repositories import MongoTaskRepository

from . import common, task
from .common import dependencies, endpoints, error_handlers, event_handlers, middleware
from .task import endpoints as task_endpoints


def create_api() -> FastAPI:
    """Instantiate FastAPI-based Web API."""
    container = Container()

    container.task_repository.override(providers.Singleton(MongoTaskRepository))
    container.task_service.override(
        providers.Singleton(
            DatabaseTaskService,
            repository=container.task_repository.provided,
        )
    )
    container.wire(packages=[common, task])

    return pipe(
        container.api_settings().create_app(),
        # commons
        dependencies.bootstrap,
        error_handlers.bootstrap,
        event_handlers.bootstrap,
        middleware.bootstrap,
        # routes
        endpoints.bootstrap,
        task_endpoints.bootstrap,
    )
