from app import create_app
from extensions import db
from models.models import Category

app = create_app()

def check_categories():
    with app.app_context():
        categories = Category.query.all()
        print("\nCurrent categories in database:")
        for cat in categories:
            print(f"- {cat.name}")

if __name__ == "__main__":
    check_categories() 