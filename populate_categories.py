from app import create_app
from extensions import db
from models.models import Category
from categories import Recipe_Category, All_Ingredients

def populate_categories():
    app = create_app()
    with app.app_context():
        print("Starting category population...")
        
        # Add recipe categories
        print("\nAdding recipe categories:")
        for category_name in Recipe_Category:
            if not Category.query.filter_by(name=category_name).first():
                category = Category(name=category_name)
                db.session.add(category)
                print(f"Added category: {category_name}")
        
        # Add ingredient categories
        print("\nAdding ingredient categories:")
        for ingredient_name in All_Ingredients:
            if not Category.query.filter_by(name=ingredient_name).first():
                category = Category(name=ingredient_name)
                db.session.add(category)
                print(f"Added ingredient category: {ingredient_name}")
        
        try:
            db.session.commit()
            print("\nCategories populated successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

if __name__ == "__main__":
    populate_categories()