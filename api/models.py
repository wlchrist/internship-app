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
    job_type: Optional[str] = None  # "full-time", "part-time", "contract"
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }