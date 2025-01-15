# Recipe Manager Application

Set environment variables first
$env:FLASK_APP = "main.py"
$env:FLASK_ENV = "development"

## Setup
1. Install requirements: `pip install -r requirements.txt`
2. Initialize database: `python main.py`
3. Run application: `flask run`

## Features
- User authentication
- Recipe management
- Shopping list
- User management (admin)

## Structure
- `/static`: Static files (CSS, JS, images)
- `/templates`: HTML templates
- `/instance`: Database file
- `main.py`: Main application file 