"""
Core database module for Prophantom Johnnet AI 2.0
"""

import sqlite3
from flask import g, current_app
import os

DATABASE = 'prophantom_ai.db'

def get_db():
    """Get database connection"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    """Initialize database"""
    with app.app_context():
        db = get_db()
        
        # Create users table
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Create sessions table
        db.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                agent_type TEXT NOT NULL,
                session_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create conversations table
        db.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                agent_type TEXT NOT NULL,
                message TEXT NOT NULL,
                response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create agent_analytics table
        db.execute('''
            CREATE TABLE IF NOT EXISTS agent_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_type TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                performance_metrics TEXT
            )
        ''')
        
        db.commit()
    
    # Register teardown handler
    app.teardown_appcontext(close_db)

def execute_query(query, params=None):
    """Execute a database query"""
    db = get_db()
    cursor = db.execute(query, params or ())
    db.commit()
    return cursor

def fetch_one(query, params=None):
    """Fetch single row"""
    db = get_db()
    return db.execute(query, params or ()).fetchone()

def fetch_all(query, params=None):
    """Fetch all rows"""
    db = get_db()
    return db.execute(query, params or ()).fetchall()