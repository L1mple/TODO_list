from typing import Protocol

from .models import UpdateUser, User, UserUID


class AbstractUserRepository(Protocol):
    """Abstract repository for repository pattern."""

    async def create_one(self, user: User) -> UserUID:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read_one_by_uid(self, uid: UserUID) -> User | None:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read_one_by_username(self, username: str) -> User | None:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete_one_by_uid(self, uid: UserUID) -> None | UserUID:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def update_one(self, update_user: UpdateUser) -> None | UserUID:
        """Abstract method in generic repository."""
        raise NotImplementedError
