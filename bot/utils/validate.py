from services.geo.geoservice import get_normalized_address_and_coordinates
from bot.utils.memory import form_memory


def validate_place_input(answer: str) -> tuple[str, float, float]:
    """Validate the place input and get normalized address and coordinates."""
    normalized_address, latitude, longitude = get_normalized_address_and_coordinates(answer)
    return normalized_address, latitude, longitude


def validate_price_input(answer: str) -> float:
    """Validate the price input to ensure it's a positive float."""
    price = float(answer)
    if price < 0:
        raise ValueError("Price must be a positive number.")
    return price


def validate_final_confirmation_input(user_id: int) -> tuple[str, list[str]]:
    """Validate and prepare the final confirmation message for the listing."""
    data = form_memory.get_answers(
        user_id=user_id,
        form='create_listing'
    )
    text = ("📋 Проверьте объявление перед публикацией:\n\n"
            f"🏷 Название: {data.get('listing_title')}\n"
            f"📝 Описание: {data.get('listing_description')}\n"
            f"📍 Местоположение: {data.get('listing_place')}\n"
            f"💰 Цена: {data.get('listing_price')}₽\n"
            )
    if data.get('listing_duration'):
        text += (f"⏳ Длительность аренды: {data.get('listing_duration')}\n")
    photos = data.get('listing_photo') or []

    return text, photos


def validate_listing_text(listing) -> str:
    """Generate a formatted text representation of a listing."""
    price_info = f"Цена: {listing.price}₽"
    if listing.transaction_type == 'rent':
        price_info += f"\nДлительность аренды: {listing.duration}"

    text = (f"🏷 <b>{listing.title}</b>\n\n"
            f"{price_info}\n\n"
            f"📝 {listing.description}\n\n"
            f"📍 Местоположение: {listing.place}\n"
            f"🆔 ID объявления: {listing.listing_id}")

    return text
