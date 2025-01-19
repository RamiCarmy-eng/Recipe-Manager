import os
import sqlite3
import time
from sqlalchemy import text
from wsgi import app, db  # Import from your original wsgi.py

def test_connection():
    print("\nTesting database connection...")
    
    # Get database path from app config
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    db_path = db_uri.replace('sqlite:///', '')
    print(f"Database URI from config: {db_uri}")
    print(f"Database path: {os.path.abspath(db_path)}")
    print(f"Database exists: {os.path.exists(db_path)}")
    
    # Test direct SQLite connection
    print("\nTesting direct SQLite connection...")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("✓ Direct SQLite connection successful")
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("\nExisting tables:")
        for table in tables:
            print(f"- {table[0]}")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"✗ Direct SQLite connection failed: {e}")
    
    # Test SQLAlchemy connection
    print("\nTesting SQLAlchemy connection...")
    try:
        with app.app_context():
            # Close any existing sessions
            db.session.remove()
            
            # Test the connection
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                result.scalar()
                print("✓ SQLAlchemy connection successful")
                
                # Test model queries
                from models.models import User, Recipe
                user_count = User.query.count()
                recipe_count = Recipe.query.count()
                print(f"\nDatabase contents:")
                print(f"- Users: {user_count}")
                print(f"- Recipes: {recipe_count}")
            
            # Print connection info
            print(f"\nDatabase options: {app.config.get('SQLALCHEMY_ENGINE_OPTIONS', {})}")
            
    except Exception as e:
        print(f"✗ SQLAlchemy connection failed: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Database file exists: {os.path.exists(db_path)}")
        print(f"Database file is readable: {os.access(db_path, os.R_OK)}")
        print(f"Database file is writable: {os.access(db_path, os.W_OK)}")
    
    # Check file permissions
    print("\nChecking file permissions...")
    try:
        stats = os.stat(db_path)
        print(f"File permissions: {oct(stats.st_mode)[-3:]}")
        print(f"File owner: {stats.st_uid}")
        print(f"File size: {stats.st_size} bytes")
        print(f"Last modified: {time.ctime(stats.st_mtime)}")
    except Exception as e:
        print(f"✗ Could not check file permissions: {e}")

if __name__ == "__main__":
    # First ensure instance directory exists with correct permissions
    instance_dir = 'instance'
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"Created instance directory: {instance_dir}")
    
    # Run the tests
    test_connection() 