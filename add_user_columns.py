import sqlite3

def add_column_if_not_exists(cursor, table, column, definition):
    try:
        cursor.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
        print(f"Added column: {column}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"Column already exists: {column}")
        else:
            print(f"Error adding {column}: {e}")

# Connect to the database
conn = sqlite3.connect('instance/recipes.db')
cursor = conn.cursor()

try:
    # Try to add each column individually
    add_column_if_not_exists(cursor, 'users', 'password_hash', 'TEXT')
    add_column_if_not_exists(cursor, 'users', 'role', 'TEXT DEFAULT "user"')
    add_column_if_not_exists(cursor, 'users', 'is_active', 'BOOLEAN DEFAULT TRUE')
    add_column_if_not_exists(cursor, 'users', 'last_login', 'DATETIME')
    add_column_if_not_exists(cursor, 'users', 'updated_at', 'DATETIME')
    
    conn.commit()
    print("\nFinished adding columns!")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    conn.close() 