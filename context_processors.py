from flask_login import current_user

def register_context_processors(app):
    @app.context_processor
    def utility_processor():
        return {
            'current_user': current_user
        } 