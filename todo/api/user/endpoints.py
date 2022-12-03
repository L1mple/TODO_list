from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from todo.core.auth.models import Token
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


# @router.get("/users/me/", response_model=User)
# @inject
# async def read_users_me(
#     token: Token = Depends(oauth2_scheme),
#     user_service: AbstractUserService = Depends(Provide[Container.user_service]),
# ):
#     """Fetch the current logged in user."""
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     current_user = None
#     try:
#         current_user = await user_service.get_current_user(token.access_token)
#     finally:
#         if current_user is None:
#             raise credentials_exception
#     return UserJSONResponse.from_entity(current_user)
