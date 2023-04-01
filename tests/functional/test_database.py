"""
This file (test_database.py) contains the functional tests for the database components.
Examples:
* Focus on view components that operate under different conditions.
* Nominal conditions(GET, POST)
* Invalid HTTP methods
* Invalid input data
"""


def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post(
        "/login",
        data=dict(email="test@pytest.com", password="FlaskIsAwesome"),
        follow_redirects=True,
    )
    assert response.status_code == 400

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200


def test_invalid_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post(
        "/login",
        data=dict(email="test@pytest.com", password="FlaskIsNotAwesome"),
        follow_redirects=True,
    )
    assert response.status_code == 400
