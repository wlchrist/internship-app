import httpx
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import json
import os
from models import Internship

class InternshipService:
    """Service to fetch and manage internship data"""
    
    def __init__(self):
        self.internships_cache: List[Internship] = []
        self.last_fetch: datetime = None
        
    async def get_internships(self) -> List[Internship]:
        """Get internships from cache or fetch if needed"""
        if not self.internships_cache or self._should_refresh():
            await self.fetch_and_store_internships()
        return self.internships_cache
    
    def _should_refresh(self) -> bool:
        """Check if data should be refreshed (24 hours)"""
        if not self.last_fetch:
            return True
        
        time_diff = datetime.now() - self.last_fetch
        return time_diff.total_seconds() > 24 * 60 * 60  # 24 hours
    
    async def fetch_and_store_internships(self):
        """Fetch internships from external APIs and store them"""
        try:
            # For now, we'll use mock data since we don't have real API access
            # In a real implementation, you would call actual job board APIs
            mock_internships = await self._fetch_mock_internships()
            
            self.internships_cache = mock_internships
            self.last_fetch = datetime.now()
            
            print(f"Fetched {len(mock_internships)} internships")
            
        except Exception as e:
            print(f"Error fetching internships: {e}")
            # Keep existing cache if fetch fails
            if not self.internships_cache:
                self.internships_cache = []
    
    async def _fetch_mock_internships(self) -> List[Internship]:
        """Generate mock internship data for demonstration"""
        # This simulates fetching from multiple sources
        mock_data = [
            {
                "id": "internship_1",
                "title": "Software Engineering Intern",
                "company": "TechCorp Inc.",
                "location": "San Francisco, CA",
                "description": "Join our engineering team and work on cutting-edge web applications. You'll collaborate with senior engineers on real projects.",
                "requirements": "Computer Science major, Python/JavaScript experience, Git knowledge",
                "salary": "$25-30/hour",
                "duration": "3 months",
                "posted_date": datetime.now(),
                "source_url": "https://example.com/job/1",
                "source": "mock_api",
                "remote": False,
                "job_type": "full-time"
            },
            {
                "id": "internship_2", 
                "title": "Data Science Intern",
                "company": "DataFlow Solutions",
                "location": "Remote",
                "description": "Work with our data team to analyze user behavior and build machine learning models for product recommendations.",
                "requirements": "Statistics/Data Science background, Python/R, SQL experience",
                "salary": "$22-28/hour",
                "duration": "6 months",
                "posted_date": datetime.now(),
                "source_url": "https://example.com/job/2",
                "source": "mock_api",
                "remote": True,
                "job_type": "full-time"
            },
            {
                "id": "internship_3",
                "title": "Frontend Development Intern",
                "company": "WebStudio",
                "location": "New York, NY",
                "description": "Help build responsive web interfaces using React and modern CSS frameworks. Work on user-facing features.",
                "requirements": "HTML/CSS/JavaScript, React experience preferred, UI/UX interest",
                "salary": "$20-25/hour",
                "duration": "4 months",
                "posted_date": datetime.now(),
                "source_url": "https://example.com/job/3",
                "source": "mock_api",
                "remote": False,
                "job_type": "part-time"
            },
            {
                "id": "internship_4",
                "title": "DevOps Engineering Intern",
                "company": "CloudTech",
                "location": "Austin, TX",
                "description": "Learn cloud infrastructure, CI/CD pipelines, and containerization technologies like Docker and Kubernetes.",
                "requirements": "Linux knowledge, scripting experience, cloud platforms interest",
                "salary": "$24-32/hour",
                "duration": "5 months",
                "posted_date": datetime.now(),
                "source_url": "https://example.com/job/4",
                "source": "mock_api",
                "remote": True,
                "job_type": "full-time"
            },
            {
                "id": "internship_5",
                "title": "Product Management Intern",
                "company": "StartupXYZ",
                "location": "Seattle, WA",
                "description": "Work with product managers to define features, analyze user feedback, and coordinate with engineering teams.",
                "requirements": "Business/Engineering background, analytical skills, communication skills",
                "salary": "$18-24/hour",
                "duration": "3 months",
                "posted_date": datetime.now(),
                "source_url": "https://example.com/job/5",
                "source": "mock_api",
                "remote": False,
                "job_type": "full-time"
            }
        ]
        
        return [Internship(**data) for data in mock_data]
    
    async def _fetch_from_real_api(self, api_url: str, headers: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """Template for fetching from real APIs"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(api_url, headers=headers or {})
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error fetching from {api_url}: {e}")
                return []
            except Exception as e:
                print(f"Error fetching from {api_url}: {e}")
                return []