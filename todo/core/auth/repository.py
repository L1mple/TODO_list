from typing import Protocol

from .models import Identity, IdentityUID


class AbstractIdentityRepository(Protocol):
    """Abstract repository for repository pattern."""

    async def create_one(self, identity: Identity) -> IdentityUID:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read_one_by_uid(self, uid: IdentityUID) -> Identity | None:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete_one_by_uid(self, uid: IdentityUID) -> None | IdentityUID:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def update_one(self, update_user: Identity) -> None | IdentityUID:
        """Abstract method in generic repository."""
        raise NotImplementedError
