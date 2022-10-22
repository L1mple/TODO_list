import uuid
from datetime import datetime
from typing import Optional


class Task:
    """Domain model for Task of TODO_list."""

    def __init__(
        self, description: str, deadline: Optional[datetime], exp_date: datetime
    ):
        self.id = uuid.uuid4()
        self.description = description
        self.deadline = deadline
        self.exp_date = exp_date

    def __repr__(self):
        return f"Task {self.description} with deadline: {self.deadline}"

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return other.id == self.id

    def __hash__(self):
        return hash(self.description + str(self.exp_date))

    def change_deadline(self, datetime: datetime):
        """Takes new deadline and rewrites old one."""
        self.deadline = datetime

    def change_description(self, new_description: str):
        """Takes new description and rewrites old one."""
        self.description = new_description
