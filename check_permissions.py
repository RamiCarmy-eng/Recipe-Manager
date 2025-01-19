import os
import sys
import sqlite3
from pathlib import Path

def check_and_fix_permissions():
    # Get the current working directory
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")

    # Check instance directory
    instance_path = os.path.join(current_dir, 'instance')
    db_path = os.path.join(instance_path, 'recipes.db')
    
    print("\nChecking paths and permissions...")
    print(f"Instance directory path: {instance_path}")
    print(f"Database file path: {db_path}")

    # Check if instance directory exists
    if not os.path.exists(instance_path):
        try:
            os.makedirs(instance_path)
            print(f"Created instance directory at: {instance_path}")
        except Exception as e:
            print(f"Error creating instance directory: {e}")
            return False

    # Check if we can write to instance directory
    try:
        test_file = os.path.join(instance_path, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("Successfully wrote to instance directory")
    except Exception as e:
        print(f"Error writing to instance directory: {e}")
        return False

    # Try to create/open the database
    try:
        if os.path.exists(db_path):
            print(f"Database exists at: {db_path}")
            # Try to open it
            conn = sqlite3.connect(db_path)
            conn.close()
            print("Successfully opened existing database")
        else:
            print("Database file doesn't exist, trying to create it...")
            conn = sqlite3.connect(db_path)
            conn.close()
            print("Successfully created new database")
            
        # Set proper permissions
        try:
            os.chmod(db_path, 0o666)  # Read/write for everyone
            print("Set database file permissions")
        except Exception as e:
            print(f"Warning: Couldn't set database permissions: {e}")
            
    except Exception as e:
        print(f"Error accessing database: {e}")
        return False

    print("\nAll checks completed!")
    return True

if __name__ == "__main__":
    success = check_and_fix_permissions()
    if success:
        print("\nPermissions check passed. You can now run fix_db.py")
    else:
        print("\nPermissions check failed. Please fix the issues above before running fix_db.py") 