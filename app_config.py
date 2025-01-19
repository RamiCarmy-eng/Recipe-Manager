import os

# Get absolute path to the application root directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
config = {
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{os.path.join(basedir, "instance", "recipes.db")}',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ENGINE_OPTIONS': {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'check_same_thread': False,
            'timeout': 30
        }
    },
    
    # Rest of your config settings...
    'SECRET_KEY': 'dev',
    'SESSION_COOKIE_SECURE': True,
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'UPLOAD_FOLDER': os.path.join(basedir, 'static', 'uploads'),
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'gif'},
    'ADMIN_USERNAME': 'admin',
    'ADMIN_PASSWORD': 'admin123'
}

# Create necessary directories
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
os.makedirs(os.path.join(basedir, 'static', 'uploads'), exist_ok=True)

# Create folders if they don't exist
def create_upload_folders():
    folders = [
        config['UPLOAD_FOLDER'],    # /static/images
        config['AVATAR_FOLDER'],    # /static/images/avatars
        config['RECIPE_FOLDER'],    # /static/images/recipes
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")