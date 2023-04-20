"""
This file (test_functional.py) contains the functional tests for the database components.
Examples:
* Focus on view components that operate under different conditions.
* Nominal conditions(GET, POST)
* Invalid HTTP methods
* Invalid input data
"""


def test_app_factory_context(app):
    assert app.testing is True
    assert app.debug is True


def test_app_factory_client(client):
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


def test_register(client):
    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register",
        data={"email": "test@pytest.com", "password": "testing"},
    )
    x = 0
    assert client.get("/auth/profile").status_code == 200


def test_login_auth(client, auth):
    """
    GIVEN a Flask application with an authorized user
    WHEN the user is logged in
    THEN check that user is able to access the "/auth/profile" route
    AND check the response is valid
    """
    auth.login()
    with client:
        response = client.get("/auth/profile")
        assert response.status_code == 200


def test_logout_auth(client, auth):
    """
    GIVEN a Flask application configured with a logged in authorized user
    WHEN the '/logout' page is requested (GET)
    THEN check the user_id is not recorded in the session object
    """
    from flask import session

    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
