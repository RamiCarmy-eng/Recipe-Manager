import os
from datetime import timedelta

class ProductionConfig:
    """Production configuration settings"""
    # Basic Flask Configuration
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'

    # Security Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'generate-a-strong-secret-key-in-production')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/recipes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Logging Configuration
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT', 'false').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.getenv('LOG_FILE', 'logs/recipe_manager.log')
    # 10MB = 10485760 bytes
    LOG_MAX_BYTES = 10485760
    LOG_BACKUP_COUNT = 10

    # Cache Configuration
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300

    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = '100 per minute'
    RATELIMIT_HEADERS_ENABLED = True

    # Security Headers
    STRICT_TRANSPORT_SECURITY = True
    STRICT_TRANSPORT_SECURITY_PRELOAD = True
    STRICT_TRANSPORT_SECURITY_MAX_AGE = 31536000
    CONTENT_SECURITY_POLICY = {
        'default-src': "'self'",
        'img-src': "'self' data: https:",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net",
        'style-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net",
        'font-src': "'self' https://cdn.jsdelivr.net",
    }

    # Error Reporting
    PROPAGATE_EXCEPTIONS = True
    PREFERRED_URL_SCHEME = 'https'

    # Performance
    COMPRESS_MIMETYPES = [
        'text/html',
        'text/css',
        'text/xml',
        'application/json',
        'application/javascript'
    ]
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500