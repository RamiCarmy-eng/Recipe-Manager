import sqlite3

conn = sqlite3.connect('instance/recipes.db')
cursor = conn.cursor()

# Get column info
cursor.execute('PRAGMA table_info(recipes_images)')
columns = cursor.fetchall()

print("Recipe table columns:")
for col in columns:
    print(f"- {col[1]} ({col[2]})")

conn.close()
