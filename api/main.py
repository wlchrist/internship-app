from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import asyncio
import logging
from models import Internship, NotificationPreferences
from services import InternshipService
from notification_service import NotificationService

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)