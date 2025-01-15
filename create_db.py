import sqlite3
import os

def create_db():
    # Delete existing database
    if os.path.exists('recipes.db'):
        os.remove('recipes.db')
        print("Deleted old database")
    
    # Create new database
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    print("Created users table")
    
    # Add test users
    cursor.execute('''
        INSERT INTO users (username, password, role)
        VALUES 
            ('admin', 'admin', 'admin'),
            ('manager', 'manager', 'manager'),
            ('user', 'user', 'user')
    ''')
    print("Added test users")
    
    conn.commit()
    
    # Verify users were added
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    print("\nUsers in database:")
    for user in users:
        print(f"Username: {user[1]}, Password: {user[2]}, Role: {user[3]}")
    
    conn.close()
    print("\nDatabase creation complete!")

if __name__ == '__main__':
    create_db()