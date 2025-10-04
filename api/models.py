from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

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