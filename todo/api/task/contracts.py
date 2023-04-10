from datetime import datetime

from caseconverter import camelcase  # noqa
from toolz import keymap

from todo.api.common.contracts import JSONContract
from todo.core.task.models import Task


class TaskJSONResponse(JSONContract):
    """JSONRespponse for Task."""

    uid: str
    created_at: datetime

    description: str | None = None
    deadline: datetime | None = None
    exp_date: datetime | None = None
    done: bool = False
    updated_at: datetime | None = None
    expired: bool = False
    owner_uid: str | None = None

    @staticmethod
    def from_entity(entity: Task) -> "TaskJSONResponse":
        """Convert Task to JSONResponse."""
        return TaskJSONResponse(**keymap(camelcase, entity.dict()))
