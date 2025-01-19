from .admin import admin_bp
from .auth import auth_bp
from .main import main_bp
from .recipe import recipe_bp
from .shopping import shopping_bp
from .collaborative import collaborative_bp
from .ingredient import ingredient_bp
from .category import category_bp
from .favorite import favorite_bp
from .comment import comment_bp
from .template import template_bp

__all__ = [
    'admin_bp',
    'auth_bp',
    'main_bp',
    'recipe_bp',
    'shopping_bp',
    'collaborative_bp',
    'ingredient_bp',
    'category_bp',
    'favorite_bp',
    'comment_bp',
    'template_bp'
]

from flask import Blueprint

main_bp = Blueprint('main', __name__)

from . import main  # This imports the routes