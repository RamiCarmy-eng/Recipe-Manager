import sqlite3

def check_schema():
    conn = sqlite3.connect('instance/recipes.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name;
    """)
    
    tables = cursor.fetchall()
    
    print("Database Tables:")
    for table in tables:
        print(f"\nTable: {table[0]}")
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == '__main__':
    check_schema() 