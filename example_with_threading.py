import json
import threading

from flask import render_template, request, session, redirect, url_for, Flask

app = Flask(__name__)
lock = threading.Lock()  # Create a lock for file access


def read_file(filename):
    with lock:  # Acquire the lock before reading
        with open(filename, 'r') as f:
            return json.load(f)


def write_file(filename, data):
    with lock:  # Acquire the lock before writing
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


# Load user data from file (replace with your actual data source)
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


users = load_users()


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
