"""
This file (test_endpoints.py) contains the functional tests for the routing components.
Examples:
* Focus on view components that operate under different conditions.
* Nominal conditions(GET, POST)
* Invalid HTTP methods
* Invalid input data
"""


def test_index_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"AstroDodge" in response.data


def test_index_page_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post("/")
    assert response.status_code == 405


def test_about_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/about' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data


def test_about_page_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/about' page is requested (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post("/about")
    assert response.status_code == 405


def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data


# def test_login_page_post(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' page is requested (POST)
#     THEN check the response is valid
#     """
#     response = test_client.post("/login")
#     assert response.status_code == 200


def test_register_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Confirm" in response.data


# def test_register_page_post(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' page is requested (POST)
#     THEN check the response is valid
#     """
#     response = test_client.post("/register")
#     assert response.status_code == 200
