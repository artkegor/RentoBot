from motor.motor_asyncio import AsyncIOMotorClient
from config import config


class BaseDB:
    """Base class for MongoDB connection and operations."""

    def __init__(self, db_url: str, db_name: str):
        self.client = AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]

    async def get_collection(self, collection_name: str):
        return self.db[collection_name]

    async def close(self):
        self.client.close()

    async def init_indexes(self):
        collection = await base_db.get_collection("listings")

        await collection.create_index([
            ("location", "2dsphere")
        ])


base_db = BaseDB(db_url=config.DB_URL, db_name=config.DB_NAME)
