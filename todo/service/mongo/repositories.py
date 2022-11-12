from bson import ObjectId

from todo.domain.common.models import Entity, EntityUID
from todo.domain.task.models import Task
from todo.domain.task.repository import AbstractRepository, AbstractTaskRepository
from todo.service.mongo.models import MongoEntity, PyObjectId


class MongoDbRepository(AbstractRepository[EntityUID]):
    """implementation of AbstractRepository."""

    def __init__(self, some_collection):
        self.some_collection = some_collection

    async def create_one(self, entity: Entity) -> EntityUID:
        """Create document method."""
        doc_entity = MongoEntity.from_entity(entity=entity)
        existing_doc: MongoEntity = MongoEntity(
            **await self.some_collection.find_one({"_id": doc_entity.uid})
        )

        if existing_doc is not None:
            return "Непонятно что делать("

        result = await self.some_collection.insert_one(doc_entity.dict(by_alias=True))
        return EntityUID(result.inserted_id)

    async def read_one_by_uid(self, uid: EntityUID) -> Entity | None:
        """Read document method."""
        document_id = PyObjectId(ObjectId(uid))
        result: MongoEntity = MongoEntity(
            **await self.some_collection.find_one({"_id": document_id})
        )

        if result is None:
            return None

        return result.to_entity()

    async def update_one(self, entity: Entity) -> None:
        """Update document method."""
        doc_entity = MongoEntity.from_entity(entity=entity)
        fields = {}
        entity_content = doc_entity.dict(by_alias=True)
        for key, value in entity_content:
            if value is not None:
                fields[key] = value
        existing_document = await self.some_collection.find_one({"_id": doc_entity.uid})

        if existing_document is not None:
            await self.some_collection.update_one(
                {"_id": doc_entity.uid}, {"$set": fields}
            )

    async def delete_one_by_uid(self, uid: EntityUID) -> None:
        """Delete document method."""
        document_id = PyObjectId(ObjectId(uid))
        existing_document = await self.some_collection.find_one({"_id": document_id})

        if existing_document is not None:
            await self.some_collection.delete_one({"_id": document_id})


class MongoDbTaskRepository(MongoDbRepository, AbstractTaskRepository):
    """Repository for MongoDb and Task."""

    def __init__(self, task_collection):
        self.task_collection = task_collection

    async def create_one(self, task: Task) -> EntityUID:
        return await super().create_one(Task)
