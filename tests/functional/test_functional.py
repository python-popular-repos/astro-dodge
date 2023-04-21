"""
This file (test_functional.py) contains the functional tests for the database components.
Examples:
* Focus on view components that operate under different conditions.
* Nominal conditions(GET, POST)
* Invalid HTTP methods
* Invalid input data
"""


def test_app_factory_context(app):
    """
    Unit test for the app factory function to ensure that the app's testing and debug properties are set to True.

    Args:
        app: The Flask application instance to be tested.

    Returns:
        None
    """
    assert app.testing is True
    assert app.debug is True


def test_app_factory_client(client):
    """
    Unit test for the app factory function to ensure that the Flask test client's application testing and debug properties
    are set to True.

    Args:
        client: The Flask test client instance to be tested.

    Returns:
        None
    """
    assert client.application.testing is True
    assert client.application.debug is True


def test_index_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"AstroDodge" in response.data
    assert b"<header" in response.data
    assert b"<footer" in response.data


def test_index_page_post(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (POST)
    THEN check that a '405' status code is returned
    """
    response = client.post("/")
    assert response.status_code == 405


def test_about_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/about' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data
    assert b"<header" in response.data
    assert b"<footer" in response.data


def test_about_page_post(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/about' page is requested (POST)
    THEN check that a '405' status code is returned
    """
    response = client.post("/about")
    assert response.status_code == 405


def test_list_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/list' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get("/list")
    assert response.status_code == 200
    assert b"Near Earth Objects" in response.data
    assert b"Closest Approach Date" in response.data
    assert b"Current Distance" in response.data
    assert b"<header" in response.data
    assert b"<footer" in response.data


def test_register_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Confirm" in response.data


def test_register_invalid(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/auth/register' page is posted to (POST) with invalid data (missing password)
    THEN check an error message is returned to the user
    THEN check the page is not redirected
    """
    response = client.post(
        "/auth/register",
        data={
            "email": "test@pytest.com",
            "password": "",
            "confirm": "",
        },  # Empty field is not allowed!
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Confirm" in response.data


def test_register_user(client):
    response = client.post(
        "/auth/register",
        data={"email": "test@pytest.com", "password": "testing", "confirm": "testing"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Profile Page" in response.data
    assert b"No Watchlist Items" in response.data


def test_register_duplicate(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/auth/register' page is posted to (POST) with the email address for an existing user
    THEN check an error message is returned to the user
    """
    client.post(
        "/auth/register",
        data={"email": "test@pytest.com", "password": "testing", "confirm": "testing"},
        follow_redirects=True,
    )

    client.get("/auth/logout", follow_redirects=True)

    response = client.post(
        "/auth/register",
        data={
            "email": "test@pytest.com",  # Duplicate email address
            "password": "testing2",
            "confirm": "testing2",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"has already been registered" in response.data


def test_login_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data


def test_login_invalid(client, register_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/login' page is posted to (POST) with invalid credentials (incorrect password)
    THEN check an error message is returned to the user
    """
    response = client.post(
        "/auth/login",
        data={"email": "test@pytest.com", "password": "incorrect_pw"},  # Incorrect!
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Incorrect login credentials." in response.data


def test_login_when_logged_in_already(client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing and the default user logged in
    WHEN the '/auth/login' page is posted to (POST) with value credentials for the default user
    THEN check a warning is returned to the user (already logged in)
    """
    response = client.post(
        "/auth/login",
        data={"email": "test@pytest.com", "password": "testing"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_logout_invalid(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/auth/logout' page is posted to (POST)
    THEN check that a 405 error is returned
    """
    client.get("/auth/logout", follow_redirects=True)
    response = client.post("/auth/logout", follow_redirects=True)
    assert response.status_code == 405
    assert b"Method Not Allowed" in response.data


def test_list_auth(client, log_in_default_user):
    response = client.get("/auth/list")
    assert response.status_code == 200


def test_list_empty_post(client, log_in_default_user):
    response = client.post("/auth/list", data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Nothing selected to be added to the watchlist" in response.data


def test_profile_auth(client, log_in_default_user):
    response = client.get("/auth/profile")
    assert response.status_code == 200


def test_profile_empty_post(client, log_in_default_user):
    response = client.post("/auth/profile", data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Nothing selected." in response.data