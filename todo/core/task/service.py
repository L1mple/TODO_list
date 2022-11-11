from .models import NewTask, Task, TaskUID, UpdateTask
from .repository import TaskRepository


async def create_one(
    new_task: NewTask,
    repository: TaskRepository,
) -> TaskUID:
    """Create new task."""
    task = Task(**new_task.dict())
    return await repository.insert_one(task)


async def get_by_uid(
    task_uid: TaskUID,
    repository: TaskRepository,
) -> Task | None:
    """Find one Task by it's uid."""
    return await repository.find_one_by_uid(task_uid)


async def get_many(
    page: int,
    per_page: int,
    repository: TaskRepository,
) -> list[Task]:
    """Find multiple paginated tasks."""
    return await repository.find_many_paginated(page, per_page)


async def complete(
    task_uid: TaskUID,
    repository: TaskRepository,
) -> None:
    """Mark task as completed."""
    update = UpdateTask(
        uid=task_uid,
        done=True,
    )
    return await repository.update_one(update)
