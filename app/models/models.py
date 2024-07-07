from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    user_is_seller = db.Column(db.Boolean, default=False)
    user_is_stuff = db.Column(db.Boolean, default=False)
    user_agreed = db.Column(db.Boolean, default=False)
    user_banned = db.Column(db.Boolean, default=False)
    user_activated = db.Column(db.Boolean, default=False)
    user_last_login = db.Column(db.DateTime, nullable=True)
    user_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return str(self.id)
