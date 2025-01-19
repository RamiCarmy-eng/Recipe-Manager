import os

# Move basedir outside the class
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')

# Create instance directory if it doesn't exist
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

class Config:
    # Database
    db_path = os.path.join(basedir, 'instance', 'recipes.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database connection settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'check_same_thread': False,
            'timeout': 30
        }
    }

    # Security
    SECRET_KEY = 'dev'  # Change this to a random string in production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File Upload
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Admin
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'

    # Make sure instance path exists
    @staticmethod
    def init_app(app):
        os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
        os.makedirs(os.path.join(basedir, 'static', 'uploads'), exist_ok=True)
        print(f"Database path: {os.path.abspath(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))}")


class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific settings here

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# This is what we import in main.py
AppConfig = DevelopmentConfig 