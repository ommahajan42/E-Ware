from flask import Flask, request, jsonify, render_template, redirect, url_for, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management
DATABASE = "hardware.db"

# Database connection
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # User Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Products Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT NOT NULL
        )
    ''')

    # Cart Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# Home Route
@app.route('/')
def home():
    return render_template('signup.html')

# User Registration
@app.route('/signup', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO user (name, email, password) VALUES (?, ?, ?)', (name, email, password))
        conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 400

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    logo = "http://127.0.0.1:5500/hardware_corp/templates/images/trolley.png"
    user = "http://127.0.0.1:5500/hardware_corp/templates/images/user-286.png"
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']  # Store user ID in session
            return render_template('home.html')
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    return render_template('login.html', logo=logo)

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Shop Page - List Products
@app.route('/shop')
def shop():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('shop.html', products=products)

# Add Product to Cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'message': 'Login required!'}), 403

    data = request.json
    product_id = data.get('product_id')
    user_id = session['user_id']

    db = get_db()
    cursor = db.execute("SELECT * FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    existing_item = cursor.fetchone()

    if existing_item:
        db.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    else:
        db.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)", (user_id, product_id))

    db.commit()
    return jsonify({"message": "Product added to cart successfully!"})

# View Cart
@app.route('/cart')
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = get_db()
    cursor = db.execute("""
        SELECT products.id, products.name, products.price, products.image, cart.quantity 
        FROM cart 
        JOIN products ON cart.product_id = products.id 
        WHERE cart.user_id = ?
    """, (user_id,))
    cart_items = cursor.fetchall()
    return render_template('cart.html', cart_items=cart_items)

if __name__ == '__main__':
    app.run(debug=True)

