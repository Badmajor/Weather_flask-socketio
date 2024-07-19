import pytest


def test_index_get(client_app):
    rv = client_app.get("/")
    assert rv.status_code == 200
    assert "Введите город..." in rv.text
