from typing import Protocol, TypeVar

from .models import TUID, Entity

TEntity = TypeVar("TEntity", bound=Entity)


class AbstractRepository(Protocol[TEntity, TUID]):
    """Generic repository."""

    async def create_one(self, entity: TEntity) -> TUID:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def create_many(self, entities: list[TEntity]) -> list[TUID]:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def get_one_by_uid(self, uid: TUID) -> TEntity | None:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def get_many(self, page: int = 0, per_page: int = 10) -> list[TEntity]:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete_one_by_uid(self, uid: TUID) -> None:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def replace_one(self, entity: TEntity) -> None:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def list_all(self) -> list[TEntity]:
        """Abstract method in generic repository."""
        raise NotImplementedError
