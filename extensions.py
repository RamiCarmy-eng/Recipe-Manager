from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_caching import Cache
from flask_apscheduler import APScheduler

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
cache = Cache()
scheduler = APScheduler()

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
