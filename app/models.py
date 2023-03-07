from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String)
    track = db.Column(db.String, unique=True)
