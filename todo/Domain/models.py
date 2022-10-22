from datetime import datetime
from typing import Optional
import uuid


class Task:
    def __init__(
            self,
            description: str,
            deadline: Optional[datetime],
            exp_date: datetime):
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
        self.deadline = datetime

    def change_description(self, new_description: str):
        self.description = new_description
