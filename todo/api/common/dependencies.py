from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI
from toolz import pipe

from todo.dependencies import Container
from todo.service.celery.celery_worker import create_celery
from todo.service.celery.settings import CelerySettings


def bootstrap(app: FastAPI) -> FastAPI:
    """Bootstrap general dependencies."""
    return pipe(
        app,
        add_celery,
    )


@inject
def add_celery(
    app: FastAPI,
    celery_settings: CelerySettings = Provide[Container.celery_settings],
) -> FastAPI:
    app.celery_app = create_celery(
        app_name=celery_settings.NAME,
        broker_url=celery_settings.connection_str(),
        backend_url=celery_settings.connection_str(),
    )
    return app
