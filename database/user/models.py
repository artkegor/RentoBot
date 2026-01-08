from pydantic import BaseModel, Field


class User(BaseModel):
    """Data model representing a user."""
    id: int = Field(..., description="The unique identifier for the user")
    username: str = Field(..., description="The username of the user")
    phone_number: str = Field(..., description="The phone number of the user")
    rating: float = Field(..., description="The user's rating")
    reviews: list = Field(default_factory=list, description="List of user's reviews")
    listings: list = Field(default_factory=list, description="List of user's listings")
