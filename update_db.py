from wsgi import app, db
from sqlalchemy import text

def column_exists(conn, table, column):
    """Check if a column exists in a table"""
    result = conn.execute(text(f"PRAGMA table_info({table})"))
    columns = result.fetchall()
    return any(col[1] == column for col in columns)

def update_database():
    print("Starting database update...")
    
    with app.app_context():
        try:
            # Check if subcategory column exists and add it if it doesn't
            print("Checking recipes table structure...")
            with db.engine.connect() as conn:
                if not column_exists(conn, 'recipes', 'subcategory'):
                    print("Adding subcategory column to recipes table...")
                    conn.execute(text('ALTER TABLE recipes ADD COLUMN subcategory VARCHAR(100)'))
                    conn.commit()
                    print("✓ Successfully added subcategory column")
                else:
                    print("✓ Subcategory column already exists")
            
                # Show all columns in recipes table
                print("\nCurrent recipes table columns:")
                result = conn.execute(text("PRAGMA table_info(recipes)"))
                columns = result.fetchall()
                for col in columns:
                    print(f"- {col[1]} ({col[2]})")
            
            print("\nDatabase update completed successfully!")
            
        except Exception as e:
            print(f"Error updating database: {e}")
            db.session.rollback()
            return False
        
        return True

if __name__ == "__main__":
    if update_database():
        print("\nYou can now run test_db_connection.py again")
    else:
        print("\nDatabase update failed") 