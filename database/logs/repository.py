from database.base import base_db
from database.logs.models import Log
from datetime import datetime


class LogRepository:
    """Repository class for log-related database operations."""

    def __init__(self, base_db):
        self.base_db = base_db
        self.collection_name = "logs"

    async def get_collection(self) -> any:
        """Get the logs collection from the database."""
        return await self.base_db.get_collection(self.collection_name)

    async def create_log(self, log: Log) -> Log:
        """Create a new log entry in the database."""
        collection = await self.base_db.get_collection(self.collection_name)
        await collection.insert_one(log.dict())
        return log

    async def get_logs_by_action(self, action: str) -> list[Log]:
        """Fetch logs by their action type."""
        collection = await self.base_db.get_collection(self.collection_name)
        cursor = collection.find({"action": action})
        logs_data = await cursor.to_list(length=None)
        return [Log(**log_data) for log_data in logs_data]

    async def count_action_since(self, action: str, since_timestamp: float) -> int:
        """Count logs by action since timestamp."""
        collection = await self.get_collection()

        return await collection.count_documents({
            "action": action,
            "timestamp": {"$gte": str(since_timestamp)}
        })

    async def get_log_by_user_and_action(self, user_id: int, action: str) -> list[Log]:
        """Fetch logs by user ID and action type."""
        collection = await self.get_collection()
        cursor = collection.find({"user_id": user_id, "action": action})
        logs_data = await cursor.to_list(length=None)
        return [Log(**log_data) for log_data in logs_data]

    async def count_action_between(self, action: str, start: float, end: float) -> int:
        collection = await self.get_collection()

        return await collection.count_documents({
            "action": action,
            "timestamp": {
                "$gte": str(start),
                "$lt": str(end)
            }
        })

log_repository = LogRepository(base_db)
