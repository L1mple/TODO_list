from typing import Protocol

from .models import Task, TaskUID, UpdateTask
from .repository import AbstractTaskRepository


class AbstractTaskService(Protocol):
    """Abstract service."""

    async def create_one(
        self,
        new_task: Task,
    ) -> TaskUID:
        """Create new task."""
        raise NotImplementedError

    async def get_by_uid(
        self,
        task_uid: TaskUID,
    ) -> Task | None:
        """Find one Task by it's uid."""
        raise NotImplementedError

    async def get_many(
        self,
        page: int,
        per_page: int,
    ) -> list[Task]:
        """Find multiple paginated tasks."""
        raise NotImplementedError

    async def complete(
        self,
        task_uid: TaskUID,
    ) -> None:
        """Mark task as completed."""
        raise NotImplementedError

    async def update_one(
        self,
        update_task: UpdateTask,
    ) -> None:
        """Update info about Task."""
        raise NotImplementedError

    async def delete_by_uid(
        self,
        task_uid: TaskUID,
    ) -> None | TaskUID:
        """Delete all info about Task."""
        raise NotImplementedError


class DatabaseTaskService(AbstractTaskService):
    """Implementation of AbstractTaskService."""

    def __init__(self, repository: AbstractTaskRepository) -> None:
        self.repository = repository

    async def create_one(
        self,
        new_task: Task,
    ) -> TaskUID:
        """Create new task."""
        return await self.repository.create_one(new_task)

    async def get_by_uid(
        self,
        task_uid: TaskUID,
    ) -> Task | None:
        """Find one Task by it's uid."""
        return await self.repository.read_one_by_uid(task_uid)

    async def get_many(
        self,
        page: int,
        per_page: int,
    ) -> list[Task]:
        """Find multiple paginated tasks."""
        return await self.repository.get_many(page, per_page)

    async def complete(self, task_uid: TaskUID) -> None:
        """Mark task as completed."""
        update = UpdateTask(
            uid=task_uid,
            done=True,
        )
        return await self.repository.update_one(update)

    async def update_one(
        self,
        update_task: UpdateTask,
    ) -> None:
        """Edit info about Task."""
        return await self.repository.update_one(update_task)

    async def delete_by_uid(
        self,
        task_uid: TaskUID,
    ) -> None | TaskUID:
        """Delete all info about Task with this particular uid."""
        return await self.repository.delete_one_by_uid(task_uid)
