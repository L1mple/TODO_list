from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from todo.api.auth.contracts import TokenJSONResponse
from todo.core.auth.models import Token
from todo.core.auth.settings import AuthSettings
from todo.core.user.models import User
from todo.core.user.services import AbstractUserService
from todo.dependencies import Container

from .contracts import UserJSONResponse

router = APIRouter(prefix="/user", tags=["User"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


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
    token: TokenJSONResponse = Depends(oauth2_scheme),
    user_service: AbstractUserService = Depends(Provide[Container.user_service]),
    auth_settings: AuthSettings = Depends(Provide[Container.auth_settings]),  # noqa
):
    """Fetch the current logged in user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    current_username = None
    try:
        current_username = await user_service.decode_username_from_token(
            str(token), auth_settings
        )
    finally:
        if current_username is None:
            raise credentials_exception
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
