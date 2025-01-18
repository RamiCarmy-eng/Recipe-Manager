import sqlite3

def print_table_info(cursor, table_name):
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    print(f"\n{table_name} table columns:")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")

# Connect to the database
conn = sqlite3.connect('instance/recipes.db')
cursor = conn.cursor()

# Get list of all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print info for each table
for table in tables:
    print_table_info(cursor, table[0])

conn.close() 