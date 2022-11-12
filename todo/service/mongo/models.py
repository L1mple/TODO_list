from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from todo.domain.common.models import Entity
from todo.domain.task.models import Task, TaskUID


class PyObjectId(ObjectId):
    """Class for _id in mongodb."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validation of objectid."""
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoEntity(BaseModel):
    """Entity for mongodb and all mongodb models will inherit from this."""

    uid: PyObjectId = Field(alias="_id")

    def to_entity(self) -> Entity:
        """Convert MongoEntity to Entity from domain."""
        return Entity(
            uid=TaskUID(self.uid),
            **self.dict(exclude={"uid"}),  # Возможно тут надо написать {"_id"}
        )

    @staticmethod
    def from_entity(entity: Entity) -> "MongoEntity":
        """Convert Entity to MongoEntity."""
        return MongoEntity(
            uid=PyObjectId(ObjectId((entity.uid))),
            **entity.dict(exclude={"uid"}),
        )


class TaskDb(MongoEntity):
    """Domain model for Task of TODO_list."""

    created_at: datetime
    updated_at: datetime | None
    description: str
    deadline: datetime | None
    exp_date: datetime | None
    done: bool

    def to_entity(self) -> Task:
        """Convert TaskDb to Task from domain."""
        return Task(
            uid=TaskUID(self.uid),
            **self.dict(exclude={"uid"}),  # Возможно тут надо написать {"_id"}
        )

    @staticmethod
    def from_task_entity(entity: Task) -> "TaskDb":
        """Convert Task to TaskDb."""
        return TaskDb(
            uid=PyObjectId(ObjectId((entity.uid))),
            **entity.dict(exclude={"uid"}),
        )

    class Config:
        """Config for TaskDb."""

        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
