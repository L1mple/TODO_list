import pymongo


class Database:
    """init mongodb in class."""

    def __init__(self, mongo_url: str):
        self.database = pymongo.MongoClient(mongo_url)
        self.table = self.database.task
        self.collection = self.table.task_collection
