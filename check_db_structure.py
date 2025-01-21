from flask import Flask
from extensions import db
from models.models import *
from sqlalchemy import inspect

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def check_database_structure():
    print("\n=== Complete Database Structure ===\n")
    inspector = inspect(db.engine)
    
    for table_name in inspector.get_table_names():
        print(f"\nTable: {table_name}")
        print("-" * (len(table_name) + 7))
        
        # Get columns
        columns = inspector.get_columns(table_name)
        print("Columns:")
        for column in columns:
            print(f"  - {column['name']}: {column['type']}")
            
        # Get foreign keys
        foreign_keys = inspector.get_foreign_keys(table_name)
        if foreign_keys:
            print("\nForeign Keys:")
            for fk in foreign_keys:
                print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        # Get indexes
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print("\nIndexes:")
            for idx in indexes:
                print(f"  - {idx['name']}: {idx['column_names']}")

        print("\n" + "=" * 50)

    # Also check model relationships
    print("\n=== Model Relationships ===\n")
    for model in [User, ShoppingList, ShoppingListItem, CollaborativeList, CollaborativeListMember, CollaborativeListItem]:
        print(f"\nModel: {model.__name__}")
        print("-" * (len(model.__name__) + 7))
        for rel in inspect(model).relationships:
            print(f"  - {rel.key}: {rel.target.name}")

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        check_database_structure() 