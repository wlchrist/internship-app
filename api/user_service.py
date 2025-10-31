import bcrypt
from typing import Optional, List
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
import secrets
from models import User
from database import get_db_connection, init_database, user_from_row
import sqlite3

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

class UserService:
    """Service for user registration, authentication, and management"""
    
    def __init__(self):
        # Initialize database on startup
        init_database()
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against a hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def create_user(self, username: str, password: str) -> Optional[User]:
        """Create a new user account"""
        # Validate username (alphanumeric and underscores only)
        if not username.replace('_', '').isalnum():
            return None
        
        # Check if username already exists
        if self.get_user_by_username(username):
            return None
        
        # Create user
        user_id = secrets.token_urlsafe(16)
        password_hash = self.hash_password(password)
        created_at = datetime.now()
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (id, username, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            """, (user_id, username, password_hash, created_at.isoformat()))
            conn.commit()
            conn.close()
            
            return User(
                id=user_id,
                username=username,
                password_hash=password_hash,
                created_at=created_at
            )
        except sqlite3.IntegrityError:
            # Username already exists (race condition)
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return user_from_row(row)
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return user_from_row(row)
        return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password"""
        user = self.get_user_by_username(username)
        if not user:
            return None
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        return user
    
    def create_access_token(self, user: User) -> str:
        """Create a JWT access token for a user"""
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": user.id,
            "username": user.username,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    def get_user_from_token(self, token: str) -> Optional[User]:
        """Get a user from a JWT token"""
        payload = self.verify_token(token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        return self.get_user_by_id(user_id)

