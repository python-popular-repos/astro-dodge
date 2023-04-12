"""
Scope defines WHEN a fixture will be run
1) function - run once per test function (default)
2) class - run once per test class
3) module - run once per module (i.e. test file)
4) session - run once per session (i.e per call to pytest)
"""


import pytest
from app.models import User
from app import create_app, db


# Fixtures for unit testing
@pytest.fixture(scope="module")
def new_user():
    new_user = User("test@pytest.com", "FlaskIsAwesome")
    return new_user


@pytest.fixture(scope="module")
def mock_space_object():
    fake_data = {
        "des": "pytest",
        "orbit_id": "0",
        "jd": "100.1",
        "cd": "2023-Apr-01 00:00",
        "dist": "0.1001",
        "dist_min": "0.0",
        "dist_max": "0.1",
        "v_rel": "10.0",
        "v_inf": "10.1",
        "t_sigma_f": "00:00",
        "h": "100.101",
    }
    return fake_data


# Fixtures for functional testing
@pytest.fixture(scope="module")
def app():
    test_app = create_app("testing")
    test_app.config["WTF_CSRF_ENABLED"] = False  # Flask-WTF Forms
    with test_app.app_context():
        db.create_all()

    yield test_app


@pytest.fixture(scope="module")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="module")
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthorizedActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth_user(client):
    return AuthorizedActions(client)
