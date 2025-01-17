from datetime import datetime
from flask_login import UserMixin
from extensions import db

from datetime import datetime
from flask_login import UserMixin
from extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    email = db.Column(db.String(120))
    avatar = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Define relationships with back_populates
    recipes = db.relationship('Recipe', back_populates='user', lazy=True)
    favorites = db.relationship('Favorite', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    shopping_lists = db.relationship('ShoppingList', back_populates='user', lazy=True)

    def is_admin(self):
        return self.role == 'admin'