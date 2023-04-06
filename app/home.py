from flask import Blueprint, render_template, request
from app.models import SpaceRecord
from app.forms import ExampleForm
from app import db
from flask_login import current_user

# Blueprint Configuration
home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="AstroDodge")


@home_bp.route("/about", methods=["GET"])
def about():
    return render_template("about.html", title="About")


@home_bp.route("/list", methods=["GET", "PUT"])
def space_list():
    form = ExampleForm()
    # populate the forms dynamically with the choices in the database
    stmt = db.select(SpaceRecord)
    # query = db.session.execute(stmt).scalars()
    query = SpaceRecord.query.all()
    print(query)
    form.choices.choices, cool = [a.designation for a in query], [a for a in query]
    # if it's a post request and we validated successfully
    if request.method == "POST" and form.validate_on_submit():
        # get our choices again, could technically cache these in a list if we wanted but w/e
        c_records = query
        test = 0
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
        toggle = "" if current_user.is_authenticated else ""  # type: ignore

        return render_template(
        "list.html", space_list=query, title="Space List", toggle=toggle, form=form
    )

    # form = AstroForm()
    # if current_user.is_authenticated:  # type: ignore
    #     record = SpaceRecord.query.all()
    # else:
    #     record = SpaceRecord.query.limit(5).all()

    # toggle = "" if current_user.is_authenticated else "disabled"  # type: ignore

    # return render_template(
    #     "list.html", space_list=record, title="Space List", toggle=toggle, form=form
    # )


# user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()
