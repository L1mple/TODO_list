import motor.motor_asyncio


class Database:
    """init mongodb in class."""

    def __init__(self, mongo_url: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        self.database = self.client.task
        self.task_collection = self.database.task_collection
