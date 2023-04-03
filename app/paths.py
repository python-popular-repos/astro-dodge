from flask import Blueprint, render_template
import app.nasa as information

# Blueprint Configuration
home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="AstroDodge")


@home_bp.route("/about", methods=["GET"])
def about():
    return render_template("about.html", title="About")


@home_bp.route("/list", methods=["GET"])
def space_list():
    data = information.format_space_object()
    return render_template("list.html", space_list=data, title="Space List")
