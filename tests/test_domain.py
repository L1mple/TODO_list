from datetime import datetime

import pytest
from todo.domain.models import Task


@pytest.fixture
def make_task():
    return Task(
        description="example_desc",
        deadline=datetime(2003, 1, 14),
        exp_date=datetime(2003, 2, 10),
    )


def test_domain_change_deadline_of_the_task(make_task):
    task1 = make_task
    old_deadline = task1.deadline
    new_deadline = datetime.now()
    task1.change_deadline(new_deadline)
    assert task1.deadline != old_deadline
    assert task1.deadline == new_deadline


def test_domain_change_description_of_the_task(make_task):
    task1 = make_task
    old_description = task1.description
    new_description = "literally new desc"
    task1.change_description(new_description)
    assert task1.description != old_description
    assert task1.description == new_description
