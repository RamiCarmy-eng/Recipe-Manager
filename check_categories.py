from wsgi import app, db
from models.models import Category, IngredientCategory
from sqlalchemy import text

def check_database():
    with app.app_context():
        print("\nChecking database tables...")
        
        # Check if tables exist
        with db.engine.connect() as conn:
            # Get all tables
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result]
            print("\nExisting tables:", tables)
            
            # Check categories table
            if 'categories' in tables:
                result = conn.execute(text("PRAGMA table_info(categories);"))
                print("\nCategories table structure:")
                for row in result:
                    print(f"- {row}")
                
                # Count categories
                result = conn.execute(text("SELECT COUNT(*) FROM categories;"))
                count = result.scalar()
                print(f"\nNumber of categories in database: {count}")
                
                # Show all categories
                result = conn.execute(text("SELECT * FROM categories;"))
                print("\nAll categories:")
                for row in result:
                    print(f"- {row}")
            else:
                print("\nCategories table does not exist!")
            
            # Check ingredient_categories table
            if 'ingredient_categories' in tables:
                result = conn.execute(text("PRAGMA table_info(ingredient_categories);"))
                print("\nIngredient Categories table structure:")
                for row in result:
                    print(f"- {row}")
                
                # Count ingredient categories
                result = conn.execute(text("SELECT COUNT(*) FROM ingredient_categories;"))
                count = result.scalar()
                print(f"\nNumber of ingredient categories in database: {count}")
                
                # Show all ingredient categories
                result = conn.execute(text("SELECT * FROM ingredient_categories;"))
                print("\nAll ingredient categories:")
                for row in result:
                    print(f"- {row}")
            else:
                print("\nIngredient Categories table does not exist!")

if __name__ == "__main__":
    check_database() 