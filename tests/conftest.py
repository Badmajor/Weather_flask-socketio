import pytest

from app_tools import app


@pytest.fixture
def client_app():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
