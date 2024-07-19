import os
import validators

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()

DEBUG = os.getenv("DEBUG", False) == "True"
WEATHER_URL = os.getenv("WEATHER_URL", "")
SEARCH_CITY_URL = os.getenv("SEARCH_CITY_URL", "")

assert validators.url(
    WEATHER_URL
), "WEATHER_URL не является действительным url"
assert validators.url(
    SEARCH_CITY_URL
), "SEARCH_CITY_URL не является действительным url"

SECRET_KEY = os.getenv("SECRET_KEY", "really-secret-key")

# DATABASE
DATABASE_DIALECT = os.getenv("DATABASE_DIALECT", "postgresql")
DATABASE_DRIVER = os.getenv("DATABASE_DRIVER", "psycopg2")
DATABASE_NAME = os.getenv("POSTGRES_DB", "name")
DATABASE_USER = os.getenv("POSTGRES_USER", "test")
DATABASE_PASS = os.getenv("POSTGRES_PASSWORD", "pass")
DATABASE_HOST = os.getenv("POSTGRES_HOST", "localhost")
DATABASE_PORT = os.getenv("POSTGRES_PORT", 5432)

SQLALCHEMY_DATABASE_URI = URL.create(
    drivername=f"{DATABASE_DIALECT}+{DATABASE_DRIVER}",
    username=DATABASE_USER,
    password=DATABASE_PASS,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    database=DATABASE_NAME,
)

# REDIS
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
