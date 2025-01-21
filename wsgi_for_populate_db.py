import os
import sys
from flask import Flask
from extensions import db, login_manager
from flask_migrate import Migrate
from app_config import config
from models.models import (  # Make sure this path matches your project structure
    User, Recipe, Category, Ingredient, Comment, Favorite,
    UserPreference, IngredientCategory, ShoppingList, ShoppingListItem,
    ShoppingListTemplate, TemplateItem, CollaborativeList,
    CollaborativeListMember, CollaborativeListItem, RecipeIngredient,
    UserActivity
)
from sqlalchemy import text
from app import create_app
from config import Config
from jinja2 import Environment
from flask_login import LoginManager
from routes.auth import auth_bp
from routes.main import main_bp
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def nl2br(value):
    return value.replace('\n', '<br>\n')


def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    # Get absolute path for database
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'recipes.db')

    # Load config
    app.config.from_object(Config)

    # Override database URI with absolute path
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set configuration
    app.config.update(config)


    # Initialize extensions
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    db.init_app(app)
    login_manager.init_app(app)

    # Setup login manager
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        if user_id is None:
            return None
        return User.query.get(int(user_id))

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Register blueprints

    from routes.recipe import recipe_bp




    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Initialize extensions

    login_manager.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Import blueprints
    from routes.admin import admin_bp
    from routes.auth import auth_bp
    from routes.main import main_bp

    from routes.shopping import shopping_bp
    from routes.collaborative import collaborative_bp
    from routes.ingredient import ingredient_bp
    from routes.category import category_bp
    from routes.favorite import favorite_bp
    from routes.comment import comment_bp
    from routes.template import template_bp

    # Register blueprints in order of specificity
    app.register_blueprint(recipe_bp, url_prefix='/recipe')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(shopping_bp)
    app.register_blueprint(collaborative_bp)
    app.register_blueprint(ingredient_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(favorite_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(template_bp)

    def nl2br(value):
        return value.replace('\n', '<br>\n')

    # Register jinja2 filters
    app.jinja_env.filters['nl2br'] = nl2br

    return app

app = create_app()

def check_tables():
    print("\nChecking table contents:")
    tables = {
        'users': User,
        'recipes': Recipe,
        'categories': Category,
        'ingredients': Ingredient,
        'comments': Comment,
        'favorites': Favorite,
        'user_preferences': UserPreference,  # Changed from models.UserPreference
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
    
    return empty_tables

def populate_complete_data():
    print("\nPopulating empty tables with comprehensive data...")
    
    try:
        # Get existing user and recipes
        user = User.query.first()
        recipes = Recipe.query.all()
        
        if not user or not recipes:
            print("Error: Need existing users and recipes!")
            return

        # 1. User Preferences (comprehensive)
        if UserPreference.query.count() == 0:
            print("\nAdding complete user preferences...")
            for user in User.query.all():
                pref = UserPreference(
                    user_id=user.id,
                    email_notifications=True,
                    public_profile=True,
                    default_servings=4,
                    measurement_system='metric',
                    theme='light',
                    language='en',
                    created_at=datetime.utcnow()
                )
                db.session.add(pref)

        # 2. Comments (comprehensive)
        if Comment.query.count() == 0:
            print("\nAdding comprehensive comments...")
            comments_text = [
                "Absolutely delicious! Made this for my family and they loved it.",
                "Great recipe, I added some extra garlic and it was perfect.",
                "This has become a weekly staple in our house.",
                "Perfect for meal prep, stays fresh for days.",
                "Love how simple yet flavorful this is.",
                "Made this for a dinner party and got so many compliments!",
                "The instructions were clear and easy to follow.",
                "Great healthy option, will definitely make again.",
                "The cooking time was spot on.",
                "Loved the combination of flavors!"
            ]
            
            # Add multiple comments for each recipe
            for recipe in recipes:
                # Add 2-4 comments per recipe
                for _ in range(random.randint(2, 4)):
                    comment = Comment(
                        user_id=user.id,
                        recipe_id=recipe.id,
                        content=random.choice(comments_text),
                        created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                    )
                    db.session.add(comment)

        # 3. Favorites (comprehensive)
        if Favorite.query.count() == 0:
            print("\nAdding comprehensive favorites...")
            # Add favorites for about 70% of recipes
            for recipe in random.sample(recipes, int(len(recipes) * 0.7)):
                fav = Favorite(
                    user_id=user.id,
                    recipe_id=recipe.id,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 60))
                )
                db.session.add(fav)

        # 4. User Activities (comprehensive)
        if UserActivity.query.count() == 0:
            print("\nAdding comprehensive user activities...")
            activities = [
                ('login', 'User logged in successfully'),
                ('view_recipe', 'Viewed recipe details'),
                ('add_favorite', 'Added recipe to favorites'),
                ('remove_favorite', 'Removed recipe from favorites'),
                ('add_comment', 'Added comment to recipe'),
                ('edit_profile', 'Updated profile information'),
                ('search_recipe', 'Searched for recipes'),
                ('view_category', 'Viewed recipe category'),
                ('export_recipe', 'Exported recipe to PDF'),
                ('share_recipe', 'Shared recipe with others')
            ]
            
            # Add 50 activities with varied timestamps
            for _ in range(50):
                action, details = random.choice(activities)
                activity = UserActivity(
                    user_id=user.id,
                    action=action,
                    details=details,
                    ip_address='127.0.0.1',
                    timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 90))
                )
                db.session.add(activity)

        # Commit all changes
        db.session.commit()
        print("\nSuccessfully added comprehensive data to all empty tables!")
        print("Existing recipes, categories, and ingredients were preserved.")

    except Exception as e:
        db.session.rollback()
        print(f"Error adding data: {str(e)}")
        raise e

# Update your if __name__ == '__main__': section
if __name__ == '__main__':
    with app.app_context():
        empty_tables = check_tables()
        if empty_tables:
            print("\nFound empty tables. Would you like to populate them? (y/n)")
            response = input().lower()
            if response == 'y':
                populate_complete_data()
                check_tables()  # Check again after populating
        
    app.run(debug=True)






