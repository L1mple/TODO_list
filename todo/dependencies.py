from dependency_injector import containers, providers

# from todo.api.auth.dependencies import AuthScheme
from todo.api.common.settings import ApiSettings
from todo.core.auth.repository import AbstractIdentityRepository
from todo.core.auth.services import AbstractAuthService
from todo.core.auth.settings import AuthSettings
from todo.core.task.repository import AbstractTaskRepository
from todo.core.task.services import AbstractTaskService
from todo.core.user.repository import AbstractUserRepository
from todo.core.user.services import AbstractUserService
from todo.service.mongo.settings import MongoSettings


class Container(containers.DeclarativeContainer):
    """DI container."""

    mongo_settings = providers.Object(MongoSettings())
    api_settings = providers.Object(ApiSettings())
    auth_settings = providers.Object(AuthSettings())

    crypt_service = providers.AbstractSingleton()
    # auth_scheme = providers.Callable(
    #     AuthScheme, token_url=auth_settings.provided.TOKEN_URL
    # )

    task_repository = providers.AbstractSingleton(AbstractTaskRepository)
    task_service = providers.AbstractSingleton(AbstractTaskService)

    user_repository = providers.AbstractSingleton(AbstractUserRepository)
    user_service = providers.AbstractSingleton(AbstractUserService)

    identity_repository = providers.AbstractSingleton(AbstractIdentityRepository)
    auth_service = providers.AbstractSingleton(AbstractAuthService)
