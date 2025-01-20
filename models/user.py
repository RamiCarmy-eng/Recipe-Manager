from datetime import datetime
from extensions import db

class ShoppingList(db.Model):
    __tablename__ = 'shopping_lists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='shopping_lists')
    items = db.relationship('ShoppingListItem', backref='shopping_list', lazy=True, cascade='all, delete-orphan')