from flask_login import UserMixin
from sqlalchemy import Enum

from rollie import db, login_manager
from rollie.enums import TrashType, UserRole
from rollie.utils.helper import (
    gen_unique_id, date_today, time_now_ist,
    gen_community_id
)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

notice_user = db.Table(
    "notice_user",
    db.Column("notice_id", db.Integer, db.ForeignKey("notice.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

class User(db.Model, UserMixin):
    """User model representing community members."""

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(12), unique=True, nullable=False, default=gen_unique_id)
    community_id = db.Column(db.String(12), db.ForeignKey("community.unique_id"), nullable=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"), nullable=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_date = db.Column(db.DateTime, default=date_today)

    role = db.Column(Enum(UserRole), nullable=False, default=UserRole.USER)

    scanins = db.relationship('ScanIn', backref='user', lazy=True)
    community = db.relationship("Community", back_populates="users")
    plant = db.relationship("Plant", backref="operators")
    notices = db.relationship("Notice", secondary=notice_user, backref="recipients")

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"


class Plant(db.Model):
    """Waste sorting plant model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=date_today)

    communities = db.relationship("Community", backref="plant", lazy=True)

    def __repr__(self):
        return f"<Plant {self.name}>"


class Community(db.Model):
    """Community model representing groups that users belong to."""

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(12), unique=True, nullable=False, default=gen_community_id)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_date = db.Column(db.DateTime, default=date_today)
    is_flagged = db.Column(db.Boolean, default=False)

    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"), nullable=False)

    users = db.relationship("User", back_populates="community", lazy=True)
    notices = db.relationship("Notice", back_populates="community", lazy=True)

    def __repr__(self):
        return f"<Community {self.name} ({self.unique_id})>"
    
    def get_population(self):
        return len(self.users)


class ScanIn(db.Model):
    """User key card scan-in record with timestamp."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weight = db.Column(db.Integer)
    type = db.Column(Enum(TrashType), nullable=False)
    timestamp = db.Column(db.DateTime, default=time_now_ist)

    def __repr__(self):
        return f"<Scan in by {self.user_id} at {self.timestamp}>"


class Notice(db.Model):
    """Notices sent to community members when flagged/unflagged."""
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey("community.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=time_now_ist)

    community = db.relationship("Community", back_populates="notices")
