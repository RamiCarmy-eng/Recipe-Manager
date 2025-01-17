import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask Configuration
    FLASK_APP = os.getenv('FLASK_APP', 'wsgi.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', True)

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_PATH', 'sqlite:///instance/recipes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Recipe Configuration
    RECIPES_PER_PAGE = 12

    # Shopping List Configuration
    MAX_SHOPPING_LISTS = 10

    # Comment Configuration
    MAX_COMMENT_LENGTH = 1000

    def __init__(self):
        # Ensure upload folder exists
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    SECRET_KEY = os.getenv('SECRET_KEY')  # Must be set in production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Create default config instance
config = Config()