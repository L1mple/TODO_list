from bson import ObjectId

from todo.domain.models import Task
from todo.repository.repo import AbstractRepository


class TaskService:
    """Service layer for api."""

    def __init__(self, repository: AbstractRepository) -> None:
        self._repository: AbstractRepository = repository

    async def get_users(self) -> list[Task]:
        return self._repository.list_all()

    async def get_user_by_id(self, task_id: ObjectId) -> Task:
        return self._repository.get(task_id)

    async def create_user(self, task_data: Task) -> Task:
        return self._repository.add(task=task_data)

    async def delete_user_by_id(self, task_id: ObjectId) -> None:
        return self._repository.delete(task_id)
