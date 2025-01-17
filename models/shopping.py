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
    user = db.relationship('User', backref=db.backref('shopping_lists', lazy=True))
    items = db.relationship('ShoppingListItem', backref='shopping_list', lazy=True, cascade='all, delete-orphan')


class ShoppingListItem(db.Model):
    __tablename__ = 'shopping_list_items'

    id = db.Column(db.Integer, primary_key=True)
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_lists.id'), nullable=False)
    ingredient_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(50))
    checked = db.Column(db.Boolean, default=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))  # Optional: track which recipe it came from
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Optional: link to recipe
    recipe = db.relationship('Recipe', backref=db.backref('shopping_items', lazy=True))