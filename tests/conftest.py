"""
Scope defines WHEN a fixture will be run
1) function - run once per test function (default)
2) class - run once per test class
3) module - run once per module (i.e. test file)
4) session - run once per session (i.e per call to pytest)
"""


import pytest
from app.models import User


# Fixtures
@pytest.fixture
def new_user():
    new_user = User("test@pytest.com", "FlaskIsAwesome")
    return new_user
