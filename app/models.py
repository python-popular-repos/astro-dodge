from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "astro_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)


class Record(db.Model):
    __tablename__ = "record"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
