from celery import Celery
from dependency_injector.wiring import Provide, inject

from todo.dependencies import Container
from todo.service.celery.settings import CelerySettings


def create_celery_app() -> Celery:
    """Factory for celery app."""
    container = Container()
    container.wire(modules=[__name__])
    celery_app = Celery(
        container.celery_settings.provided.NAME,
        broker=container.celery_settings.provided.broker_connection_str(),
        backend=container.celery_settings.provided.result_connection_str(),
    )
    return celery_app


celeryyy = create_celery_app()


# @inject
# def create_celery(celery_settings: CelerySettings = Provide[Container.celery_settings]) -> Celery:
#     """Factory for celery app."""
#     celery_app = Celery(
#         celery_settings.NAME,
#         broker=celery_settings.broker_connection_str(),
#         backend=celery_settings.result_connection_str(),
#     )
#     return celery_app
# Еще я пытался сделать так, но там 'Provide' object has no attribute NAME ошибка была и я не смог нагуглить как пофиксить(
