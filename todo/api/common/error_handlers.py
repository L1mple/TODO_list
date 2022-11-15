from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def bootstrap(app: FastAPI) -> FastAPI:
    """Bootstrap error handler."""
    app.add_exception_handler(Exception, any_exception_handler)
    return app


def any_exception_handler(request: Request, err: Exception) -> JSONResponse:
    """Custom exception hadler."""
    return JSONResponse(status_code=500, content=str(err))
