from flask import Blueprint, render_template
from app.models import SpaceRecord
from app.forms import AstroForm
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
    form = AstroForm()
    if current_user.is_authenticated:  # type: ignore
        record = SpaceRecord.query.all()
    else:
        record = SpaceRecord.query.limit(5).all()

    toggle = "" if current_user.is_authenticated else "disabled"  # type: ignore

    return render_template(
        "list.html", space_list=record, title="Space List", toggle=toggle, form=form
    )


# user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()
