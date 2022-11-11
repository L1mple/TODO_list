"""Module for everything specific for /task sub route part of API."""

from fastapi import FastAPI
from toolz import pipe

from . import endpoints


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize task sub routes."""
    return pipe(
        app,
        endpoints.bootstrap,
    )
