from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from todo.domain.models import Task


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


class TaskDb(BaseModel):
    """Domain model for Task of TODO_list."""

    uid: PyObjectId | None = Field(alias="_id")
    description: str
    deadline: datetime | None = None
    exp_date: datetime | None = None

    def to_entity(self) -> Task:
        """Convert TaskDb to Task from domain."""
        return Task(
            uid=str(self.uid),
            description=self.description,
            deadline=self.deadline,
            exp_date=self.exp_date,
        )

    def from_entity(self, entity: Task):
        """Convert Task to TaskDb."""
        return TaskDb(
            _id=PyObjectId(ObjectId(entity.uid)),
            description=entity.description,
            deadline=entity.deadline,
            exp_date=entity.exp_date,
        )

    class Config:
        """Config for TaskDb."""

        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
