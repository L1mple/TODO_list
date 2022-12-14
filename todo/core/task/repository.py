from typing import Protocol

from .models import Task, TaskUID, UpdateTask


class AbstractTaskRepository(Protocol):
    """Abstract repository for repository pattern."""

    async def create_one(self, task: Task) -> TaskUID:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read_one_by_uid(self, uid: TaskUID) -> Task | None:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def update_one(self, task: UpdateTask) -> None:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete_one_by_uid(self, uid: TaskUID) -> None | TaskUID:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def get_many(self, page: int = 0, per_page: int = 10) -> list[Task]:
        """Abstract method in generic repository."""
        raise NotImplementedError
