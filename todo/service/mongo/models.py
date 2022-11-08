from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field


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

    class Config:
        """Config for TaskDb."""

        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
