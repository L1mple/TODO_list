from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolz import pipe

from todo.dependencies import Container

from .settings import ApiSettings


def bootstrap(app: FastAPI) -> FastAPI:
    """Bootstrap general middleware."""
    return pipe(
        app,
        _add_cors,
    )


@inject
def _add_cors(
    app: FastAPI,
    api_settings: ApiSettings = Provide[Container.api_settings],
) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_settings.CORS_ALLOW_ORIGINS,
        allow_credentials=api_settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=api_settings.CORS_ALLOW_METHODS,
        allow_headers=api_settings.CORS_ALLOW_HEADERS,
    )
    return app
