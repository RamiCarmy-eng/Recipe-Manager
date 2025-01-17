import sqlite3
from datetime import datetime

def add_timestamps():
    conn = sqlite3.connect('instance/recipes.db')
    cursor = conn.cursor()
    
    try:
        # Add created_at column
        cursor.execute('ALTER TABLE recipes ADD COLUMN created_at DATETIME')
        
        # Add updated_at column
        cursor.execute('ALTER TABLE recipes ADD COLUMN updated_at DATETIME')
        
        # Update existing rows
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('UPDATE recipes SET created_at = ?, updated_at = ?', 
                      (current_time, current_time))
        
        conn.commit()
        print("Successfully added timestamp columns")
        
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_timestamps()