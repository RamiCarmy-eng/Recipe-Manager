import sqlite3
import os

def reset_db():
    # Delete the existing database file
    if os.path.exists('recipes_images.db'):
        os.remove('recipes_images.db')
        print("Old database deleted")
    
    # Create new database
    conn = sqlite3.connect('recipes_images.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Create recipes_images table
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            instructions TEXT,
            image_url TEXT
        )
    ''')
    
    # Create ingredients table
    c.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER,
            name TEXT NOT NULL,
            amount REAL,
            unit TEXT,
            FOREIGN KEY (recipe_id) REFERENCES recipes_images (id)
        )
    ''')
    
    # Create shopping list table
    c.execute('''
        CREATE TABLE IF NOT EXISTS shopping_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            recipe_id INTEGER,
            item_name TEXT NOT NULL,
            amount REAL,
            unit TEXT,
            category TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (recipe_id) REFERENCES recipes_images (id)
        )
    ''')
    
    # Add test users
    c.execute('''
        INSERT INTO users (username, password, role)
        VALUES 
            ('admin', 'admin', 'admin'),
            ('manager', 'manager', 'manager'),
            ('user', 'user', 'user')
    ''')
    
    conn.commit()
    
    # Verify users were created
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    print("\nCreated users:")
    for user in users:
        print(f"Username: {user[1]}, Password: {user[2]}, Role: {user[3]}")
    
    conn.close()
    print("\nDatabase reset complete!")

if __name__ == '__main__':
    reset_db() 