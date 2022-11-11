from datetime import datetime

import pytest

from todo.core.models import Task


@pytest.fixture
def make_task():
    return Task(
        uid="1",
        description="example_desc",
        deadline=datetime(2003, 1, 14),
        exp_date=datetime(2003, 2, 10),
    )
