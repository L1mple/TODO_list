from dependency_injector import providers
from fastapi import FastAPI
from toolz import pipe

from todo.api.auth.dependencies import CryptService
from todo.core.auth.services import AuthService
from todo.core.task.services import DatabaseTaskService
from todo.core.user.services import UserService
from todo.dependencies import Container
from todo.service.mongo.identity.repository import MongoDbIdentityRepository
from todo.service.mongo.task.repositories import MongoTaskRepository
from todo.service.mongo.user.repositories import MongoDbUserRepository

from . import auth, common, task, user
from .auth import endpoints as auth_endpoints
from .common import dependencies, endpoints, error_handlers, event_handlers, middleware
from .task import endpoints as task_endpoints
from .user import endpoints as user_endpoints


def create_api() -> FastAPI:
    """Instantiate FastAPI-based Web API."""
    container = Container()

    container.crypt_service.override(providers.Singleton(CryptService))
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
    container.identity_repository.override(
        providers.Singleton(MongoDbIdentityRepository)
    )
    container.auth_service.override(
        providers.Singleton(
            AuthService,
            repository=container.identity_repository.provided,
            user_service=container.user_service.provided,
            crypt_service=container.crypt_service.provided,
        )
    )

    container.wire(packages=[common, task, auth, user])

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
        user_endpoints.bootstrap,
    )
