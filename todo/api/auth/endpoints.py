from datetime import timedelta

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from todo.core.auth.models import Token
from todo.core.auth.services import AbstractAuthService
from todo.core.auth.settings import AuthSettings
from todo.core.user.models import User
from todo.dependencies import Container

from .contracts import TokenJSONResponse

router = APIRouter(tags=["Auth"])


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize task router for app."""
    app.include_router(router)
    return app


@router.post(
    "/token",
    response_model=TokenJSONResponse,
    responses={
        401: {"description": "Incorrect username or password"},
    },
)
@inject
async def post_token(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa
    auth_service: AbstractAuthService = Depends(  # noqa
        Provide[Container.auth_service]
    ),
):
    """Take data from form.

    Then get the user data from db,if its exist creates access_token.
    """
    user: User | None = await auth_service.authentificate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=AuthSettings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: Token = await auth_service.create_access_token(
        {"sub": user.username}, expires_delta=access_token_expires
    )
    return TokenJSONResponse.from_entity(access_token)
