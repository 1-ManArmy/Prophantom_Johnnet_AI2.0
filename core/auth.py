"""
Authentication module for Prophantom Johnnet AI 2.0
"""

from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
import hashlib
import secrets
from core.database import execute_query, fetch_one

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return salt + password_hash.hex()

def verify_password(password, password_hash):
    """Verify password against hash"""
    salt = password_hash[:32]
    stored_hash = password_hash[32:]
    password_hash_check = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return stored_hash == password_hash_check.hex()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    data = request.get_json() if request.is_json else request.form
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = fetch_one('SELECT * FROM users WHERE username = ?', (username,))
    
    if user and verify_password(password, user['password_hash']):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'success': True, 'redirect': '/dashboard'})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    data = request.get_json() if request.is_json else request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': 'All fields required'}), 400
    
    # Check if user exists
    existing_user = fetch_one('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409
    
    # Create new user
    password_hash = hash_password(password)
    execute_query(
        'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
        (username, email, password_hash)
    )
    
    return jsonify({'success': True, 'message': 'User created successfully'})

@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('home'))

@auth_bp.route('/profile')
def profile():
    """User profile"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = fetch_one('SELECT username, email, created_at FROM users WHERE id = ?', (session['user_id'],))
    return render_template('auth/profile.html', user=user)

def login_required(f):
    """Decorator for routes that require authentication"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function