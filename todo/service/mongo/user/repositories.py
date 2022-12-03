from todo.core.user.models import UpdateUser, User, UserUID
from todo.core.user.repository import AbstractUserRepository

from .models import PydanticObjectId, UserMongoDb


class MongoDbUserRepository(AbstractUserRepository):
    """Implementation of AbstractUserRepository."""

    async def create_one(self, user: User) -> UserUID | None:
        """Create method in repository."""
        user_doc = UserMongoDb.from_user_entity(user)
        result_by_username = await UserMongoDb.find_one(
            UserMongoDb.username == user_doc.username
        )
        if result_by_username is not None:
            return None
        result_by_email = await UserMongoDb.find_one(
            UserMongoDb.email == user_doc.email
        )
        if result_by_email is not None:
            return None
        await UserMongoDb.save(user_doc)
        return UserUID(user_doc.username)

    async def read_one_by_uid(self, uid: UserUID) -> User | None:
        """Read method in repository."""
        result: UserMongoDb | None = await UserMongoDb.get(
            document_id=PydanticObjectId(uid)
        )
        if result is None:
            return None
        return result.to_entity()

    async def read_one_by_username(self, username: str) -> User | None:
        """Read method in repository."""
        result: UserMongoDb | None = await UserMongoDb.find_one(
            UserMongoDb.username == username
        )
        if result is None:
            return None
        return result.to_entity()

    async def update_one(self, update_user: UpdateUser) -> None | UserUID:
        """Update method in repository."""
        existing_document = await UserMongoDb.get(
            document_id=PydanticObjectId(update_user.uid)
        )
        if existing_document is None:
            return None
        await existing_document.set(
            update_user.dict(exclude_unset=True, exclude={"uid"})
        )
        return UserUID(existing_document.id)

    async def delete_one_by_uid(self, uid: UserUID) -> None | UserUID:
        """Delete method in repository."""
        existing_document = await UserMongoDb.get(document_id=PydanticObjectId(uid))
        if existing_document is None:
            return None
        await existing_document.delete()
        return UserUID(existing_document.id)
