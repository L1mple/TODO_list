import pymongo

MONGO_URL = "mongodb://localhost:27017"

client = pymongo.MongoClient(MONGO_URL)

database = client.tasks

tasks_collection = database.get_collection("tasks_collection")
