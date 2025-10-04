from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from models import Internship
from services import InternshipService

app = FastAPI(title="Internship Aggregator API", version="1.0.0")

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the internship service
internship_service = InternshipService()

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)