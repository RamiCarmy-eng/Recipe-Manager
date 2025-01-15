import sqlite3

db = sqlite3.connect('instance/recipes.db')
cursor = db.cursor()
try:
    cursor.execute('ALTER TABLE recipes ADD COLUMN image TEXT')
    db.commit()
    print("Successfully added image column!")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print("Image column already exists")
    else:
        print(f"Error: {str(e)}")
finally:
    db.close()
