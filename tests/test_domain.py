from datetime import datetime
from typing import Optional

from todo.Domain.models import Task


def make_task(
    example_desc: str, example_deadline: Optional[datetime], example_exp_date: datetime
):
    return Task(example_desc, example_deadline, example_exp_date)


def test_domain_change_deadline_of_the_task():
    task1 = make_task("example_task", "14.01.2003", "10.02.2003")
    old_deadline = task1.deadline
    new_deadline = datetime.now()
    task1.change_deadline(new_deadline)
    assert task1.deadline != old_deadline
    assert task1.deadline == new_deadline


def test_domain_change_description_of_the_task():
    task1 = make_task("example_task", "14.01.2003", "10.02.2003")
    old_description = task1.description
    new_description = "literally new desc"
    task1.change_deadline(new_description)
    assert task1.deadline != old_description
    assert task1.deadline == new_description


def test_domain_equals_tasks():
    task1 = make_task("example_task", "14.01.2003", "10.02.2003")
    task2 = make_task("example_task", "14.01.2003", "10.02.2003")
    assert task1 != task2


def test_making_task_withot_deadline():
    task = make_task("example_task", None, "10.02.2003")
    assert task.deadline is None
