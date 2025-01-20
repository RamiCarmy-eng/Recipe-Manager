
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
# Configure login manager
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
mail = Mail()  # Add this line
