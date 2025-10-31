from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Carrier(str, Enum):
    VERIZON = "verizon"
    ATT = "att"
    TMOBILE = "tmobile"
    SPRINT = "sprint"
    US_CELLULAR = "us_cellular"

class NotificationPreferences(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    phone: str = Field(..., description="User's phone number (digits only)")
    sms_enabled: bool = Field(True, description="Whether SMS notifications are enabled")
    daily_digest: bool = Field(True, description="Whether to receive daily digest SMS")
    instant_alerts: bool = Field(False, description="Whether to receive instant alerts for new internships")
    
    # User's own Twilio credentials (optional - can use system defaults)
    twilio_account_sid: Optional[str] = Field(None, description="User's Twilio Account SID")
    twilio_auth_token: Optional[str] = Field(None, description="User's Twilio Auth Token")
    twilio_phone_number: Optional[str] = Field(None, description="User's Twilio Phone Number")

class Internship(BaseModel):
    """Model representing an internship posting"""
    id: str
    title: str
    company: str
    location: str
    description: str
    requirements: Optional[str] = None
    salary: Optional[str] = None
    duration: Optional[str] = None
    application_deadline: Optional[datetime] = None
    posted_date: datetime
    source_url: str
    source: str  # e.g., "indeed", "linkedin", "glassdoor"
    remote: Optional[bool] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# User Authentication Models
class User(BaseModel):
    """User model with account information"""
    id: str
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password_hash: str = Field(..., description="Hashed password")
    created_at: datetime = Field(default_factory=datetime.now, description="Account creation date")

class UserRegister(BaseModel):
    """Request model for user registration"""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")

class UserLogin(BaseModel):
    """Request model for user login"""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

class Token(BaseModel):
    """Response model for authentication token"""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str

class UserResponse(BaseModel):
    """Response model for user info (without password)"""
    id: str
    username: str
    created_at: datetime

# Saved Jobs Models
class SavedJob(BaseModel):
    """Model for a saved internship"""
    id: str
    user_id: str
    internship_id: str
    saved_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SavedJobCreate(BaseModel):
    """Request model for saving an internship"""
    internship_id: str

class SavedJobResponse(BaseModel):
    """Response model for saved job"""
    id: str
    internship_id: str
    saved_at: datetime
    internship: Internship  # The full internship data