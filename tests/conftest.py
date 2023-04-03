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
def test_client():
    test_app = create_app()
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    db.drop_all()
    db.create_all()

    # Insert user data
    user1 = User(email="test@pytest.com", password_plaintext="FlaskIsAwesome")
    user2 = User(email="test@pytest.c0m", password_plaintext="Flask1sAwesome")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    yield

    db.drop_all()


@pytest.fixture(scope="function")
def login_default_user(test_client):
    test_client.post(
        "/login",
        data=dict(email="test@pytest.com", password="FlaskIsAwesome"),
        follow_redirects=True,
    )

    yield

    test_client.get("/logout", follow_redirects=True)
