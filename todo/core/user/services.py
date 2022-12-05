from typing import Protocol

from jose import JWTError, jwt

from todo.core.auth.settings import AuthSettings

from .models import UpdateUser, User, UserUID
from .repository import AbstractUserRepository


class AbstractUserService(Protocol):
    """Abstract service."""

    async def create_one(self, user: User) -> UserUID:
        """Abstract method to create User document."""
        raise NotImplementedError

    async def read_one_by_uid(self, uid: UserUID) -> User | None:
        """Abstract method to read User document."""
        raise NotImplementedError

    async def read_one_by_username(self, username: str) -> User | None:
        """Abstract method to read User document."""
        raise NotImplementedError

    async def update_one(self, update_user: UpdateUser) -> None | UserUID:
        """Abstract method to update User document."""
        raise NotImplementedError

    async def delete_one_by_uid(self, uid: UserUID) -> None | UserUID:
        """Abstract method to delete User document."""
        raise NotImplementedError

    async def decode_username_from_token(
        self,
        token: str,
        auth_settings: AuthSettings,
    ):
        """Abstract method to encode jwt token."""
        raise NotImplementedError


class UserService(AbstractUserService):
    """Implementation of AbstractUserService."""

    def __init__(self, repository: AbstractUserRepository) -> None:
        self.repository = repository

    async def create_one(self, user: User) -> UserUID:
        """Implementation of abstract method from AbstractUserService."""
        return await self.repository.create_one(user)

    async def read_one_by_uid(self, uid: UserUID) -> User | None:
        """Implementation of abstract method from AbstractUserService."""
        return await self.repository.read_one_by_uid(uid)

    async def read_one_by_username(self, username: str) -> User | None:
        """Implementation of abstract method from AbstractUserService."""
        return await self.repository.read_one_by_username(username)

    async def update_one(self, update_user: UpdateUser) -> None | UserUID:
        """Implementation of abstract method from AbstractUserService."""
        return await self.repository.update_one(update_user)

    async def delete_one_by_uid(self, uid: UserUID) -> None | UserUID:
        """Implementation of abstract method from AbstractUserService."""
        return await self.repository.delete_one_by_uid(uid)

    async def decode_username_from_token(
        self,
        token: str,
        auth_settings: AuthSettings,
    ):
        """Implementation fo abstract method from AbstractUserService."""
        try:
            payload = jwt.decode(
                token=token,
                key=auth_settings.SECRET_KEY.get_secret_value(),
                algorithms=[auth_settings.ALGORITHM],
            )
            username: str | None = payload.get("sub")
            if username is None:
                return None
        except JWTError:
            return None
        return username
