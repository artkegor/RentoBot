from database.listings.service import listing_service
from database.logs.service import log_service
from database.users.service import user_service


def stats_parser():
    """Parse and print statistics about users, listings, and logs."""
    import asyncio

    async def gather_stats():
        total_users = await user_service.count_users()
        total_listings = await listing_service.count_listings()
        total_logs = await log_service.count_logs()

        print(f"Total Users: {total_users}")
        print(f"Total Listings: {total_listings}")
        print(f"Total Logs: {total_logs}")

    asyncio.run(gather_stats())
