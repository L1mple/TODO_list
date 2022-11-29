from datetime import datetime, timedelta
from typing import Protocol

from jose import jwt
from passlib.context import CryptContext

from todo.core.auth.settings import AuthSettings

from ..user.models import User
from ..user.services import AbstractUserService
from .models import Token


class AbstractAuthService(Protocol):
    """Abstract service."""

    async def authentificate_user(self, username: str, password: str) -> User | None:
        """Abstract method of auth User."""
        raise NotImplementedError

    async def create_access_token(
        self, data: dict, expires_delta: timedelta | None
    ) -> Token:
        """Abstract method of creating Token."""
        raise NotImplementedError


class AuthService(AbstractAuthService):
    """Implementation of AbstractAuthService."""

    def __init__(self, user_service: AbstractUserService) -> None:
        self.user_service = user_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def authentificate_user(self, username: str, password: str) -> User | None:
        """Implementation method of auth User."""
        user: User | None = await self.user_service.read_one_by_username(
            username=username
        )
        if user is None:
            return None
        if not self.pwd_context.verify(password, user.hashed_password):
            return None
        return user

    async def create_access_token(
        self, data: dict, expires_delta: timedelta | None
    ) -> Token:
        """Implemetation of method to create jwt token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=AuthSettings().ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            AuthSettings().SECRET_KEY.get_secret_value(),
            algorithm=AuthSettings().ALGORITHM,
        )
        return Token(  # noqa
            access_token=encoded_jwt,
            token_type="bearer",
        )
