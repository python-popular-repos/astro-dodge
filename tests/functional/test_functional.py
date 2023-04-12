"""
This file (test_functional.py) contains the functional tests for the database components.
Examples:
* Focus on view components that operate under different conditions.
* Nominal conditions(GET, POST)
* Invalid HTTP methods
* Invalid input data
"""


def test_app_factory(client):
    assert client.application.testing == True
    assert client.application.debug == True


def test_index_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"AstroDodge" in response.data


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


def test_login_profile(client, auth_user):
    """
    GIVEN a Flask application with an authorized user
    WHEN the user is logged in assert the redirect count is 1
    THEN check that user is able to access the "/profile" route
    THEN check the response is valid
    """
    response = auth_user.login()
    assert response.status_code == 200

    with client:
        client.get("/auth/profile")
        assert response.status_code == 200


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


def test_logout(client, auth_user):
    """
    GIVEN a Flask application configured with an authorized user
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    WHEN the '/logout' page is requested (GET)
    THEN check the page has been redirected to home page ('/')
    """
    auth_user.login()
    response = client.get("/auth/profile")
    assert response.status_code == 200

    with client:
        auth_user.logout()
        response = client.get("/")


def test_auth_profile(client, auth_user):
    """
    GIVEN a Flask application configured with an authorized user
    WHEN the '/auth/profile' page is requested (GET)
    THEN check the response is valid
    """
    auth_user.login()
    response = client.get("/auth/profile")
    assert response.status_code == 200


def test_auth_list(client, auth_user):
    """
    GIVEN a Flask application configured with an authorized user
    WHEN the '/auth/list' page is requested (GET)
    THEN check the response is valid
    """
    auth_user.login()
    response = client.get("/auth/list")
    assert response.status_code == 200
