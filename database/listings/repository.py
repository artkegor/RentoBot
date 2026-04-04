from typing import Iterable
from database.base import base_db
from database.listings.models import Listing
from datetime import datetime, timedelta


class ListingRepository:
    """Repository class for listing-related database operations."""

    def __init__(self, base_db):
        self.base_db = base_db
        self.collection_name = "listings"

    async def get_collection(self) -> any:
        """Get the listings collection from the database."""
        return await self.base_db.get_collection(self.collection_name)

    async def get_listing_by_id(self, listing_id: str) -> Listing | None:
        """Fetch a listing by its unique ID."""
        collection = await self.base_db.get_collection(self.collection_name)
        listing_data = await collection.find_one({"listing_id": listing_id})
        if listing_data:
            return Listing(**listing_data)
        return None

    async def create_listing(self, listing: Listing) -> Listing:
        """Create a new listing in the database."""
        collection = await self.base_db.get_collection(self.collection_name)
        await collection.insert_one(listing.dict())
        return listing

    async def update_listing(self, listing_id: str, update_data: dict) -> Listing:
        """Update an existing listing's information."""
        collection = await self.base_db.get_collection(self.collection_name)
        await collection.update_one({"listing_id": listing_id}, {"$set": update_data})
        updated_listing_data = await collection.find_one({"listing_id": listing_id})
        return Listing(**updated_listing_data)

    async def delete_listing(self, listing_id: str) -> bool:
        """Delete a listing from the database."""
        collection = await self.base_db.get_collection(self.collection_name)
        result = await collection.delete_one({"listing_id": listing_id})
        return result.deleted_count > 0

    async def get_recent_listings(self, limit: int = 10, listing_type: str = "all") -> list[Listing]:
        """Fetch recent listings from the database."""
        collection = await self.get_collection()

        if listing_type in ["sale", "rent"]:
            cursor = (
                collection
                .find({'is_active': True, 'transaction_type': listing_type})
                .sort("_id", -1)
                .limit(limit)
            )
            return [Listing(**doc) async for doc in cursor]
        else:
            cursor = (
                collection
                .find({'is_active': True})
                .sort("_id", -1)
                .limit(limit)
            )
            return [Listing(**doc) async for doc in cursor]

    async def get_nearest_listings(
            self,
            latitude: float,
            longitude: float,
            listing_type: str = "all",
            limit: int = 20,
            max_distance_km: float = 50
    ) -> list[Listing]:

        collection = await self.get_collection()

        pipeline = [
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": [longitude, latitude]
                    },
                    "distanceField": "distance",
                    "distanceMultiplier": 0.001,
                    "maxDistance": max_distance_km * 1000,
                    "spherical": True,
                    "query": {"is_active": True} if listing_type == "all" else {"is_active": True,
                                                                                "transaction_type": listing_type}
                }
            },
            {"$limit": limit}
        ]

        cursor = collection.aggregate(pipeline)

        listings = []
        async for doc in cursor:
            listings.append(Listing(**doc))

        return listings

    async def search_by_tags(self, query_tags: Iterable[str], limit: int = 20, listing_type: str = "all") -> list[
        Listing]:
        """
        Mongo search using $in on tags.
        """
        collection = await self.get_collection()
        cursor = collection.find(
            {"tags": {"$in": list(query_tags)}, "is_active": True} if listing_type == "all" else {
                "tags": {"$in": list(query_tags)}, "is_active": True, "transaction_type": listing_type},
            limit=limit
        )

        listings = []
        async for doc in cursor:
            listings.append(Listing(**doc))

        return listings

    async def count_created_since(self, since_timestamp: float) -> int:
        """Count listings created since timestamp."""
        collection = await self.get_collection()

        return await collection.count_documents({
            "created_at": {"$gte": str(since_timestamp)}
        })

    async def count_finished_since(self, since_timestamp: float) -> int:
        """Count finished listings since timestamp."""
        collection = await self.get_collection()

        return await collection.count_documents({
            "finished_at": {"$gte": str(since_timestamp)}
        })

    async def count_created_between(self, start: float, end: float) -> int:
        collection = await self.get_collection()

        return await collection.count_documents({
            "created_at": {
                "$gte": str(start),
                "$lt": str(end)
            }
        })

    async def count_finished_between(self, start: float, end: float) -> int:
        collection = await self.get_collection()

        return await collection.count_documents({
            "finished_at": {
                "$gte": str(start),
                "$lt": str(end)
            }
        })


listing_repository = ListingRepository(base_db)
