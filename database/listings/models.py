from typing import List, Optional
from pydantic import BaseModel, Field


class Listing(BaseModel):
    """ Model representing a listing."""
    listing_id: str = Field(..., description="Уникальный идентификатор объявления")
    user_id: int = Field(..., description="Идентификатор пользователя, создавшего объявление")

    created_at: str = Field(..., description="Временная метка создания объявления")
    finished_at: str = Field(..., description="Временная метка завершения объявления (продано/арендовано)")

    title: str = Field(..., description="Заголовок объявления")
    description: str = Field(..., description="Описание объявления")

    item_type: str = Field(..., description="Тип объявления: товар или услуга")
    transaction_type: str = Field(..., description="Тип транзакции: продажа или аренла")

    is_active: bool = Field(..., description="Статус объявления: активно (True) или продано/арендовано (False)")

    tags: List[str] = Field(..., description="Список тегов объявления")

    price: float = Field(
        None,
        description="Цена товара"
    )

    duration: Optional[str] = Field(
        None,
        description="Срок аренды (только для rent)"
    )

    place: str = Field(..., description="Текстовое описание локации")
    location: dict = Field(..., description="GeoJSON location")

    photos: List[str] = Field(
        default_factory=list,
        description="Список file_id фотографий"
    )

    score: Optional[int] = None
