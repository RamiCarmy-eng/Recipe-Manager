import os


def verify_files():
    files_to_check = {
        'main_old.py': 'from flask import Flask',
        'init_db.py': 'from werkzeug.security import generate_password_hash',
        'templates/base.html': '<!DOCTYPE html>',
        'templates/login.html': '{% extends "base.html" %}',
        'templates/dashboard.html': '{% extends "base.html" %}',
        'templates/modals/recipe_modal.html': '<!-- Recipe Modal -->',
        'templates/modals/user_modal.html': '<div class="modal fade"',
        'static/css/styles.css': '/* General Styles */',
        'static/js/scripts.js': '// Global variables'
    }

    for file_path, expected_content in files_to_check.items():
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if expected_content in content:
                    print(f'✓ {file_path} (Content verified)')
                else:
                    print(f'✗ {file_path} (Content mismatch)')
        else:
            print(f'✗ {file_path} (File missing)')


verify_files()
