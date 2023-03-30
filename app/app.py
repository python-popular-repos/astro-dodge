from flask import Flask, render_template, flash, request, redirect, url_for
from forms import RegisterForm, LoginForm
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
    LoginManager,
)
from flask_wtf.csrf import CSRFProtect
from models import db, User
import nasa as information

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
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


@app.route("/list", methods=["GET", "POST"])
def space_list():
    data = information.format()
    return render_template("list.html", space_list=data, title="Space List")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.is_password_correct(form.password.data):
                flash(f"Thanks for logging in, {user.email}!")
                return redirect(url_for("profile"))

        flash("ERROR! Incorrect login credentials.")

    return render_template("login.html", form=form, title="Login")


@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        new_user = User(form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("profile"))

    return render_template("register.html", form=form, title="Register")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile")


@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
