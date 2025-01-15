import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the path to the application directory
basedir = os.path.abspath(os.path.dirname(__file__))
print(f"basedir {basedir}")
input("wait")
# Import the create_app function
from config.factory import create_app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Run the app with the host and port specified in environment variables
    # or use defaults if not specified
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    app.run(
        host=host,
        port=port,
        debug=debug
    )
