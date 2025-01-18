import click
from flask.cli import with_appcontext
from extensions import db
from models.models import User
from werkzeug.security import generate_password_hash
import os

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    click.echo('Initialized the database.')

@click.command('create-admin')
@with_appcontext
def create_admin_command():
    """Create admin user."""
    admin = User(
        username=os.getenv('ADMIN_USERNAME'),
        email=os.getenv('ADMIN_EMAIL'),
        password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD')),
        role='admin',
        is_active=True
    )
    db.session.add(admin)
    db.session.commit()
    click.echo('Created admin user.')
