from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Define validators as constants
email_validators = [DataRequired(), Email(), Length(min=6, max=100)]
password_validators = [DataRequired(), Length(min=6, max=40)]


class RegisterForm(FlaskForm):
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
    email = StringField("Email", validators=email_validators)
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class AstroForm(FlaskForm):
    select = BooleanField(label="Select")
    submit = SubmitField()


class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField("Search")
