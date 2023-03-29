from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime
import nasa

app = Flask(__name__)
data = nasa.format()

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:password@localhost:5432/mydatabase"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)


@app.before_first_request
def create_tables():
    print("Hopefully Creating Tables")
    db.create_all()


class User(db.Model):
    __tablename__ = "astro_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)


class Record(db.Model):
    __tablename__ = "astro_record"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)


@app.route("/")
def index():
    return render_template("index.html", title="AstroDodge")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/list")
def space_list():
    return render_template("list.html", space_list=data, title="Space List")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8005, debug=True)
