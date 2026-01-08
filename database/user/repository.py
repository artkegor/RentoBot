from database.base import base_db
from database.user.models import User


class UserRepository:
    """Repository class for user-related database operations."""

    def __init__(self, base_db):
        self.base_db = base_db
        self.collection_name = "users"

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Fetch a user by their unique ID."""
        collection = await self.base_db.get_collection(self.collection_name)
        user_data = await collection.find_one({"id": user_id})
        if user_data:
            return User(**user_data)
        return None

    async def create_user(self, user: User) -> User:
        """Create a new user in the database."""
        collection = await self.base_db.get_collection(self.collection_name)
        await collection.insert_one(user.dict())
        return user

    async def update_user(self, user_id: int, update_data: dict) -> User:
        """Update an existing user's information."""
        collection = await self.base_db.get_collection(self.collection_name)
        await collection.update_one({"id": user_id}, {"$set": update_data})
        updated_user_data = await collection.find_one({"id": user_id})
        return User(**updated_user_data)

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user from the database."""
        collection = await self.base_db.get_collection(self.collection_name)
        result = await collection.delete_one({"id": user_id})
        return result.deleted_count > 0


user_repository = UserRepository(base_db)
