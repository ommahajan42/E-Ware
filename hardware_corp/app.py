from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('hardware.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    conn = sqlite3.connect('hardware.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user (name, email, password) VALUES (?, ?, ?)', (name, email, password))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('hardware.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return jsonify({'message': 'Login successful!'}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
