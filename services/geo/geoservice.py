import requests
from config import config
from logging_config import logger


def get_normalized_address_and_coordinates(address):
    """Get geographical coordinates (latitude and longitude) for a given address using Yandex Maps API."""
    api_key = config.YANDEX_MAPS_API_KEY
    url = f"http://geocode-maps.yandex.ru/1.x/?format=json&apikey={api_key}&geocode={address}"
    response = requests.get(url).json()
    try:
        geo_object = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        normalized_address = geo_object['metaDataProperty']['GeocoderMetaData']['text']
        pos = geo_object['Point']['pos'].split()
        longitude, latitude = map(float, pos)
        return normalized_address, latitude, longitude
    except (IndexError, KeyError):
        logger.error(f"Failed to get coordinates for address: {address}")
        logger.error(f"Yandex Maps API response: {response}")
        return None, None, None
