from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db
import nasa as info

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:password@localhost:5432/mydatabase"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html", title="AstroDodge")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/list")
def space_list():
    data = info.format()
    return render_template("list.html", space_list=data, title="Space List")


@app.route("/login")
def login():
    return render_template("login.html", title="Login")


@app.route("/register")
def register():
    return render_template("register.html", title="Register")


@app.route("/profile")
def profile():
    return render_template("profile.html", title="Profile")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
