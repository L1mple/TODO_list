from dependency_injector import providers
from fastapi import FastAPI
from toolz import pipe

from todo.dependencies import Container
from todo.core.task.services import MongoDbTaskService
from todo.service.mongo.repositories import MongoTaskRepository

from . import common, task
from .common import dependencies, endpoints, error_handlers, event_handlers, middleware
from .task import endpoints as task_endpoints


def create_api() -> FastAPI:
    """Instantiate FastAPI-based Web API."""
    container = Container(
        task_repository=providers.Singleton(MongoTaskRepository),
        task_service=providers.Singleton(MongoDbTaskService),
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
