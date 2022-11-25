from fastapi import APIRouter, FastAPI

router = APIRouter(tags=["Common"])


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize common router for app."""
    app.include_router(router)
    return app


@router.get(
    "/ping",
    description="Endpoint that checks that API is up and running",
    status_code=204,
)
def get_ping():  # noqa
    return
