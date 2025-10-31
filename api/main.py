from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn
import asyncio
import logging
from models import Internship, NotificationPreferences, UserRegister, UserLogin, Token, UserResponse, SavedJobCreate, SavedJobResponse
from services import InternshipService
from notification_service import NotificationService
from user_service import UserService
from saved_jobs_service import SavedJobsService

app = FastAPI(title="Internship Aggregator API", version="1.0.0")

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
internship_service = InternshipService()
notification_service = NotificationService()
user_service = UserService()
saved_jobs_service = SavedJobsService(internship_service)

# Background task for periodic refresh and notifications
async def periodic_refresh():
    while True:
        try:
            logging.info("Starting scheduled internship refresh...")
            await internship_service.fetch_and_store_internships()
            
            # Send daily digest to subscribers
            internships = await internship_service.get_internships()
            if internships:
                sent_count = await notification_service.send_daily_digest(internships)
                logging.info(f"Sent daily digest to {sent_count} subscribers")
            
            logging.info("Scheduled refresh completed. Next refresh in 24 hours.")
            await asyncio.sleep(24 * 60 * 60)  # 24 hours
            
        except Exception as e:
            logging.error(f"Error in periodic refresh: {e}")
            await asyncio.sleep(60 * 60)  # Wait 1 hour before retrying

@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    logging.info("Application startup: Initializing services...")
    
    # Initial data load
    await internship_service.fetch_and_store_internships()
    logging.info("Initial internship data loaded.")
    
    # Start background task
    asyncio.create_task(periodic_refresh())
    logging.info("Background tasks started.")

@app.get("/")
async def root():
    return {"message": "Internship Aggregator API"}

@app.get("/internships", response_model=List[Internship])
async def get_internships():
    """Get all available internship postings"""
    try:
        internships = await internship_service.get_internships()
        return internships
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching internships: {str(e)}")

@app.get("/internships/refresh")
async def refresh_internships():
    """Manually trigger a refresh of internship data"""
    try:
        await internship_service.fetch_and_store_internships()
        return {"message": "Internships refreshed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing internships: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserRegister):
    """Register a new user account"""
    try:
        # Validate username format
        if not user_data.username.replace('_', '').isalnum():
            raise HTTPException(
                status_code=400,
                detail="Username must contain only letters, numbers, and underscores"
            )
        
        # Create user
        user = user_service.create_user(user_data.username, user_data.password)
        
        if not user:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )
        
        logging.info(f"New user registered: {user.username}")
        
        return UserResponse(
            id=user.id,
            username=user.username,
            created_at=user.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail=f"Error registering user: {str(e)}")

@app.post("/auth/login", response_model=Token)
async def login_user(user_data: UserLogin):
    """Login and receive an authentication token"""
    try:
        # Authenticate user
        user = user_service.authenticate_user(user_data.username, user_data.password)
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
        
        # Create access token
        access_token = user_service.create_access_token(user)
        
        logging.info(f"User logged in: {user.username}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            username=user.username
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error logging in user: {e}")
        raise HTTPException(status_code=500, detail=f"Error logging in: {str(e)}")

async def get_current_user(authorization: Optional[str] = Header(None)):
    """Helper function to get current user from token (for dependencies)"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    # Get user from token
    user = user_service.get_user_from_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information from token"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        created_at=current_user.created_at
    )

# Notification endpoints
@app.post("/notifications/subscribe")
async def subscribe_notifications(preferences: NotificationPreferences):
    """Subscribe to email/SMS notifications"""
    try:
        success = await notification_service.subscribe_user(preferences)
        if success:
            return {"message": "Successfully subscribed to notifications", "subscriber_count": notification_service.get_subscriber_count()}
        else:
            raise HTTPException(status_code=500, detail="Failed to subscribe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subscribing: {str(e)}")

@app.post("/notifications/unsubscribe")
async def unsubscribe_notifications(email: str):
    """Unsubscribe from notifications"""
    try:
        success = await notification_service.unsubscribe_user(email)
        if success:
            return {"message": "Successfully unsubscribed from notifications"}
        else:
            raise HTTPException(status_code=500, detail="Failed to unsubscribe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error unsubscribing: {str(e)}")

@app.get("/notifications/subscribers")
async def get_subscribers():
    """Get subscriber count and info (admin endpoint)"""
    try:
        subscribers = notification_service.get_subscribers()
        return {
            "total_subscribers": len(subscribers),
            "subscribers": [
                {
                    "email": sub.email,
                    "sms_enabled": sub.sms_enabled,
                    "daily_digest": sub.daily_digest,
                    "instant_alerts": sub.instant_alerts
                }
                for sub in subscribers
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting subscribers: {str(e)}")

@app.post("/notifications/send-test")
async def send_test_notification(email: str):
    """Send a test notification (admin endpoint)"""
    try:
        # Create test internship data
        test_internships = [
            Internship(
                id="test_1",
                title="Software Engineering Intern",
                company="Test Company",
                location="Remote",
                description="This is a test internship for notification testing.",
                salary="$25-30/hour",
                posted_date="2025-01-01T00:00:00",
                source_url="https://example.com",
                source="test"
            )
        ]
        
        # Send test digest
        sent_count = await notification_service.send_daily_digest(test_internships)
        return {"message": f"Test notification sent to {sent_count} subscribers"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending test notification: {str(e)}")

# Saved Jobs endpoints
@app.post("/saved-jobs", response_model=SavedJobResponse)
async def save_job(
    saved_job: SavedJobCreate,
    current_user = Depends(get_current_user)
):
    """Save an internship for the current user"""
    try:
        saved = saved_jobs_service.save_job(current_user.id, saved_job.internship_id)
        
        if not saved:
            raise HTTPException(
                status_code=400,
                detail="Internship already saved or not found"
            )
        
        # Get the full internship data
        internships = await internship_service.get_internships()
        internship = next((i for i in internships if i.id == saved_job.internship_id), None)
        
        if not internship:
            raise HTTPException(
                status_code=404,
                detail="Internship not found"
            )
        
        logging.info(f"User {current_user.username} saved internship {saved_job.internship_id}")
        
        return SavedJobResponse(
            id=saved.id,
            internship_id=saved.internship_id,
            saved_at=saved.saved_at,
            internship=internship
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error saving job: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving job: {str(e)}")

@app.delete("/saved-jobs/{internship_id}")
async def unsave_job(
    internship_id: str,
    current_user = Depends(get_current_user)
):
    """Remove a saved internship for the current user"""
    try:
        success = saved_jobs_service.unsave_job(current_user.id, internship_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Saved job not found"
            )
        
        logging.info(f"User {current_user.username} unsaved internship {internship_id}")
        
        return {"message": "Job unsaved successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error unsaving job: {e}")
        raise HTTPException(status_code=500, detail=f"Error unsaving job: {str(e)}")

@app.get("/saved-jobs", response_model=List[Internship])
async def get_saved_jobs(current_user = Depends(get_current_user)):
    """Get all saved internships for the current user"""
    try:
        saved_internships = await saved_jobs_service.get_saved_jobs(current_user.id)
        return saved_internships
    except Exception as e:
        logging.error(f"Error getting saved jobs: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting saved jobs: {str(e)}")

@app.get("/saved-jobs/check/{internship_id}")
async def check_saved_job(
    internship_id: str,
    current_user = Depends(get_current_user)
):
    """Check if an internship is saved by the current user"""
    try:
        is_saved = saved_jobs_service.is_job_saved(current_user.id, internship_id)
        return {"is_saved": is_saved}
    except Exception as e:
        logging.error(f"Error checking saved job: {e}")
        raise HTTPException(status_code=500, detail=f"Error checking saved job: {str(e)}")

@app.get("/saved-jobs/ids")
async def get_saved_job_ids(current_user = Depends(get_current_user)):
    """Get list of saved internship IDs for the current user"""
    try:
        saved_ids = saved_jobs_service.get_saved_job_ids(current_user.id)
        return {"saved_job_ids": saved_ids}
    except Exception as e:
        logging.error(f"Error getting saved job IDs: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting saved job IDs: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)