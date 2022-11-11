"""Module for storing HTTP Request/Response Contracts for task submodule.

Term "Contract" had been picked due to it philological nature. Contract means some
agreement and request/response models are actually some agreements between app and it's
clients.

Request classes have "Request" postfix, response - "Response"
"""
from datetime import datetime

from caseconverter import camelcase  # noqa
from toolz import keymap

from todo.api.common.contracts import JSONContract
from todo.core.task.models import Task


class TaskJSONResponse(JSONContract):  # noqa

    uid: str
    name: str
    created_at: datetime

    description: str | None = None
    deadline: datetime | None = None
    done: bool = False
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: Task) -> "TaskJSONResponse":  # noqa
        return TaskJSONResponse(**keymap(camelcase, entity.dict()))
