from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'dev'

def get_db():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            return jsonify({
                'username': session['username'],
                'role': session['role']
            })
        return jsonify({'error': 'Not logged in'}), 401

    data = request.get_json()
    print("Login attempt:", data)
    
    conn = get_db()
    try:
        cursor = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            [data['username'], data['password']]
        )
        user = cursor.fetchone()
        print("Found user:", dict(user) if user else None)
        
        if user:
            session.clear()
            session['username'] = user['username']
            session['role'] = user['role']
            session.permanent = True  # Make session permanent
            print("Session created:", dict(session))
            return jsonify({
                'success': True,
                'username': user['username'],
                'role': user['role']
            })
        return jsonify({'error': 'Invalid credentials'}), 401
    finally:
        conn.close()

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    print("Current session at dashboard:", dict(session))  # Debug print
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)