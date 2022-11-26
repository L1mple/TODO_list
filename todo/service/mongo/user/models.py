from beanie import Document, PydanticObjectId
from pydantic import EmailStr

from todo.core.user.models import UpdateUser, User, UserUID


class UserMongoDb(Document):
    """Domain model for Task of TODO_list."""

    username: str
    email: EmailStr
    full_name: str | None
    active: bool
    admin: bool
    hashed_password: str

    class Settings:
        """Config for UserMongoDb."""

        name = "users"

    def to_entity(self) -> User:
        """Convert UserMongoDb to User from domain."""
        return User(
            uid=UserUID(self.id),
            **self.dict(exclude={"id"}),  # Возможно тут надо написать {"_id"}
        )

    @staticmethod
    def from_user_entity(entity: User) -> "UserMongoDb":
        """Convert User to UserMongoDb."""
        return UserMongoDb(
            _id=PydanticObjectId(entity.uid),
            **entity.dict(exclude={"uid"}),
        )

    @staticmethod
    def from_update_user_entity(entity: UpdateUser) -> "UserMongoDb":
        """Convert UpdateUser to UserMongoDb."""
        return UserMongoDb(
            _id=PydanticObjectId(entity.uid),
            **entity.dict(exclude={"uid"}),
        )
