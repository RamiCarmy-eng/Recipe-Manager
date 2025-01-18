import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/recipes.db')
cursor = conn.cursor()

# Add the new columns
try:
    cursor.execute('ALTER TABLE recipes_images ADD COLUMN is_reported BOOLEAN DEFAULT FALSE')
    cursor.execute('ALTER TABLE recipes_images ADD COLUMN is_approved BOOLEAN DEFAULT FALSE')
    cursor.execute('ALTER TABLE recipes_images ADD COLUMN is_hidden BOOLEAN DEFAULT FALSE')
    cursor.execute('ALTER TABLE recipes_images ADD COLUMN is_featured BOOLEAN DEFAULT FALSE')
    cursor.execute('ALTER TABLE recipes_images ADD COLUMN rejection_reason TEXT')
    
    conn.commit()
    print("Columns added successfully!")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
finally:
    conn.close()
