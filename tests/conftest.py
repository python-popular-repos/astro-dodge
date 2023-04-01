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


# Fixtures for functional testing
@pytest.fixture(scope="module")
def test_client():
    test_app = create_app()
    with test_app.test_client() as testing_client:
        yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    # Create the database and the database table
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
