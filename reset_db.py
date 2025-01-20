import os
import shutil
import time
from wsgiO import app, db

def reset_database():
    print("Starting database reset...")
    
    # Path to your instance directory
    instance_dir = 'instance'
    db_path = os.path.join(instance_dir, 'recipes.db')
    
    # 1. First try to close any existing connections
    try:
        with app.app_context():
            db.session.remove()
            db.engine.dispose()
    except Exception as e:
        print(f"Warning when closing connections: {e}")
    
    time.sleep(1)  # Give time for connections to close
    
    # 2. If instance directory exists, rename it instead of deleting
    if os.path.exists(instance_dir):
        backup_dir = f"{instance_dir}_backup_{int(time.time())}"
        try:
            shutil.move(instance_dir, backup_dir)
            print(f"Existing instance directory backed up to: {backup_dir}")
        except Exception as e:
            print(f"Error backing up instance directory: {e}")
            return False
    
    # 3. Create fresh instance directory
    try:
        os.makedirs(instance_dir)
        print("Created fresh instance directory")
    except Exception as e:
        print(f"Error creating instance directory: {e}")
        return False
    
    # 4. Initialize new database
    try:
        with app.app_context():
            db.create_all()
            print("Created new database tables")
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    
    print("Database reset completed successfully!")
    return True

if __name__ == "__main__":
    if reset_database():
        print("\nNow you can run init_db.py to populate the database")
    else:
        print("\nDatabase reset failed") 