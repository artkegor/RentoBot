from database.user.models import User
from database.user.repository import UserRepository
from database.user.repository import user_repository


class UserService:
    """Service class for user-related operations."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def check_if_user_exists(self, id: int) -> bool:
        """Check if a user exists in the database."""
        existing_user = await self.user_repository.get_user_by_id(id)
        return existing_user is not None

    async def register_user(self, user: User) -> User:
        """Register a new user in the database."""
        return await self.user_repository.create_user(user)


user_service = UserService(user_repository)
