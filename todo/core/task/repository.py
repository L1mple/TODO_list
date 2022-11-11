from typing import Protocol

from .models import Task, TaskUID, UpdateTask


class TaskRepository(Protocol):
    """Service for managing Task storage."""

    async def find_many_paginated(
        self,
        page: int = 0,
        per_page: int = 10,
    ) -> list[Task]:
        """Get multiple Tasks paginated."""
        ...

    async def find_one_by_uid(self, uid: TaskUID) -> Task | None:
        """Get one Task by unique identifier."""

    async def insert_one(self, task: Task) -> TaskUID:
        """Insert one new Task."""
        ...

    async def delete_one_by_uid(self, uid: TaskUID) -> None:
        """Delete on Task by uid."""

    async def update_one(self, update: UpdateTask) -> None:
        """Replace one Task by another based on uid."""
