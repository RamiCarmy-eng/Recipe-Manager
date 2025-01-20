import sqlite3

def check_all_tables():
    print("Examining recipes.db database structure...")
    
    try:
        # Connect to recipes.db
        conn = sqlite3.connect('instance/recipes.db')
        cursor = conn.cursor()
        
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\nTables found in database:")
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get table structure
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"- {col[1]} ({col[2]})")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Number of rows: {count}")
            
            # Show sample data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample = cursor.fetchall()
            if sample:
                print("Sample data:", sample)
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_all_tables() 