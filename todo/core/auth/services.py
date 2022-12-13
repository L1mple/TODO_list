from datetime import datetime, timedelta
from typing import Protocol

from jose import jwt
from passlib.context import CryptContext

from todo.core.auth.models import Identity, IdentityUID
from todo.core.auth.repository import AbstractIdentityRepository
from todo.core.auth.settings import AuthSettings
from todo.core.user.models import User, UserSignUp, UserUID
from todo.core.user.services import AbstractUserService

from .models import Token


class AbstractAuthService(Protocol):
    """Abstract service."""

    async def authentificate_user(self, username: str, password: str) -> User | None:
        """Abstract method of auth User."""
        raise NotImplementedError

    async def create_access_token(
        self,
        username: str,
        auth_settings: AuthSettings,
    ) -> Token:
        """Abstract method of creating Token."""
        raise NotImplementedError

    async def register(self, user: UserSignUp) -> UserUID | None:
        """Abstract method of signup User."""
        raise NotImplementedError

    async def read_one_by_uid(self, uid: IdentityUID) -> Identity | None:
        """Abstract method for read info from Db."""
        raise NotImplementedError

    async def get_password_hash(self, password: str) -> str:
        """Abstract method for hash password."""
        raise NotImplementedError

    async def check_if_user_exists(self, username: str) -> User | None:
        """Abstract method for check if user already exists."""
        raise NotImplementedError


class AuthService(AbstractAuthService):
    """Implementation of AbstractAuthService."""

    def __init__(
        self,
        repository: AbstractIdentityRepository,
        user_service: AbstractUserService,
        crypt_service: CryptContext,
    ) -> None:
        self.user_service = user_service
        self.pwd_context = crypt_service
        self.repository = repository

    async def authentificate_user(self, username: str, password: str) -> User | None:
        """Implementation method of auth User."""
        user: User | None = await self.user_service.read_one_by_username(
            username=username
        )
        if user is None:
            return None
        user_identity = await self.repository.read_one_by_uid(user.identity_uid)
        if user_identity is None:
            return None
        if not self.pwd_context.verify(password, user_identity.hashed_password):
            return None
        return user

    async def create_access_token(
        self,
        username: str,
        auth_settings: AuthSettings,
    ) -> Token:
        """Implemetation of method to create jwt token."""
        data = {"sub": username}
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            auth_settings.SECRET_KEY.get_secret_value(),
            algorithm=auth_settings.ALGORITHM,
        )
        return Token(  # noqa
            access_token=encoded_jwt,
            token_type="bearer",
        )

    async def register(self, user: UserSignUp) -> UserUID | None:
        """Implementation of method to register User."""
        identity_to_create = Identity(hashed_password=user.password)
        identity_created_uid = await self.repository.create_one(identity_to_create)

        user_to_create = User(
            identity_uid=identity_created_uid, **user.dict(exclude={"password"})
        )
        user_created_uid = await self.user_service.create_one(user_to_create)
        if user_created_uid is None:
            await self.repository.delete_one_by_uid(identity_created_uid)
            return None
        return user_created_uid

    async def check_if_user_exists(self, username: str) -> User | None:
        """Implemetation of method to check if user exists."""
        existing_user: User | None = await self.user_service.read_one_by_username(
            UserUID(username)
        )
        return existing_user

    async def get_password_hash(self, password: str) -> str:
        """Implementation of abstract method."""
        return self.pwd_context.hash(password)

    async def read_one_by_uid(self, uid: IdentityUID) -> Identity | None:
        """Implementation of abstract method from AbstractAuthService."""
        return await self.repository.read_one_by_uid(uid)
