import sqlite3

def check_users():
    conn = sqlite3.connect('recipes_images.db')
    conn.row_factory = sqlite3.Row
    
    try:
        cursor = conn.execute('SELECT * FROM users')
        users = cursor.fetchall()
        
        print("\nUsers in database:")
        for user in users:
            print(f"Username: {user['username']}")
            print(f"Password: {user['password']}")
            print(f"Role: {user['role']}")
            print("-" * 20)
            
    finally:
        conn.close()

if __name__ == '__main__':
    check_users()