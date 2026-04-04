from datetime import datetime, timedelta

from database.users.models import User
from database.users.repository import UserRepository
from database.users.repository import user_repository


class UserService:
    """Service class for users-related operations."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user(self, id: int) -> bool:
        """Check if a users exists in the database."""
        existing_user = await self.user_repository.get_user_by_id(id)
        return existing_user if existing_user else False

    async def register_user(self, user: User) -> User:
        """Register a new users in the database."""
        return await self.user_repository.create_user(user)

    async def add_listing_to_user(self, user_id: int, listing_id: str) -> User | None:
        """Add a listing ID to the users's listings."""
        user = await self.user_repository.get_user_by_id(user_id)
        if user:
            user.listings.append(listing_id)
            updated_user = await self.user_repository.update_user(user_id, {"listings": user.listings})
            return updated_user
        return None

    async def delete_listing_from_user(self, user_id: int, listing_id: str) -> User | None:
        """Remove a listing ID from the users's listings."""
        user = await self.user_repository.get_user_by_id(user_id)
        if user and listing_id in user.listings:
            user.listings.remove(listing_id)
            updated_user = await self.user_repository.update_user(user_id, {"listings": user.listings})
            return updated_user
        return None

    async def update_username(self, user_id: int, username: str) -> User | None:
        """Update the users's username."""
        user = await self.user_repository.get_user_by_id(user_id)
        if user:
            user.username = username
            updated_user = await self.user_repository.update_user(user_id, {"username": username})
            return updated_user
        return None

    async def get_registration_statistics(self) -> dict:
        """Get user registration statistics."""

        now = datetime.utcnow()

        day = (now - timedelta(days=1)).timestamp()
        week = (now - timedelta(days=7)).timestamp()
        month = (now - timedelta(days=30)).timestamp()

        users_day = await self.user_repository.count_users_since(day)
        users_week = await self.user_repository.count_users_since(week)
        users_month = await self.user_repository.count_users_since(month)

        return {
            "day": users_day,
            "week": users_week,
            "month": users_month
        }

    async def update_location(self, user_id: int, latitude: float, longitude: float) -> User | None:
        """Update the users's location."""
        user = await self.user_repository.get_user_by_id(user_id)
        if user:
            user.latitude = latitude
            user.longitude = longitude
            updated_user = await self.user_repository.update_user(user_id,
                                                                  {"latitude": latitude, "longitude": longitude})
            return updated_user
        return None

    async def get_registration_statistics_by_month(self) -> list:
        """Return last 12 months user registrations."""

        now = datetime.utcnow()
        result = []

        for i in range(11, -1, -1):
            start = datetime(now.year, now.month, 1) - timedelta(days=30 * i)
            end = datetime(start.year, start.month, 1) + timedelta(days=32)
            end = datetime(end.year, end.month, 1)

            count = await self.user_repository.count_users_between(
                start.timestamp(),
                end.timestamp()
            )

            result.append({
                "month": start.strftime("%Y-%m"),
                "count": count
            })

        return result


user_service = UserService(user_repository)
