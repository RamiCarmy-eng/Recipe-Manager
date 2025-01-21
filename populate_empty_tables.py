from flask import Flask
from extensions import db
from models.models import *
from datetime import datetime, timedelta
import random


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


def populate_complete_database():
    print("\nStarting COMPLETE database population...")

    try:
        # Get existing data
        user = User.query.first()
        recipes = Recipe.query.all()
        ingredients = Ingredient.query.all()

        if not user or not recipes or not ingredients:
            print("Error: Need existing user, recipes, and ingredients!")
            return

        # 1. Create Shopping Lists
        print("\nCreating shopping lists...")
        shopping_lists = []
        for name in ["Weekly Groceries", "Party Supplies", "Monthly Stock", "Healthy Foods"]:
            sl = ShoppingList(
                user_id=user.id,
                name=name,
                created_at=datetime.utcnow()
            )
            db.session.add(sl)
            shopping_lists.append(sl)

        # 2. Create Shopping List Templates
        print("Creating shopping list templates...")
        templates = []
        for name in ["Basic Weekly", "Party Essentials", "Healthy Shopping"]:
            template = ShoppingListTemplate(
                user_id=user.id,
                name=name,
                created_at=datetime.utcnow()
            )
            db.session.add(template)
            templates.append(template)

        # 3. Create Collaborative Lists
        print("Creating collaborative lists...")
        collab_lists = []
        for name in ["Family Shopping", "Roommates List", "Holiday Planning"]:
            cl = CollaborativeList(
                name=name,
                owner_id=user.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(cl)
            collab_lists.append(cl)

        db.session.flush()

        # 4. Add Shopping List Items
        print("Adding shopping list items...")
        for sl in shopping_lists:
            for ingredient in random.sample(ingredients, min(5, len(ingredients))):
                item = ShoppingListItem(
                    shopping_list_id=sl.id,
                    ingredient_id=ingredient.id,
                    ingredient_name=ingredient.name,  # Add this line
                    amount=random.randint(1, 5),
                    unit=ingredient.unit,
                    checked=random.choice([True, False])
                )
                db.session.add(item)

        # 5. Add Template Items
        print("Adding template items...")
        for template in templates:
            for ingredient in random.sample(ingredients, min(5, len(ingredients))):
                item = TemplateItem(
                    template_id=template.id,
                    name=ingredient.name,
                    amount=random.randint(1, 5),
                    unit=ingredient.unit,
                    category=ingredient.category,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(item)

        # 6. Add Collaborative List Members and Items
        print("Adding collaborative list members and items...")
        for cl in collab_lists:
            # Add member
            member = CollaborativeListMember(
                list_id=cl.id,
                user_id=user.id,
                can_edit=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(member)

            # Add items
            for ingredient in random.sample(ingredients, min(5, len(ingredients))):
                item = CollaborativeListItem(
                    list_id=cl.id,
                    name=ingredient.name,
                    amount=random.randint(1, 5),
                    unit=ingredient.unit,
                    category=ingredient.category,
                    added_by=user.id,
                    completed=random.choice([True, False]),
                    completed_by=user.id if random.choice([True, False]) else None,
                    completed_at=datetime.utcnow() if random.choice([True, False]) else None,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(item)

        # 7. Add User Activities
        print("Adding user activities...")
        activities = [
            ('created_list', 'Created new shopping list'),
            ('added_item', 'Added item to list'),
            ('completed_item', 'Marked item as complete'),
            ('shared_list', 'Shared list with user'),
            ('used_template', 'Created list from template')
        ]

        for _ in range(50):
            activity_type, activity_details = random.choice(activities)  # Get both values from the tuple
            activity = UserActivity(
                user_id=user.id,
                action=activity_type,  # Use activity_type instead of action
                details=activity_details,  # Use activity_details instead of details
                ip_address='127.0.0.1',
                timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(activity)

        # Final commit
        db.session.commit()
        print("\nDatabase population completed successfully!")

        # Print summary
        print("\n=== Final Database Summary ===")
        print(f"Shopping Lists: {len(shopping_lists)}")
        print(f"Shopping List Items: {ShoppingListItem.query.count()}")
        print(f"Templates: {len(templates)}")
        print(f"Template Items: {TemplateItem.query.count()}")
        print(f"Collaborative Lists: {len(collab_lists)}")
        print(f"Collaborative List Members: {CollaborativeListMember.query.count()}")
        print(f"Collaborative List Items: {CollaborativeListItem.query.count()}")
        print(f"User Activities: {UserActivity.query.count()}")

    except Exception as e:
        db.session.rollback()
        print(f"\nError: {str(e)}")
        print(f"Error location: {e.__traceback__.tb_lineno}")
        raise e


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        populate_complete_database()