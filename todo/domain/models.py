from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    """Domain model for Task of TODO_list."""

    uid: str
    description: str
    deadline: datetime | None = None
    exp_date: datetime | None = None
