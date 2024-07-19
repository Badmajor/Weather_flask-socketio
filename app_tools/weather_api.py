import openmeteo_requests

import requests

import requests_cache
from retry_requests import retry

from .config import SEARCH_CITY_URL, WEATHER_URL
from .utils import get_icon

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_cities(query: str) -> list:
    url = SEARCH_CITY_URL
    params = {"name": query, "language": "ru"}
    response = requests.get(url, params=params)
    qs = [item.get("name") for item in response.json().get("results", [])]
    return qs


def get_coords(city_name: str, count: int = 1) -> dict:
    """Метод получает координаты города"""
    url = SEARCH_CITY_URL
    params = {"name": city_name, "count": count, "language": "ru"}
    response = requests.get(url, params=params)
    data = response.json()
    if result := data.get("results", None):
        return {
            "result": {
                "latitude": result[0].get("latitude"),
                "longitude": result[0].get("longitude"),
                "city": result[0].get("name"),
                "country": result[0].get("country"),
            }
        }

    return {"result": None}


def get_weather(city: str):
    """Получает и сериализует данные о погоде в городе"""
    url = WEATHER_URL
    coords = get_coords(city)
    if not (result := coords.get("result", None)):
        return coords
    city = result.pop("city")
    country = result.pop("country")
    params = {
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation_probability",
            "weather_code",
        ],
        **result,
    }
    responses = openmeteo.weather_api(url, params=params)
    weather_current = responses[0]
    return {
        "result": {
            "temperature": f"{weather_current.Current().Variables(0).Value():.2f} C°",
            "humidity": f"{weather_current.Current().Variables(1).Value()} %",
            "precipitation_probability": f"{weather_current.Current().Variables(2).Value()} %",
            "weather_icon": get_icon(
                weather_current.Current().Variables(3).Value()
            ),
        },
        "location": {
            "city": city,
            "country": country,
        },
    }
