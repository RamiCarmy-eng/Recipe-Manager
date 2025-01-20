import sqlite3
import os

def check_db_contents(db_path):
    print(f"\nChecking database: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Tables found:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"- {table_name}: {count} rows")
            
            # Show first few rows of data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
            sample = cursor.fetchall()
            if sample:
                print(f"  Sample data: {sample}")
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def main():
    db_files = [
        'instance/recipes.db',        # Main database
        'instance/recipe.db',         # Extra file
        'instance/recipes_images.db', # Images database
        'instance/recipe_master.db'   # Extra file
    ]
    
    for db_path in db_files:
        if os.path.exists(db_path):
            check_db_contents(db_path)
        else:
            print(f"\n{db_path} does not exist")

if __name__ == "__main__":
    main() 