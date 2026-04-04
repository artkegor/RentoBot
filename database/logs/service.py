from datetime import datetime, timedelta

from database.logs.models import Log
from database.logs.repository import LogRepository
from database.logs.repository import log_repository


class LogService:
    """Service class for log-related operations."""

    def __init__(self, log_repository: LogRepository):
        self.log_repository = log_repository

    async def create_log(self, log: Log) -> Log:
        """Create a new log entry in the database."""
        return await self.log_repository.create_log(log)

    async def get_logs_by_action(self, action: str) -> list[Log]:
        """Fetch logs by their action type."""
        return await self.log_repository.get_logs_by_action(action)

    async def get_action_statistics(self) -> dict:
        """Get logs statistics."""

        now = datetime.utcnow()

        day = (now - timedelta(days=1)).timestamp()
        week = (now - timedelta(days=7)).timestamp()
        month = (now - timedelta(days=30)).timestamp()

        search_day = await self.log_repository.count_action_since("search_listings", day)
        search_week = await self.log_repository.count_action_since("search_listings", week)
        search_month = await self.log_repository.count_action_since("search_listings", month)

        contact_day = await self.log_repository.count_action_since("contact_seller", day)
        contact_week = await self.log_repository.count_action_since("contact_seller", week)
        contact_month = await self.log_repository.count_action_since("contact_seller", month)

        return {
            "search": {
                "day": search_day,
                "week": search_week,
                "month": search_month
            },
            "contact": {
                "day": contact_day,
                "week": contact_week,
                "month": contact_month
            }
        }

    async def get_logs_by_user_and_action(self, user_id: int, action: str) -> list[Log]:
        """Fetch logs by user ID and action type."""
        return await self.log_repository.get_log_by_user_and_action(user_id, action)

    async def get_action_statistics_by_month(self) -> list:
        """Return last 12 months logs stats."""

        now = datetime.utcnow()
        result = []

        for i in range(11, -1, -1):
            start = datetime(now.year, now.month, 1) - timedelta(days=30 * i)
            end = datetime(start.year, start.month, 1) + timedelta(days=32)
            end = datetime(end.year, end.month, 1)

            search = await self.log_repository.count_action_between(
                "search_listings",
                start.timestamp(),
                end.timestamp()
            )

            contact = await self.log_repository.count_action_between(
                "contact_seller",
                start.timestamp(),
                end.timestamp()
            )

            result.append({
                "month": start.strftime("%Y-%m"),
                "search": search,
                "contact": contact
            })

        return result


log_service = LogService(log_repository)
