"""Common error handlers.

Error handler is a function that takes request and some Exception. Based on Exception
type (just like singledispatch) it chooses function to handle the error and convert that
to some common format.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def bootstrap(app: FastAPI) -> FastAPI:
    """Bootstrap general error handlers."""
    app.add_exception_handler(Exception, any_exception_handler)
    return app


def any_exception_handler(_: Request, err: Exception) -> JSONResponse:  # noqa
    return JSONResponse(status_code=500, content=(str(err)))
