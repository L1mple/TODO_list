from datetime import datetime

from beanie import Document, PydanticObjectId

from todo.core.task.models import Task, TaskUID, UpdateTask, UserUID


class TaskMongoDb(Document):
    """Database model for Task of TODO_list."""

    created_at: datetime | None
    updated_at: datetime | None
    description: str | None
    deadline: datetime | None
    exp_date: datetime | None
    done: bool | None
    expired: bool | None
    owner_uid: UserUID | None

    class Settings:
        """Config for TaskMongoDb."""

        name = "tasks"

    def to_entity(self) -> Task:
        """Convert TaskMongoDb to Task from database."""
        return Task(
            uid=TaskUID(self.id),
            **self.dict(exclude={"id"}),  # Возможно тут надо написать {"_id"}
        )

    @staticmethod
    def from_task_entity(entity: Task) -> "TaskMongoDb":
        """Convert Task to TaskMongoDb."""
        return TaskMongoDb(
            _id=PydanticObjectId(entity.uid),
            **entity.dict(exclude={"uid"}),
        )

    @staticmethod
    def from_update_task_entity(entity: UpdateTask) -> "TaskMongoDb":
        """Convert UpdateTask to TaskMongoDb."""
        return TaskMongoDb(
            _id=PydanticObjectId(entity.uid),
            **entity.dict(exclude={"uid"}),
        )
