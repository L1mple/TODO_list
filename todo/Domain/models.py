import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    """Domain model for Task of TODO_list."""

    description: str = Field(default=...)
    deadline: Optional[datetime] = Field(default=None)
    exp_date: datetime = Field(default=None)
    task_id: uuid.UUID = Field(default=uuid.uuid1())

    def change_deadline(self, datetime: datetime):
        """Takes new deadline and rewrites old one."""
        self.deadline = datetime

    def change_description(self, new_description: str):
        """Takes new description and rewrites old one."""
        self.description = new_description
