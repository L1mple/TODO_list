from abc import ABC, abstractmethod

from bson import ObjectId

from todo.database.models import TaskDb
from todo.domain.models import Task


class AbstractRepository(ABC):
    """Abstract repository for repository pattern."""

    @abstractmethod
    async def add(self, task: Task):
        """Add method in repository."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, uid: str):
        """Get method in repository."""
        raise NotImplementedError

    @abstractmethod
    async def list_all(self):
        """List method in repository."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, uid: str):
        """Delete method in repository."""
        raise NotImplementedError


class MongoDbRepository(AbstractRepository):
    """Repository for MongoDb."""

    def __init__(self, task_collection):
        self.task_collection = task_collection

    async def add(self, task_data: TaskDb):
        """Add method in repository."""
        task = await self.task_collection.insert_one(task_data)
        new_student = await self.task_collection.find_one({"_id": task.inserted_id})
        return new_student

    async def get(self, uid: ObjectId):
        """Get method in repository."""
        task = await self.task_collection.find_one({"_id": uid})
        if not task:
            return "404 NOT FOUND"
        return task

    async def list_all(self):
        """List method in repository."""
        tasks = []
        async for task in self.task_collection.find():
            tasks.append(task)
        return tasks

    async def delete(self, uid: ObjectId):
        """Delete method in repository."""
        task = await self.task_collection.find_one({"_id": uid})
        if task:
            await self.task_collection.delete_one({"_id": uid})
        return task


class FakeMongoRepository(AbstractRepository):
    """Fake repository for tests."""

    def __init__(self, tasks: list[Task]):
        self._tasks = set(tasks)

    def add(self, task: Task):
        """Add method in repository."""
        self._tasks.add(task)

    def get(self, uid: ObjectId):
        """Get method in repository."""
        return next(task for task in self._tasks if task.uid == uid)

    def list_all(self):
        """List method in repository."""
        return list(self._tasks)

    def delete(self, uid: ObjectId):
        """Delete method in repository."""
        self._tasks.remove(next(task for task in self._tasks if task.uid == uid))
