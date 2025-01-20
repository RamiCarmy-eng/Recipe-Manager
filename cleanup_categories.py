from wsgiO import app, db
from sqlalchemy import text

def cleanup_database():
    with app.app_context():
        try:
            print("Starting database cleanup...")
            
            # Drop duplicate tables if they exist
            with db.engine.connect() as conn:
                # Drop categories tables
                conn.execute(text("DROP TABLE IF EXISTS categories"))
                conn.execute(text("DROP TABLE IF EXISTS ingredient_categories"))
                conn.commit()
                print("Dropped duplicate tables successfully")
                
                # Show remaining tables
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                tables = [row[0] for row in result]
                print("\nRemaining tables:", tables)
                
                # Show contents of category table
                result = conn.execute(text("SELECT COUNT(*) FROM category"))
                count = result.scalar()
                print(f"\nCategories in category table: {count}")
                
                # Show contents of ingredient_category table
                result = conn.execute(text("SELECT COUNT(*) FROM ingredient_category"))
                count = result.scalar()
                print(f"Categories in ingredient_category table: {count}")
                
            print("\nCleanup completed successfully!")
            return True
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
            return False

if __name__ == "__main__":
    cleanup_database() 