from flask import Blueprint, render_template, request, flash
from app.models import SpaceRecord
from app.forms import AstroForm
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


@home_bp.route("/list", methods=["GET", "POST"])
def space_list():
    form = AstroForm()

    if current_user.is_authenticated:  # type: ignore
        stmt = db.select(SpaceRecord)
        toggle = ""
    else:
        stmt = db.select(SpaceRecord).limit(5)
        toggle = "disabled"

    query = db.session.execute(stmt).scalars()

    if request.method == "POST" and form.validate_on_submit():
        selected_items = []
        records = request.form.getlist("select")
        for item in records:
            selected_items.append(item)
        flash(f"Added {selected_items}")

        return render_template(
            "list.html", space_list=query, title="Space List", toggle=toggle, form=form
        )

    return render_template(
        "list.html", space_list=query, title="Space List", toggle=toggle, form=form
    )
