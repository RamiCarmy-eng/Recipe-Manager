from flask import Flask
from extensions import db
import sqlite3

# First, try direct SQLite connection
print("Trying direct SQLite connection...")
try:
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\nTables in database:")
    for table in tables:
        print(table[0])
    conn.close()
except Exception as e:
    print(f"SQLite Error: {e}")

# Then try Flask-SQLAlchemy connection
print("\nTrying Flask-SQLAlchemy connection...")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    try:
        result = db.session.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("\nTables through SQLAlchemy:")
        for row in result:
            print(row[0])
    except Exception as e:
        print(f"SQLAlchemy Error: {e}") 