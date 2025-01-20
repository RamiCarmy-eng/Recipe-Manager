import sqlite3
import os

def check_db_file(db_path):
    print(f"\nChecking database: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Tables found:")
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
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
        print(f"Error with {db_path}: {e}")

def check_all_databases():
    instance_path = 'instance'
    db_files = [f for f in os.listdir(instance_path) if f.endswith('.db')]
    
    print(f"Found database files: {db_files}")
    
    for db_file in db_files:
        db_path = os.path.join(instance_path, db_file)
        check_db_file(db_path)

if __name__ == "__main__":
    check_all_databases() 