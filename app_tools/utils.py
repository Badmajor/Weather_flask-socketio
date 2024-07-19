from datetime import datetime

from app_tools import db
from app_tools.constatnts import weather_icons
from app_tools.database.models import City, Country, User, UsersCities
from app_tools.database.utils import get_or_create


def get_icon(weather_code: int) -> str:
    """Метод возвращает иконку в зависимости от кода погоды."""
    if weather_code in weather_icons.keys():
        return weather_icons[weather_code]
    return ""


def record_data(user: str, location: dict):
    """Метод записывает историю поиска и меняет время для UserCities"""
    city = location.get("city")
    county = location.get("country")
    country_obj, _ = get_or_create(Country, name=county)
    city_obj, _ = get_or_create(City, name=city, country=country_obj)
    user_obj, _ = get_or_create(User, user_session=user)
    user_city, _ = get_or_create(UsersCities, user=user_obj, city=city_obj)
    user_city.created_at = datetime.now()
    city_obj.count += 1
    db.session.commit()
