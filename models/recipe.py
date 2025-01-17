from extensions import db
from datetime import datetime

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    instructions = db.Column(db.Text)
    image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)

    # Define relationships with back_populates
    favorites = db.relationship('Favorite', back_populates='recipe')
    comments = db.relationship('Comment', back_populates='recipe')

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    __table_args__ = {'extend_existing': True}  # Add this line

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(50))
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)