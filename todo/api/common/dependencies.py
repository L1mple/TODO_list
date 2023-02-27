from fastapi import FastAPI


def bootstrap(app: FastAPI) -> FastAPI:
    """Bootstrap general dependencies."""
    return app
