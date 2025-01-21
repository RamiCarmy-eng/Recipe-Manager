from extensions import db
from flask import Flask
from extensions import db
from flask_login import LoginManager
from models.models import (
    User, Recipe, Category, Ingredient, Comment, Favorite,
    UserPreference, IngredientCategory, ShoppingList, ShoppingListItem,
    ShoppingListTemplate, TemplateItem, CollaborativeList,
    CollaborativeListMember, CollaborativeListItem, RecipeIngredient,
    UserActivity
)
from sqlalchemy import text
from routes.auth import auth_bp
from routes.main import main_bp  # Changed from main to main_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Setup Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)  # Changed from main to main_bp

    return app


def check_tables():
    print("\nChecking table contents:")
    tables = {
        'users': User,
        'recipes': Recipe,
        'categories': Category,
        'ingredients': Ingredient,
        'comments': Comment,
        'favorites': Favorite,
        'user_preferences': UserPreference,
        'ingredient_categories': IngredientCategory,
        'shopping_lists': ShoppingList,
        'shopping_list_items': ShoppingListItem,
        'shopping_list_templates': ShoppingListTemplate,
        'template_items': TemplateItem,
        'collaborative_lists': CollaborativeList,
        'collaborative_list_members': CollaborativeListMember,
        'collaborative_list_items': CollaborativeListItem,
        'recipe_ingredients': RecipeIngredient,
        'user_activities': UserActivity
    }

    print("\n=== Table Row Counts ===")
    empty_tables = []
    for table_name, model in tables.items():
        try:
            count = db.session.query(model).count()
            print(f"{table_name}: {count} rows")
            if count == 0:
                empty_tables.append(table_name)
        except Exception as e:
            print(f"Error checking {table_name}: {str(e)}")

    print("\n=== Empty Tables ===")
    for table in empty_tables:
        print(f"- {table}")


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        check_tables()

    app.run(debug=True)