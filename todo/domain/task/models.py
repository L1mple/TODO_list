from datetime import datetime

from pydantic import Field

from ..common.models import Auditable, Entity, TaskUID


class Task(Entity[TaskUID], Auditable):
    """Domain model for Task of TODO_list."""

    description: str
    deadline: datetime | None = None
    exp_date: datetime | None = None
    done: bool = False


class UpdateTask(Entity[TaskUID]):
    """Domain model for Update method in repository."""

    updated_at: datetime = Field(default_factory=datetime.utcnow)
    description: str | None = None
    deadline: datetime | None = None
    exp_date: datetime | None = None
    done: bool | None = None
