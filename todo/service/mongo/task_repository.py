from datetime import datetime

from beanie import Document, PydanticObjectId

from todo.core.task.models import Task, TaskUID, UpdateTask
from todo.core.task.repository import TaskRepository


class TaskDocument(Document):  # noqa

    name: str
    created_at: datetime
    updated_at: datetime | None
    description: str | None
    deadline: datetime | None
    done: bool

    @staticmethod
    def from_entity(entity: Task) -> "TaskDocument":  # noqa
        return TaskDocument(
            id=PydanticObjectId(entity.uid) if entity.uid is not None else None,
            **entity.dict(exclude={"uid"}),
        )

    def to_entity(self) -> Task:  # noqa
        return Task(
            uid=TaskUID(self.id),
            **self.dict(exclude={"id"}),
        )


class MongoTaskRepository(TaskRepository):  # noqa
    async def find_one_by_uid(self, uid: TaskUID) -> Task | None:  # noqa
        doc: TaskDocument | None = await TaskDocument.get(
            document_id=PydanticObjectId(uid)
        )

        if doc is None:
            return None

        return doc.to_entity()

    async def find_many_paginated(  # noqa
        self,
        page: int = 0,
        per_page: int = 10,
    ) -> list[Task]:
        docs: list[TaskDocument] = await (
            TaskDocument.find_all().skip(page * per_page).limit(per_page).to_list()
        )

        return list(map(TaskDocument.to_entity, docs))

    async def insert_one(self, task: Task) -> TaskUID:  # noqa
        doc = TaskDocument.from_entity(task)
        await TaskDocument.insert_one(doc)

        return TaskUID(doc.id)

    async def delete_one_by_uid(self, uid: TaskUID) -> None:  # noqa
        doc = await TaskDocument.get(document_id=PydanticObjectId(uid))

        if doc is not None:
            await doc.delete()

    async def update_one(self, update: UpdateTask) -> None:  # noqa
        fields = {}
        fields[TaskDocument.updated_at] = update.updated_at
        if update.name is not None:
            fields[TaskDocument.name] = update.name
        if update.description is not None:
            fields[TaskDocument.description] = update.description
        if update.deadline is not None:
            fields[TaskDocument.deadline] = update.deadline
        if update.done is not None:
            fields[TaskDocument.done] = update.done

        doc = await TaskDocument.get(document_id=PydanticObjectId(update.uid))
        if doc is not None:
            await doc.set(fields)
