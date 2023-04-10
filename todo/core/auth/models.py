from pydantic import BaseModel

from todo.core.common.models import Entity

IdentityUID = str


class Token(BaseModel):
    """Domain model for AuthToken."""

    access_token: str
    token_type: str


class Identity(Entity[IdentityUID]):
    """Domain model for Identity as a part of AUTH module."""

    hashed_password: str

    class Config:
        """Extra config for Identity model."""

        schema_extra = {
            "example": {
                "uid": "507f191e810c19729de860ea",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # noqa
            }
        }
