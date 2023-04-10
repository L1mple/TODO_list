from beanie import PydanticObjectId

from todo.core.auth.models import Identity, IdentityUID
from todo.core.auth.repository import AbstractIdentityRepository
from todo.service.mongo.identity.models import IdentityMongoDb


class MongoDbIdentityRepository(AbstractIdentityRepository):
    """Implementation of AbstractIdentityRepository."""

    async def create_one(self, identity: Identity) -> IdentityUID:
        """Create method in repository."""
        identity_doc = IdentityMongoDb.from_identity_entity(identity)
        await IdentityMongoDb.save(identity_doc)
        return IdentityUID(identity_doc.id)

    async def read_one_by_uid(self, uid: IdentityUID) -> Identity | None:
        """Read method in repository."""
        result: IdentityMongoDb | None = await IdentityMongoDb.get(
            document_id=PydanticObjectId(uid)
        )
        if result is None:
            return None
        return result.to_entity()

    async def update_one(self, identity: Identity) -> None | IdentityUID:
        """Update method in repository."""
        existing_document = await IdentityMongoDb.get(
            document_id=PydanticObjectId(identity.uid)
        )
        if existing_document is None:
            return None
        await existing_document.set(identity.dict(exclude_unset=True, exclude={"uid"}))
        return IdentityUID(existing_document.id)

    async def delete_one_by_uid(self, uid: IdentityUID) -> None | IdentityUID:
        """Delete method in repository."""
        existing_document = await IdentityMongoDb.get(document_id=PydanticObjectId(uid))
        if existing_document is None:
            return None
        await existing_document.delete()
        return IdentityUID(existing_document.id)
