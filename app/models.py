from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from dataclasses import dataclass
from app import db


class BaseModel(db.Model):
    __abstract__ = True
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_updated = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )


class User(UserMixin, BaseModel):
    """
    Class that represents a user of the application

    The following attributes of a user are stored in this table:
        * email - email address of the user
        * hashed password - hashed password (using werkzeug.security)
        * registered_on - date & time that the user registered
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hashed = db.Column(db.String(200), nullable=False)

    def __init__(self, email: str, password_plaintext: str):
        """Create a new User object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)

    def is_password_correct(self, password_plaintext: str) -> bool:
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str) -> None:
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext) -> str:
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f"<User: {self.email}>"

    @property
    def is_authenticated(self) -> bool:
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self) -> bool:
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self) -> bool:
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self) -> str:
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)


@dataclass
class SpaceObject:
    """Python dataclass for individually tracked objects in space."""

    des: str
    jd: str
    cd: str
    orbit_id: str
    t_sigma_f: str
    h: float
    dist: float
    dist_min: float
    dist_max: float
    v_rel: float
    v_inf: float

    def __post_init__(self):
        AU_TO_KM_CONVERSION = 1.49e8
        self.dist = float(self.dist) * AU_TO_KM_CONVERSION
        self.dist = round(self.dist, 2)
        self.dist_min = round(float(self.dist_min), 2)
        self.dist_max = float(self.dist_max)
        self.dist_min = float(self.dist_min)
        self.v_rel = float(self.v_rel)
        self.v_inf = round(float(self.v_inf), 2)
        self.h = float(self.h)


class SpaceRecord(BaseModel):
    __tablename__ = "space"

    designation = db.Column(db.String, primary_key=True, unique=True)
    velocity = db.Column(db.Float)
    distance = db.Column(db.Float)
    closest = db.Column(db.DateTime)

    def __init__(self, entry: SpaceObject):
        self.designation = entry.des
        self.velocity = entry.v_inf
        self.distance = entry.dist
        self.closest = datetime.strptime(entry.cd, "%Y-%b-%d %H:%M")

    @classmethod
    def from_dict(cls, data) -> SpaceObject:
        obj = SpaceObject(**data)
        return cls(obj)

    def __repr__(self):
        return (
            f"{self.designation} | {self.velocity} | {self.distance} | {self.closest}"
        )


class Record(BaseModel):
    __tablename__ = "records"
    record_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    space_id = db.Column(db.String, db.ForeignKey("space.designation"))
    space = db.relationship("SpaceRecord", backref=backref("space"))
    user = db.relationship("User", backref=backref("users"))

    def __init__(self, user: int, space: str):
        self.user_id = user
        self.space_id = space

    def __repr__(self):
        return f"{self.user_id} | {self.space_id} | {self.user} | {self.space}"
