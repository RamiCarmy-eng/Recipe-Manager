from extensions import db
from models import Category, IngredientCategory
from categories import categories, Recipe_Category, All_Ingredients
from main import app
import sqlite3
import flask
from flask import flask_sqlaLchemy




def populate_categories():
    with app.app_context():
        # Add main recipe categories
        for category_name in Recipe_Category:
            if not Category.query.filter_by(name=category_name).first():
                category = Category(name=category_name)
                db.session.add(category)
        
        # Add ingredient categories
        for ingredient_name in set(All_Ingredients):  # Using set to remove duplicates
            if not IngredientCategory.query.filter_by(name=ingredient_name).first():
                ingredient_cat = IngredientCategory(name=ingredient_name)
                db.session.add(ingredient_cat)
        
        try:
            db.session.commit()
            print("Categories populated successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

if __name__ == "__main__":
    populate_categories()