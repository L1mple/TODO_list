from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from todo.core.auth.models import Token
from todo.core.auth.services import AbstractAuthService
from todo.core.auth.settings import AuthSettings
from todo.core.user.models import User, UserSignUp
from todo.dependencies import Container

from .contracts import TokenJSONResponse

router = APIRouter(tags=["Auth"], prefix="/auth")


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize task router for app."""
    app.include_router(router)
    return app


@router.post(
    "/login",
    response_model=TokenJSONResponse,
    responses={
        401: {"description": "Incorrect username or password"},
    },
)
@inject
async def post_login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa
    auth_service: AbstractAuthService = Depends(  # noqa
        Provide[Container.auth_service]
    ),
    auth_settings: AuthSettings = Depends(Provide[Container.auth_settings]),  # noqa
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
    access_token: Token = await auth_service.create_access_token(
        user.username, auth_settings=auth_settings
    )
    return TokenJSONResponse.from_entity(access_token)


@router.post(
    "/signup",
    response_model=TokenJSONResponse,
    status_code=201,
    responses={201: {"description": "Succesfully registered"}},
)
@inject
async def post_signup(
    new_user: UserSignUp = Body(default=..., description="Data about new user"),  # noqa
    auth_service: AbstractAuthService = Depends(  # noqa
        Provide[Container.auth_service]
    ),
    auth_settings: AuthSettings = Depends(Provide[Container.auth_settings]),  # noqa
):
    """Take data about user.

    -> check if user already exists;
    -> if not -> create new user;
    -> response with Token.
    """
    hashed_password = await auth_service.get_password_hash(new_user.password)
    existing_user = await auth_service.check_if_user_exists(new_user.username)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with this username or email already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    result = await auth_service.register(
        UserSignUp(
            username=new_user.username,
            password=hashed_password,
            email=new_user.email,
        )
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with this username or email already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token: Token = await auth_service.create_access_token(
        new_user.username, auth_settings=auth_settings
    )
    return TokenJSONResponse.from_entity(access_token)
