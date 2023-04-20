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
    """Create and configure a new app instance for each test."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def auth_user(client):
    """A test user that is logged in."""
    with app.app_context():
        from app.models import User

        user = User(email="testing@pytest.com", password_plaintext="testing")
        db.session.add(user)
        db.session.commit()

        client.post(
            "/auth/login", data={"email": "testing@pytest.com", "password": "testing"}
        )

        yield user

        client.get("/logout")
