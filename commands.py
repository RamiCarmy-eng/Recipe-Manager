import click
from flask.cli import with_appcontext
from extensions import db

def register_commands(app):
    @app.cli.command('init-db')
    @with_appcontext
    def init_db():
        """Initialize the database."""
        # Create tables if they don't exist
        db.create_all()
        click.echo('Initialized the database.')
        
    @app.cli.command('reset-db')
    @with_appcontext
    def reset_db():
        """WARNING: Destroys and recreates database tables."""
        if app.env == 'production':
            click.echo('This command is disabled in production.')
            return
        # Only allow in development
        db.drop_all()
        db.create_all()
        click.echo('Database has been reset.') 