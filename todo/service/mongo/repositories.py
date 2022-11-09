from bson import ObjectId
from pydantic import BaseModel

from todo.domain.abstractions import AbstractRepository, AbstractTaskRepository
from todo.service.mongo.models import PyObjectId


async def helper(task_data) -> dict:
    """Parse method for repository."""
    return {
        "uid": str(task_data["_id"]),
        "description": task_data["description"],
        "deadline": task_data["deadline"],
        "exp_date": task_data["exp_date"],
    }


class MongoDbRepository(AbstractRepository):
    """Repository for MongoDb."""

    def __init__(self, some_collection):
        self.some_collection = some_collection

    async def create_one(self, document_data: BaseModel):
        """Create one method in repository."""
        await self.some_collection.insert_one(document_data.dict(by_alias=True))
        return "200 OK"

    async def create_many(self, documents: list[dict]):
        """Create many method in repository."""
        await self.some_collection.insert_many(documents)
        return "200 OK"

    async def get_one_by_id(self, uid: PyObjectId):
        """Get method in repository."""
        document = await self.some_collection.find_one({"_id": uid})
        if not document:
            return "404 NOT FOUND"
        return await helper(document)

    async def get_many(self, page: int = 0, per_page: int = 10):
        """Get many method in repository."""
        cursor = self.some_collection.find().skip(page - 1).limit(per_page - page)
        if not cursor:
            return "404 NOT FOUND"
        documents = []
        async for document in cursor:
            documents.append(await helper(document))
        return documents

    async def list_all(self):
        """List method in repository."""
        documents = []
        async for document in self.some_collection.find():
            documents.append(await helper(document))
        return documents

    async def delete_one_by_id(self, uid: PyObjectId):
        """Delete method in repository."""
        document = await self.some_collection.find_one({"_id": uid})
        if document:
            await self.some_collection.delete_one({"_id": uid})
        return await helper(document)

    async def replace_one(self, document: BaseModel):
        """Patch method in repository."""
        tuid = document.uid
        old_document = await self.get_one_by_id(tuid)
        if old_document == "404 NOT FOUND":
            return "404 document NOT FOUND"
        _id = PyObjectId(ObjectId(old_document["uid"]))
        await self.some_collection.replace_one(
            {"_id": _id}, document.dict(by_alias=True)
        )
        return "200 OK"


class MongoDbTaskRepository(MongoDbRepository, AbstractTaskRepository):
    """Repository for MongoDb and Task."""
