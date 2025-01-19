from extensions import db
from app import create_app

def run():
    app = create_app()
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    run()
