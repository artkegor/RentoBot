from datetime import datetime, timedelta

from services.tags.tags_extractor import generate_tags
from services.geo.maths import haversine_distance

from database.listings.models import Listing
from database.listings.repository import ListingRepository
from database.listings.repository import listing_repository


class ListingService:
    """Service class for listing-related operations."""

    def __init__(self, listing_repository: ListingRepository):
        self.listing_repository = listing_repository

    async def create_listing(self, listing: Listing) -> Listing:
        """Create a new listing in the database."""
        return await self.listing_repository.create_listing(listing)

    async def get_listing(self, listing_id: str) -> Listing | None:
        """Fetch a listing by its unique ID."""
        return await self.listing_repository.get_listing_by_id(listing_id)

    async def delete_listing(self, listing_id: str) -> bool:
        """Delete a listing from the database."""
        return await self.listing_repository.delete_listing(listing_id)

    async def get_recent_listings(self, limit: int = 10, listing_type: str = "all") -> list[Listing]:
        """Fetch recent listings from the database."""
        return await self.listing_repository.get_recent_listings(limit, listing_type)

    async def search_listings(self, query: str, latitude: float, longitude: float, listing_type: str = "all",
                              limit: int = 20,
                              min_score: int = 1) -> list[Listing]:
        """Search for listings based on a query and tags."""
        tags = set(generate_tags(text=query, top_n=10))

        listings = await self.listing_repository.search_by_tags(
            query_tags=tags,
            limit=limit,
            listing_type=listing_type
        )

        results = []
        for listing in listings:
            listing_tags = set(listing.tags)
            score = len(tags & listing_tags)

            if score >= min_score:
                coords = listing.location.get("coordinates", [0, 0])
                listing_lon, listing_lat = coords

                distance = haversine_distance(
                    latitude, longitude,
                    listing_lat, listing_lon
                )

                listing.score = score
                listing.distance = distance
                results.append(listing)

        results.sort(key=lambda x: (-x.score, x.distance))
        return results

    async def get_nearest_listings(
            self,
            latitude: float,
            longitude: float,
            listing_type: str = "all",
            limit: int = 20
    ) -> list[Listing]:

        return await self.listing_repository.get_nearest_listings(
            latitude=latitude,
            longitude=longitude,
            listing_type=listing_type,
            limit=limit
        )

    async def update_listing_status(self, listing_id: str, is_active: bool) -> Listing:
        """Update the active status of a listing."""
        return await self.listing_repository.update_listing(
            listing_id=listing_id,
            update_data={"is_active": is_active}
        )

    async def set_finished_at(self, listing_id: str, finished_at: str) -> Listing:
        """Set the finished_at timestamp for a listing."""
        return await self.listing_repository.update_listing(
            listing_id=listing_id,
            update_data={"finished_at": finished_at}
        )

    async def get_listing_statistics(self) -> dict:
        """Get listing statistics."""

        now = datetime.utcnow()

        day = (now - timedelta(days=1)).timestamp()
        week = (now - timedelta(days=7)).timestamp()
        month = (now - timedelta(days=30)).timestamp()

        created_day = await self.listing_repository.count_created_since(day)
        created_week = await self.listing_repository.count_created_since(week)
        created_month = await self.listing_repository.count_created_since(month)

        finished_day = await self.listing_repository.count_finished_since(day)
        finished_week = await self.listing_repository.count_finished_since(week)
        finished_month = await self.listing_repository.count_finished_since(month)

        return {
            "created": {
                "day": created_day,
                "week": created_week,
                "month": created_month
            },
            "finished": {
                "day": finished_day,
                "week": finished_week,
                "month": finished_month
            }
        }

    async def get_listing_statistics_by_month(self) -> list:
        """Return last 12 months listing stats."""

        now = datetime.utcnow()
        result = []

        for i in range(11, -1, -1):
            start = datetime(now.year, now.month, 1) - timedelta(days=30 * i)
            end = datetime(start.year, start.month, 1) + timedelta(days=32)
            end = datetime(end.year, end.month, 1)

            created = await self.listing_repository.count_created_between(
                start.timestamp(),
                end.timestamp()
            )

            finished = await self.listing_repository.count_finished_between(
                start.timestamp(),
                end.timestamp()
            )

            result.append({
                "month": start.strftime("%Y-%m"),
                "created": created,
                "finished": finished
            })

        return result


listing_service = ListingService(listing_repository)
