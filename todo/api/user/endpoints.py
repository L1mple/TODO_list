from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI, status
from fastapi.responses import JSONResponse

from todo.api.auth.dependencies import get_current_user
from todo.core.user.models import User
from todo.core.user.services import AbstractUserService
from todo.dependencies import Container

from .contracts import UserJSONResponse

router = APIRouter(prefix="/user", tags=["User"])


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize task router for app."""
    app.include_router(router)
    return app


@router.get(
    "/me/",
    response_model=UserJSONResponse,
    responses={
        404: {"description": "No tasks found"},
    },
)
@inject
async def read_users_me(
    current_username: str = Depends(get_current_user),  # noqa
    user_service: AbstractUserService = Depends(  # noqa
        Provide[Container.user_service]
    ),
):
    """Fetch the current logged in user."""
    current_user: User | None = await user_service.read_one_by_username(
        current_username
    )
    if current_user is None:
        # log that identity exists but user doesn't
        return JSONResponse(
            content=None,
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return UserJSONResponse.from_entity(current_user)
