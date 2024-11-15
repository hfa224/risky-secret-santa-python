""" configure test fixtures """

import os
import tempfile

import pytest
from secret_santa import create_app
from secret_santa.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "test_data/user_data.sql"), "rb") as f:
    _user_data_sql = f.read().decode("utf8")

@pytest.fixture(name="app")
def fixture_app():
    """provide test app"""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_user_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(name="client")
def fixture_client(app):
    """Provide test client"""
    return app.test_client()


@pytest.fixture(name="runner")
def fixture_runner(app):
    """Provide test runner"""
    return app.test_cli_runner()


class AuthActions:
    """Class mocking auth actions"""

    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        """call fixture client login endpoint"""
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        """call fixture client logout endpoint"""
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    """provide auth endpoint"""
    return AuthActions(client)
