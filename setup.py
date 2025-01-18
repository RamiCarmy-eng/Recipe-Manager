import os
import subprocess
import sys
from setuptools import setup, find_packages

setup(
    name='recipe_master',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-login',
        'python-dotenv',
        'werkzeug',
        'email-validator',
        'pillow',
    ],
    entry_points={
        'console_scripts': [
            'recipe-master=recipe_master.wsgi:main',
        ],
    }
)


def setup_project():
    """Set up the project environment"""
    print("Setting up Recipe-Master project...")
    
    # Create virtual environment
    if not os.path.exists('venv'):
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
        print("Created virtual environment")
    
    # Activate virtual environment and install requirements
    if os.name == 'nt':  # Windows
        activate_script = os.path.join('venv', 'Scripts', 'activate')
        pip_path = os.path.join('venv', 'Scripts', 'pip')
    else:  # Unix/Linux
        activate_script = os.path.join('venv', 'bin', 'activate')
        pip_path = os.path.join('venv', 'bin', 'pip')
    
    # Install requirements
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'])
    print("Installed requirements")
    
    # Create necessary directories
    os.makedirs('instance', exist_ok=True)
    os.makedirs(os.path.join('static', 'uploads'), exist_ok=True)
    print("Created necessary directories")
    
    print("\nSetup complete! To start working:")
    print("1. Activate the virtual environment:")
    print(f"   {activate_script}")
    print("2. Run the application:")
    print("   python main.py")

if __name__ == "__main__":
    setup_project()