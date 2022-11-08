from bson import ObjectId

from todo.domain.abstractions import AbstractTaskRepository
from todo.service.mongo.models import PyObjectId, TaskDb


async def helper(task_data) -> dict:
    """Parse method for repository."""
    return {
        "uid": str(task_data["_id"]),
        "description": task_data["description"],
        "deadline": task_data["deadline"],
        "exp_date": task_data["exp_date"],
    }


async def updatehelper(task_data) -> dict:
    """Parse method for repository."""
    return {
        "uid": str(task_data.uid),
        "description": task_data.description,
        "deadline": task_data.deadline,
        "exp_date": task_data.exp_date,
    }


class MongoDbTaskRepository(AbstractTaskRepository):
    """Repository for MongoDb."""

    def __init__(self, task_collection):
        self.task_collection = task_collection

    async def create_one(self, task_data: TaskDb):
        """Create one method in repository."""
        await self.task_collection.insert_one(task_data.dict(by_alias=True))
        return "200 OK"

    async def create_many(self, tasks: list[dict]):
        """Create many method in repository."""
        await self.task_collection.insert_many(tasks)
        return "200 OK"

    async def get_one_by_id(self, uid: PyObjectId):
        """Get method in repository."""
        task = await self.task_collection.find_one({"_id": uid})
        if not task:
            return "404 NOT FOUND"
        return await helper(task)

    async def get_many(self, page: int = 0, per_page: int = 10):
        """Get many method in repository."""
        cursor = self.task_collection.find().skip(page - 1).limit(per_page - page)
        if not cursor:
            return "404 NOT FOUND"
        tasks = []
        async for task in cursor:
            tasks.append(await helper(task))
        return tasks

    async def list_all(self):
        """List method in repository."""
        tasks = []
        async for task in self.task_collection.find():
            tasks.append(await helper(task))
        return tasks

    async def delete_one_by_id(self, uid: PyObjectId):
        """Delete method in repository."""
        task = await self.task_collection.find_one({"_id": uid})
        if task:
            await self.task_collection.delete_one({"_id": uid})
        return await helper(task)

    async def replace_one(self, task: TaskDb):
        """Patch method in repository."""
        tuid = task.uid
        old_task = await self.get_one_by_id(tuid)
        if old_task == "404 NOT FOUND":
            return "404 TASK NOT FOUND"
        _id = PyObjectId(ObjectId(old_task["uid"]))
        await self.task_collection.replace_one({"_id": _id}, task.dict(by_alias=True))
        return "200 OK"
