import os
import sqlite3


def run_migration():
    DB_PATH = 'instance/recipes.db'

    # Check if database exists
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Start transaction
        cursor.execute('BEGIN TRANSACTION')

        # Get current columns in users table
        columns = [column[1] for column in cursor.execute('PRAGMA table_info(users)').fetchall()]

        # Add new columns if they don't exist
        if 'email' not in columns:
            print("Adding email column...")
            cursor.execute('ALTER TABLE users ADD COLUMN email TEXT')

        if 'avatar' not in columns:
            print("Adding avatar column...")
            cursor.execute('ALTER TABLE users ADD COLUMN avatar TEXT')

        if 'created_at' not in columns:
            print("Adding created_at column...")
            cursor.execute('''ALTER TABLE users 
                            ADD COLUMN created_at TIMESTAMP 
                            NOT NULL 
                            DEFAULT CURRENT_TIMESTAMP''')

        if 'updated_at' not in columns:
            print("Adding updated_at column...")
            cursor.execute('ALTER TABLE users ADD COLUMN updated_at TIMESTAMP')

        # Create favorites table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            recipe_id INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (recipe_id) REFERENCES recipes (id),
            UNIQUE(user_id, recipe_id)
        )
        ''')

        # Create comments table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            recipe_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (recipe_id) REFERENCES recipes (id)
        )
        ''')

        # Update existing users with timestamps if needed
        cursor.execute('''
        UPDATE users 
        SET created_at = CURRENT_TIMESTAMP 
        WHERE created_at IS NULL
        ''')

        # Commit transaction
        cursor.execute('COMMIT')
        print("Migration completed successfully!")

    except sqlite3.Error as e:
        # Rollback in case of error
        cursor.execute('ROLLBACK')
        print(f"Error during migration: {e}")
        return False

    finally:
        # Show current schema
        print("\nCurrent users table schema:")
        for column in cursor.execute('PRAGMA table_info(users)').fetchall():
            print(f"- {column[1]} ({column[2]})")

        # Close connection
        conn.close()

    return True


if __name__ == "__main__":
    print("Starting database migration...")
    success = run_migration()
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed!")
