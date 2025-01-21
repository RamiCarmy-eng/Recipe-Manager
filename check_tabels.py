from wsgi import app
from extensions import db
with app.app_context():
    # This will show all table names in your database
    print(db.engine.table_names())