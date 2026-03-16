from pydantic import BaseModel, Field


class User(BaseModel):
    """Data model representing a users."""
    id: int = Field(..., description="The unique identifier for the users")
    created_at: str = Field(..., description="Временная метка регистрации пользователя")

    username: str = Field(..., description="The username of the users")
    phone_number: str = Field(..., description="The phone number of the users")

    latitude: float = Field(0.0, description="The latitude of the users's location")
    longitude: float = Field(0.0, description="The longitude of the users's location")

    rating: float = Field(..., description="The users's rating")
    reviews: list = Field(default_factory=list, description="List of users's reviews")
    listings: list = Field(default_factory=list, description="List of users's listings")
