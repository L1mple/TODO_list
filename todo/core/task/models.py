from datetime import datetime

from pydantic import Field

from todo.core.common.models import Auditable, Entity, TaskUID


class Task(Entity[TaskUID], Auditable):
    """Domain model for Task of TODO_list."""

    description: str
    deadline: datetime | None = None
    exp_date: datetime | None = None
    done: bool = False
    expired: bool = False

    class Config:
        """Extra config for Task model."""

        schema_extra = {
            "example": {
                "created_at": "2022-11-15T17:11:25.927Z",
                "updated_at": "2022-11-15T17:11:25.927Z",
                "uid": "507f191e810c19729de860ea",
                "description": "example description",
                "deadline": "2022-11-15T17:11:25.927Z",
                "exp_date": "2022-11-15T17:11:25.927Z",
                "done": False,
                "expired": False,
            }
        }


class UpdateTask(Entity[TaskUID]):
    """Domain model for Update method in repository."""

    updated_at: datetime = Field(default_factory=datetime.utcnow)
    description: str | None = None
    deadline: datetime | None = None
    exp_date: datetime | None = None
    done: bool | None = None
    expired: bool | None = None

    class Config:
        """Extra config for UpdateTask model."""

        schema_extra = {
            "example": {
                "created_at": "2022-11-15T17:11:25.927Z",
                "updated_at": "2022-11-15T17:11:25.927Z",
                "uid": "507f191e810c19729de860ea",
                "description": "other example description",
            }
        }
