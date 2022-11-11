"""Domain models for task submodule.

There we keep Entities, ValueObject, Aggregate Roots, Events, Messages.

If we see that it grows much than we need to split it or make it a packages and separate
models by purpose or by each (separate modules for entities, value objects, aggregate
root, etc. or separate module for each entity).
"""

from datetime import datetime

from pydantic import BaseModel, Field

from todo.core.common.models import Auditable, Entity

TaskUID = str


class Task(Entity[TaskUID], Auditable):
    """Domain model for Task of TODO_list."""

    name: str
    description: str | None = None
    deadline: datetime | None = None
    done: bool = False


class NewTask(BaseModel):
    """DTO for creating new task."""

    name: str
    description: str | None = None
    deadline: datetime | None = None


class UpdateTask(BaseModel):
    """DTO for updating task information."""

    uid: TaskUID
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    name: str | None = None
    description: str | None = None
    deadline: str | None = None
    done: bool | None = None
