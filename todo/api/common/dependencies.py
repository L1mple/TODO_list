"""Common FastAPI dependencies.

General dependencies that can be useful during development on API layer.

This might be frustrating as we already have todo.dependencies module powered by
dependency_injector which is not bad DI library. In this way this module is typically
empty, despite cases when we require some very FastAPI/API specific dependencies that
heavily rely on request.
"""

from fastapi import FastAPI


def bootstrap(app: FastAPI) -> FastAPI:
    """Bootstrap general dependencies."""
    return app
