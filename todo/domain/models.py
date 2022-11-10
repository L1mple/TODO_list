from datetime import datetime

from .common.models import Entity


class Task(Entity[str]):
    """Domain model for Task of TODO_list."""

    description: str
    deadline: datetime | None = None
    exp_date: datetime | None = None
