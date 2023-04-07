from flask import Blueprint, render_template, request
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
    stmt = db.select(SpaceRecord)
    query = db.session.execute(stmt).scalars()
    form.items = query

    if request.method == "POST" and form.validate_on_submit():
        selected_items = []
        test = request
        for item in form.items:
            if item.designation:
                selected_items.append(item.id)
    else:
        toggle = "" if current_user.is_authenticated else ""  # type: ignore

        return render_template(
        "list.html", space_list=query, title="Space List", toggle=toggle, form=form
    )
