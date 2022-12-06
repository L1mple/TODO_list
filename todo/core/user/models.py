from pydantic import BaseModel, EmailStr

from todo.core.common.models import Entity, IdentityUID, UserUID


class User(Entity[UserUID]):
    """Domain model for User of TODO_list."""

    username: str
    email: EmailStr
    full_name: str | None
    active: bool = True
    admin: bool = False
    identity: IdentityUID

    class Config:
        """Extra config for User model."""

        schema_extra = {
            "example": {
                "uid": "507f191e810c19729de860ea",
                "username": "example_username",
                "email": "123@examplemail.com",
                "full_name": "example name",
                "active": "False",
                "identity": "str",
            }
        }


class UpdateUser(Entity[UserUID]):
    """Domain model for Update method in repository."""

    username: str
    email: EmailStr | None
    full_name: str | None
    active: bool | None
    admin: bool | None

    class Config:
        """Extra config for UpdateUser model."""

        schema_extra = {
            "example": {
                "uid": "507f191e810c19729de860ea",
                "username": "example_username",
                "email": "other123@examplemail.com",
                "full_name": "other example name",
            }
        }


class UserSignUp(BaseModel):
    """Domain model for SignUp endpoint."""

    username: str
    email: EmailStr
    password: str

    class Config:
        """Extra config for UpdateUser model."""

        schema_extra = {
            "example": {
                "username": "example_username",
                "email": "other123@examplemail.com",
                "password": "1234",
            }
        }
