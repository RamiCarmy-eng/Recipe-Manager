from flask import Flask, render_template
from flask_login import LoginManager
from extensions import db
from models.models import User
import os
from datetime import datetime
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from flask_mail import Mail
mail = Mail()  # Add this line


def create_app():
    app = Flask(__name__)
    
    # Config settings
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # File upload settings
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # For recipe images
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    
    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Changed to auth blueprint
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register ALL blueprints
    from routes.main import main_bp
    from routes.admin import admin_bp
    from routes.auth import auth_bp
    from routes.recipe import recipe_bp
    from routes.shopping import shopping_bp
    from routes.category import category_bp
    from routes.collaborative import collaborative_bp
    from routes.comment import comment_bp
    from routes.user import user_bp
    from routes.ingredient import ingredient_bp
    from routes.template import template_bp
    from routes.favorite import favorite_bp
    from routes.activity import activity_bp
    from routes.list import list_bp
    from routes.search import search_bp
    from routes.profile import profile_bp
    from routes.settings import settings_bp
    
    # Register blueprints with correct URLs
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipe_bp, url_prefix='/recipe')
    app.register_blueprint(shopping_bp, url_prefix='/shopping')
    app.register_blueprint(category_bp, url_prefix='/category')
    app.register_blueprint(collaborative_bp, url_prefix='/collaborative')
    app.register_blueprint(comment_bp, url_prefix='/comment')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(ingredient_bp, url_prefix='/ingredient')
    app.register_blueprint(template_bp, url_prefix='/template')
    app.register_blueprint(favorite_bp, url_prefix='/favorite')
    app.register_blueprint(activity_bp, url_prefix='/activity')
    app.register_blueprint(list_bp, url_prefix='/list')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    
    # Create required directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'avatars'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'recipes'), exist_ok=True)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
        
    # Register template filters if needed
    @app.template_filter('datetime')
    def format_datetime(value, format='%Y-%m-%d %H:%M'):
        if value:
            return value.strftime(format)
        return ''
    
    @app.template_filter('timeago')
    def timeago(value):
        if not value:
            return ''
        now = datetime.utcnow()
        diff = now - value
        
        if diff.days > 365:
            return f'{diff.days // 365}y ago'
        if diff.days > 30:
            return f'{diff.days // 30}mo ago'
        if diff.days > 0:
            return f'{diff.days}d ago'
        if diff.seconds > 3600:
            return f'{diff.seconds // 3600}h ago'
        if diff.seconds > 60:
            return f'{diff.seconds // 60}m ago'
        return 'just now'

def create_app():
    app = Flask(__name__)

    # Config settings
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # File upload settings
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    # Initialize extensions
    db.init_app(app)

    mail.init_app(app)

    # Setup Flask-Login - UPDATED THIS SECTION
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Point to auth.login instead of main.login
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        if user_id is None:
            return None
        return User.query.get(int(user_id))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 