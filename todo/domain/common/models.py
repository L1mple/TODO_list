from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

TUID = TypeVar("TUID")

TaskUID = str
EntityUID = str


class Entity(Generic[TUID], BaseModel):
    """Base class with uid."""

    uid: TUID


class Auditable(BaseModel):
    """Base model for objects that require tracking create/update time."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
