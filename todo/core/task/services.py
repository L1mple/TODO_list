from typing import Protocol

from .models import Task, TaskUID, UpdateTask
from .repository import AbstractTaskRepository


class AbstractTaskService(Protocol):
    """Abstract service."""

    async def create_one(
        self,
        new_task: Task,
        repository: AbstractTaskRepository,
    ) -> TaskUID:
        """Create new task."""
        raise NotImplementedError

    async def get_by_uid(
        self,
        task_uid: TaskUID,
        repository: AbstractTaskRepository,
    ) -> Task | None:
        """Find one Task by it's uid."""
        raise NotImplementedError

    async def get_many(
        self,
        page: int,
        per_page: int,
        repository: AbstractTaskRepository,
    ) -> list[Task]:
        """Find multiple paginated tasks."""
        raise NotImplementedError

    async def complete(
        self,
        task_uid: TaskUID,
        repository: AbstractTaskRepository,
    ) -> None:
        """Mark task as completed."""
        raise NotImplementedError

    async def update_one(
        self,
        update_task: UpdateTask,
        repository: AbstractTaskRepository,
    ) -> None:
        """Update info about Task."""
        raise NotImplementedError


class MongoDbTaskService(AbstractTaskService):
    """Implementation of AbstractTaskService."""

    async def create_one(
        self,
        new_task: Task,
        repository: AbstractTaskRepository,
    ) -> TaskUID:
        """Create new task."""
        return await repository.create_one(new_task)

    async def get_by_uid(
        self,
        task_uid: TaskUID,
        repository: AbstractTaskRepository,
    ) -> Task | None:
        """Find one Task by it's uid."""
        return await repository.read_one_by_uid(task_uid)

    async def get_many(
        self,
        page: int,
        per_page: int,
        repository: AbstractTaskRepository,
    ) -> list[Task]:
        """Find multiple paginated tasks."""
        return await repository.get_many(page, per_page)

    async def complete(
        self,
        task_uid: TaskUID,
        repository: AbstractTaskRepository,
    ) -> None:
        """Mark task as completed."""
        update = UpdateTask(
            uid=task_uid,
            done=True,
        )
        return await repository.update_one(update)

    async def update_one(
        self,
        update_task: UpdateTask,
        repository: AbstractTaskRepository,
    ) -> None:
        """Edit info about Task."""
        return await repository.update_one(update_task)
