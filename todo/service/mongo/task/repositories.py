from beanie import PydanticObjectId

from todo.core.common.models import TaskUID
from todo.core.task.models import Task, UpdateTask
from todo.core.task.repository import AbstractTaskRepository
from todo.service.mongo.task.models import TaskMongoDb


class MongoTaskRepository(AbstractTaskRepository):
    """Implementation of AbstractTaskRepository."""

    async def create_one(self, task: Task) -> TaskUID:
        """Create method in repository."""
        task_doc = TaskMongoDb.from_task_entity(task)
        await TaskMongoDb.save(task_doc)
        return TaskUID(task_doc.id)

    async def read_one_by_uid(self, uid: TaskUID) -> Task | None:
        """Read method in repository."""
        result: TaskMongoDb | None = await TaskMongoDb.get(
            document_id=PydanticObjectId(uid)
        )
        if result is None:
            return None
        return result.to_entity()

    async def update_one(self, task: UpdateTask) -> None | TaskUID:
        """Update method in repository."""
        existing_document = await TaskMongoDb.get(
            document_id=PydanticObjectId(task.uid)
        )
        if existing_document is None:
            return None
        await existing_document.set(task.dict(exclude_unset=True, exclude={"uid"}))
        return TaskUID(existing_document.id)

    async def delete_one_by_uid(self, uid: TaskUID) -> None | TaskUID:
        """Delete method in repository."""
        existing_document = await TaskMongoDb.get(document_id=PydanticObjectId(uid))
        if existing_document is None:
            return None
        await existing_document.delete()
        return TaskUID(existing_document.id)

    async def get_many(self, page: int = 0, per_page: int = 10) -> list[Task]:
        """Paginate method in repository."""
        existing_docs: list[TaskMongoDb] = await (
            TaskMongoDb.find().skip(page * per_page).limit(per_page).to_list()
        )
        return list(map(TaskMongoDb.to_entity, existing_docs))
