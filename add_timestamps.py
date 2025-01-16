import sqlite3

def add_timestamps():
    conn = sqlite3.connect('instance/recipes.db')
    cursor = conn.cursor()
    
    try:
        # Add created_at column
        cursor.execute('''
            ALTER TABLE recipes 
            ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ''')
        
        # Add updated_at column
        cursor.execute('''
            ALTER TABLE recipes 
            ADD COLUMN updated_at DATETIME
        ''')
        
        conn.commit()
        print("Successfully added timestamp columns")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Columns already exist")
        else:
            print(f"Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    add_timestamps()