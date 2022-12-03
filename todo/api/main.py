from dependency_injector import providers
from fastapi import FastAPI
from toolz import pipe

from todo.core.auth.services import AuthService
from todo.core.task.services import DatabaseTaskService
from todo.core.user.services import UserService
from todo.dependencies import Container
from todo.service.mongo.task.repositories import MongoTaskRepository
from todo.service.mongo.user.repositories import MongoDbUserRepository

from . import auth, common, task
from .auth import endpoints as auth_endpoints
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
    container.user_repository.override(providers.Singleton(MongoDbUserRepository))
    container.user_service.override(
        providers.Singleton(UserService, repository=container.user_repository.provided)
    )
    container.auth_service.override(
        providers.Singleton(
            AuthService,
            user_service=container.user_service.provided,
            crypt_service=container.crypt_service,
        )
    )

    container.wire(packages=[common, task, auth])

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
        auth_endpoints.bootstrap,
    )
