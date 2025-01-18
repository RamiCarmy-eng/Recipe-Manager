import sqlite3

conn = sqlite3.connect('instance/recipes.db')
cursor = conn.cursor()

# Get column info for users table
cursor.execute('PRAGMA table_info(users)')
columns = cursor.fetchall()

print("\nUser table columns:")
for col in columns:
    print(f"- {col[1]} ({col[2]})")

conn.close() 