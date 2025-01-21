import os
from pathlib import Path
from datetime import timedelta

# Move basedir outside the class
basedir = Path(__file__).parent
instance_path = os.path.join(basedir, 'instance')

# Create instance directory if it doesn't exist
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

class BaseConfig:
    # Flask settings
    SECRET_KEY = 'your-super-secret-key'
    DEBUG = True
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(basedir, 'instance', 'recipes.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Instance folder for database and other instance-specific files
    INSTANCE_PATH = str(Path(basedir, 'instance'))
    
    # Mail settings
    MAIL_DEBUG = 1
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your-email@gmail.com'
    MAIL_PASSWORD = 'your-password'
    MAIL_DEFAULT_SENDER = 'your-email@gmail.com'
    MAIL_MAX_EMAILS = 10
    MAIL_ASCII_ATTACHMENTS = False
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = str(Path(basedir, 'static', 'images'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    SESSION_COOKIE_SECURE = False  # Set to True in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Recipe settings
    RECIPES_PER_PAGE = 12
    MAX_SEARCH_RESULTS = 50
    FEATURED_RECIPES_COUNT = 6
    
    # User settings
    PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
    ACTIVATION_TIMEOUT = 86400  # 24 hours
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_DISABLED = False
    
    # Cache settings
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # API settings
    API_RATE_LIMIT = '100 per minute'
    JWT_SECRET_KEY = 'your-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Social auth settings
    OAUTH_CREDENTIALS = {
        'google': {
            'id': 'your-google-client-id',
            'secret': 'your-google-client-secret'
        },
        'facebook': {
            'id': 'your-facebook-client-id',
            'secret': 'your-facebook-client-secret'
        }
    }
    
    # Shopping list settings
    MAX_SHOPPING_LISTS = 10
    MAX_ITEMS_PER_LIST = 100
    
    # Collaboration settings
    MAX_COLLABORATORS = 5
    COLLABORATION_TIMEOUT = 3600  # 1 hour
    
    # Export settings
    EXPORT_FORMATS = ['pdf', 'xlsx', 'csv']
    MAX_EXPORT_ITEMS = 1000
    
    # Notification settings
    NOTIFICATION_LIFETIME = 604800  # 7 days
    EMAIL_NOTIFICATION_DELAY = 300  # 5 minutes
    
    # Logging
    LOG_FILE = str(Path(basedir, 'instance', 'recipe_master.log'))
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = 'INFO'

    # Database connection settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'check_same_thread': False,
            'timeout': 30
        }
    }

    # Admin
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'

    # Make sure instance path exists
    @staticmethod
    def init_app(app):
        os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
        os.makedirs(os.path.join(basedir, 'static', 'images'), exist_ok=True)
        print(f"Database path: {os.path.abspath(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))}")

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(basedir, 'instance', 'recipes.db'))
    MAIL_DEBUG = 1
    SESSION_COOKIE_SECURE = False
    CACHE_TYPE = 'simple'
    LOG_LEVEL = 'DEBUG'
    
    # Development-specific settings
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = True
    SEND_FILE_MAX_AGE_DEFAULT = 0

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/recipe_master'
    MAIL_DEBUG = 0
    SESSION_COOKIE_SECURE = True
    CACHE_TYPE = 'redis'
    LOG_LEVEL = 'ERROR'
    
    # Production security settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # SSL/HTTPS settings
    PREFERRED_URL_SCHEME = 'https'
    
    # Production performance settings
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_TIMEOUT = 30
    
    # Production cache settings
    CACHE_REDIS_HOST = 'redis'
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Production mail settings
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_PORT = 465
    
    # Production file storage (e.g., AWS S3)
    USE_S3_STORAGE = True
    S3_BUCKET = 'your-bucket-name'
    S3_REGION = 'your-region'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    # Production monitoring
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = 'redis://redis:6379/0'
    
    # Production security headers
    SECURE_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'"
    }

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    
    # Test-specific settings
    LOGIN_DISABLED = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

# Set the config based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Use this in wsgi.py
def get_config():
    return config[os.environ.get('FLASK_ENV', 'default')]

# This is what we import in main.py
AppConfig = DevelopmentConfig 