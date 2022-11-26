from pydantic import EmailStr

from ..common.models import Entity, UserUID


class User(Entity[UserUID]):
    """Domain model for User of TODO_list."""

    username: str
    email: EmailStr
    full_name: str | None
    active: bool
    admin: bool = False
    hashed_password: str

    class Config:
        """Extra config for User model."""

        schema_extra = {
            "example": {
                "username": "example_username",
                "email": "123@examplemail.com",
                "full_name": "example name",
                "active": "False",
            }
        }


class UpdateUser(Entity[UserUID]):
    """Domain model for Update method in repository."""

    username: str
    email: EmailStr | None
    full_name: str | None
    active: bool | None
    admin: bool | None
    hashed_password: str | None

    class Config:
        """Extra config for UpdateUser model."""

        schema_extra = {
            "example": {
                "username": "example_username",
                "email": "other123@examplemail.com",
                "full_name": "other example name",
            }
        }
