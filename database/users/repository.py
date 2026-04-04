from database.base import base_db
from database.users.models import User
from datetime import datetime, timedelta


class UserRepository:
    """Repository class for users-related database operations."""

    def __init__(self, base_db):
        self.base_db = base_db
        self.collection_name = "users"

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Fetch a users by their unique ID."""
        collection = await self.base_db.get_collection(self.collection_name)
        user_data = await collection.find_one({"id": user_id})
        if user_data:
            return User(**user_data)
        return None

    async def create_user(self, user: User) -> User:
        """Create a new users in the database."""
        collection = await self.base_db.get_collection(self.collection_name)
        await collection.insert_one(user.dict())
        return user

    async def update_user(self, user_id: int, update_data: dict) -> User:
        """Update an existing users's information."""
        collection = await self.base_db.get_collection(self.collection_name)
        await collection.update_one({"id": user_id}, {"$set": update_data})
        updated_user_data = await collection.find_one({"id": user_id})
        return User(**updated_user_data)

    async def delete_user(self, user_id: int) -> bool:
        """Delete a users from the database."""
        collection = await self.base_db.get_collection(self.collection_name)
        result = await collection.delete_one({"id": user_id})
        return result.deleted_count > 0

    async def count_users_since(self, since_timestamp: float) -> int:
        """Count users registered since timestamp."""
        collection = await self.base_db.get_collection(self.collection_name)

        return await collection.count_documents({
            "created_at": {"$gte": str(since_timestamp)}
        })

    async def count_users_between(self, start: float, end: float) -> int:
        collection = await self.base_db.get_collection(self.collection_name)

        return await collection.count_documents({
            "created_at": {
                "$gte": str(start),
                "$lt": str(end)
            }
        })

user_repository = UserRepository(base_db)
