from typing import Protocol

from .models import TUID, Entity


class AbstractRepository(Protocol[TUID]):
    """Generic repository."""

    async def create_one(self, entity: Entity) -> TUID:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read_one_by_uid(self, uid: TUID) -> Entity | None:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def update_one(self, entity: Entity) -> None:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete_one_by_uid(self, uid: TUID) -> None:
        """Abstract method in generic repository."""
        raise NotImplementedError
