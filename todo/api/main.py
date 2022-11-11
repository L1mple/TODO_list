"""Module that builds FastAPI application for running Web API.

There we actually configure dependencies, build api and return it so ASGI can run it.
"""

from dependency_injector import providers
from fastapi import FastAPI
from toolz import pipe

from todo.dependencies import Container
from todo.service.mongo.task_repository import MongoTaskRepository

from . import common, task
from .common import dependencies, endpoints, error_handlers, event_handlers, middleware


def bootstrap() -> FastAPI:
    """Instantiate FastAPI-based Web API."""
    container = Container(
        task_repository=providers.Singleton(MongoTaskRepository),
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
        task.bootstrap,
    )
