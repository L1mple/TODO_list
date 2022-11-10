from typing import Generic, TypeVar

from pydantic import BaseModel

TUID = TypeVar("TUID")


class Entity(Generic[TUID], BaseModel):
    """Base class with uid."""

    uid: TUID
