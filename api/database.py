"""
Database module for persistent storage using SQLite
Pure Python - no external dependencies required
"""
import sqlite3
import os
from typing import Optional, List
from datetime import datetime
from contextlib import contextmanager
from models import User

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), "internship_app.db")

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    # Create index on username for faster lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_username ON users(username)
    """)
    
    # Create saved_jobs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            internship_id TEXT NOT NULL,
            saved_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, internship_id)
        )
    """)
    
    # Create indexes for faster lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_saved_jobs_user_id ON saved_jobs(user_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_saved_jobs_internship_id ON saved_jobs(internship_id)
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")

def user_from_row(row: sqlite3.Row) -> User:
    """Convert a database row to a User model"""
    return User(
        id=row['id'],
        username=row['username'],
        password_hash=row['password_hash'],
        created_at=datetime.fromisoformat(row['created_at'])
    )

