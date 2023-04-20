"""
Scope defines WHEN a fixture will be run
1) function - run once per test function (default)
2) class - run once per test class
3) module - run once per module (i.e. test file)
4) session - run once per session (i.e per call to pytest)
"""


import pytest
from app.models import User, Record, SpaceRecord, SpaceObject
from app import create_app, db


# Fixtures for unit testing
@pytest.fixture(scope="module")
def new_user():
    app = create_app("testing")

    # Establish an application context before creating the User object
    with app.app_context():
        user = User(email="test@pytest.com", password_plaintext="testing")
        yield user


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
    """Create and configure a new app instance for each test. Including app setup and teardown."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="module")
def client():
    """Created test client with setup and teardown. Will be used for most tests."""
    flask_app = create_app("testing")
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context before accessing the logger and database
        with flask_app.app_context():
            flask_app.logger.info("Creating database tables in test_client fixture...")
            db.create_all()
        yield testing_client
        with flask_app.app_context():
            db.drop_all()


@pytest.fixture(scope="module")
def register_default_user(client):
    # Register the default user
    client.post(
        "/auth/register",
        data={"email": "test@pytest.com", "password": "testing", "confirm": "testing"},
        follow_redirects=True,
    )
    client.get("/auth/logout", follow_redirects=True)
    return


@pytest.fixture(scope="function")
def log_in_default_user(client, register_default_user):
    # Log in the default user
    client.post(
        "/auth/login",
        data={"email": "test@pytest.com", "password": "testing"},
        follow_redirects=True,
    )
    yield
    # Log out the default user
    client.get("/auth/logout", follow_redirects=True)


@pytest.fixture(scope="module")
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
