from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from todo.core.auth.settings import AuthSettings
from todo.dependencies import Container


class AuthScheme:
    """Class for auth scheme."""

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@inject
async def get_current_user(
    token: str = Depends(AuthScheme.oauth2_scheme),  # noqa
    auth_settings: AuthSettings = Depends(Provide[Container.auth_settings]),  # noqa
):
    """Check if user logged in."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token=token,
            key=auth_settings.SECRET_KEY.get_secret_value(),
            algorithms=[auth_settings.ALGORITHM],
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        return credentials_exception
    return username
