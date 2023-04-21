from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Define validators as constants
email_validators = [DataRequired(), Email(), Length(min=6, max=100)]
password_validators = [DataRequired(), Length(min=6, max=40)]


class RegisterForm(FlaskForm):
    """
    Form for user registration.

    Attributes:
    email (StringField): Email address of the user.
    password (PasswordField): Password of the user.
    confirm (PasswordField): Password confirmation field.
    submit (SubmitField): Submit button to create the user.
    """
    email = StringField("Email", validators=email_validators)
    password = PasswordField("Password", validators=password_validators)
    confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Create")


class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
    email (StringField): Email address of the user.
    password (PasswordField): Password of the user.
    remember_me (BooleanField): Checkbox to remember the user.
    submit (SubmitField): Submit button to log in.
    """
    email = StringField("Email", validators=email_validators)
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class AstroForm(FlaskForm):
    """
    Form for selecting an AstroRecord object on the watchlist.

    Attributes:
    select (BooleanField): Checkbox to select the object.
    submit (SubmitField): Submit button to confirm the selection.
    """
    select = BooleanField(label="Select")
    submit = SubmitField()


class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField("Search")
