from flask import request, render_template
from app import db
from app.models import SpaceRecord
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    SelectMultipleField,
    widgets,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=100)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Create")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=100)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class AstroForm(FlaskForm):
    select = SubmitField(label="Add record")
    item = StringField("Astro", validators=[DataRequired()])


class CheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ExampleForm(FlaskForm):
    choices = CheckboxField("Astro", coerce=str)
    submit = SubmitField(label="Submit Choices")


def example():
    form = ExampleForm()
    # populate the forms dynamically with the choices in the database
    stmt = db.Select(SpaceRecord)
    query = db.session.execute(stmt).scalars()
    form.check_options.choices = [a.designation for a in query]
    # if it's a post request and we validated successfully
    if request.POST and form.validate_on_submit():
        # get our choices again, could technically cache these in a list if we wanted but w/e
        c_records = query
        # need a list to hold our choices
        accepted = []
        # looping through the choices, we check the choice ID against what was passed in the form
        for choice in c_records:
            # when we find a match, we then append the Choice object to our list
            if choice.id in form.check_options.data:
                accepted.append(choice)
        # now all we have to do is update the users choices records
        x = 0
        x = 1
    else:
        # tell the form what's already selected
        toggle = "" if current_user.is_authenticated else "disabled"  # type: ignore

        return render_template(
        "list.html", space_list=query, title="Space List", toggle=toggle, form=form
    )

if __name__ == "__main__":
    example()