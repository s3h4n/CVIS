from sqlalchemy.sql import func
from datetime import datetime
from application import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"

    user_token = db.Column(db.String(16), primary_key=True)
    first_name = db.Column(db.String(48), nullable=False)
    last_name = db.Column(db.String(48), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    email = db.Column(db.String(48), nullable=False)
    mobile = db.Column(db.String(10), nullable=False)
    addr_line_1 = db.Column(db.String(48), nullable=False)
    addr_line_2 = db.Column(db.String(48), nullable=False)
    town = db.Column(db.String(48), nullable=False)
    uid = db.Column(db.String(16), nullable=False)
    uid_type = db.Column(db.String(24), nullable=False)
    vac_count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=func.now()
    )
    db.UniqueConstraint(email, uid)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class AuthUser(UserMixin, db.Model):
    __tablename__ = "authuser"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(48), nullable=False)
    first_name = db.Column(db.String(48), nullable=True)
    last_name = db.Column(db.String(48), nullable=True)
    mobile = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(48), nullable=False)
    password = db.Column(db.String(48), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=func.now()
    )
    db.UniqueConstraint(username, email)

    def __repr__(self):
        return f"{self.email}"
