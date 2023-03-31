"""
This file (test_models.py) contains the unit tests for the models.py file.
Examples:
* Focus on testing small units of code in isolation 
  (ie database models, utility functions)
"""


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """
    assert new_user.password_hashed != "FlaskIsAwesome"
    assert new_user.__repr__() == "<User: test@pytest.com>"
    assert new_user.is_authenticated
    assert new_user.is_active
    assert not new_user.is_anonymous


def test_setting_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user.set_password("MyNewPassword")
    assert new_user.password_hashed != "MyNewPassword"
    assert new_user.is_password_correct("MyNewPassword")
    assert not new_user.is_password_correct("MyNewPassword2")
    assert not new_user.is_password_correct("FlaskIsAwesome")


def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 66
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == "66"
