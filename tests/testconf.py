import pytest
from app.models import User, Record


# Fixtures
@pytest.fixture(scope="module")
def new_user():
    user = User("test@pytest.com", "FlaskIsAwesome")
    return user
