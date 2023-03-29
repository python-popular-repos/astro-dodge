from flask import Flask, render_template, flash, request, redirect, url_for
from forms import RegisterForm
from flask_login import current_user, login_required, login_user, logout_user
from models import db, User
import nasa as information

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")
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
    data = information.format()
    return render_template("list.html", space_list=data, title="Space List")


@app.route("/login")
def login():
    return render_template("login.html", title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    # if current_user.is_authenticated:  # type: ignore
    #     flash("Already Registed, redirecting to profile page.")
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        new_user = User(form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("profile"))

    return render_template("register.html", form=form, title="Register")


@app.route("/profile")
def profile():
    return render_template("profile.html", title="Profile")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
