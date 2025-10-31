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
        # Fantastic Jobs API configuration
        self.api_key = os.getenv("RAPIDAPI_KEY", "b55b10072cmshaa3327eadfbb864p1b5030jsnd01b971a8dff")
        self.api_host = "internships-api.p.rapidapi.com"
        # More inclusive query to get more CS internship results
        self.api_url = "https://internships-api.p.rapidapi.com/active-jb-7d?location_filter=United+States&description_filter=%28intern+OR+internship+OR+co-op%29+AND+%28software+OR+programming+OR+development+OR+engineering+OR+computer+science+OR+data+science+OR+machine+learning+OR+AI+OR+artificial+intelligence%29&offset=0&advanced_title_filter=%28%27Software+Engineering%27+%7C+%27Full-Stack+Developer%27+%7C+%27Front-End+Engineering%27+%7C+%27Back-End+Engineering%27+%7C+%27Site+Reliability%27+%7C+SRE+%7C+%27iOS+Software%27+%7C+%27Android+Software%27+%7C+%27AI+Research%27+%7C+%27AI+Scientist%27+%7C+%27Machine+Learning+Engineer%27+%7C+%27Data+Science%27+%7C+%27Computer+Vision%27+%7C+%27Deep+Learning%27+%7C+NLP+%7C+%27Natural+Language+Processing%27+%7C+%27Offensive+Security%27+%7C+%27AI+Cyber+Security%27+%7C+%27Cloud+Engineer%27+%7C+AWS+%7C+Azure+%7C+DevOps+%7C+Platform+%7C+%27Data+Infrastructure%27+%7C+%27Quantitative+Developer%27+%7C+%27Quantitative+Research%27+%7C+%27Embedded+Software%27+%7C+Autonomy+%7C+Robotics+%7C+Blockchain+%7C+Web3+%7C+AR+%7C+VR+%7C+XR+%7C+%27Growth+Data%27+%7C+Analytics+%7C+%27Information+Security%27+%7C+Risk%29+%26+Intern%3A*"
        
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
            print("=" * 60)
            print("Fetching internships from Fantastic Jobs API...")
            print("=" * 60)
            
            # Try to fetch from Fantastic Jobs API with multiple calls for more results
            all_internships = []
            
            # Make multiple API calls with different offsets to get more results
            for offset in [0, 10, 20]:  # Get more results (3 batches)
                print(f"\nFetching batch at offset {offset}...")
                internships = await self._fetch_from_fantastic_jobs_api_with_offset(offset)
                all_internships.extend(internships)
                print(f"✓ Fetched {len(internships)} internships from offset {offset}")
            
            # Remove duplicates based on job ID
            unique_internships = []
            seen_ids = set()
            for internship in all_internships:
                if internship.id not in seen_ids:
                    unique_internships.append(internship)
                    seen_ids.add(internship.id)
            
            if unique_internships:
                self.internships_cache = unique_internships
                print(f"\n✓ Successfully fetched {len(unique_internships)} unique internships from Fantastic Jobs API")
                print(f"✓ Companies: {', '.join(set(internship.company for internship in unique_internships[:10]))}")
            else:
                # No internships found from API - log warning but don't use mock data
                print(f"\n⚠ WARNING: No internships found from Fantastic Jobs API")
                print("⚠ Possible reasons:")
                print("  - API rate limit exceeded")
                print("  - API key invalid or expired")
                print("  - Network connection issue")
                print("  - API endpoint changed")
                print(f"\n⚠ Keeping existing cache ({len(self.internships_cache)} internships)")
                # Don't fallback to mock data - use empty cache or existing cache
                if not self.internships_cache:
                    print("⚠ No cached data available - will return empty list")
                    self.internships_cache = []

            self.last_fetch = datetime.now()
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ ERROR fetching internships: {e}")
            import traceback
            traceback.print_exc()
            # Keep existing cache if fetch fails
            if not self.internships_cache:
                print("⚠ No cached data available - will return empty list")
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
    
    async def _fetch_from_fantastic_jobs_api_with_offset(self, offset: int) -> List[Internship]:
        """Fetch internships from Fantastic Jobs API with specific offset"""
        headers = {
            "x-rapidapi-host": self.api_host,
            "x-rapidapi-key": self.api_key
        }

        # Create URL with specific offset
        base_url = "https://internships-api.p.rapidapi.com/active-jb-7d"
        params = {
            "location_filter": "United States",
            "description_filter": "(intern OR internship OR co-op) AND (software OR programming OR development OR engineering OR computer science OR data science OR machine learning OR AI OR artificial intelligence)",
            "offset": str(offset),
            "advanced_title_filter": "('Software Engineering' | 'Full-Stack Developer' | 'Front-End Engineering' | 'Back-End Engineering' | 'Site Reliability' | SRE | 'iOS Software' | 'Android Software' | 'AI Research' | 'AI Scientist' | 'Machine Learning Engineer' | 'Data Science' | 'Computer Vision' | 'Deep Learning' | NLP | 'Natural Language Processing' | 'Cyber Security' | 'Cloud Engineer' | AWS | Azure | DevOps | Platform | 'Data Infrastructure' | 'Quantitative Developer' | 'Quantitative Research' | 'Embedded Software' | Autonomy | Robotics | Blockchain | Web3 | AR | VR | XR | 'Information Security' | 'Security Engineer' | 'Software Developer' | Programmer) & Intern:*"
        }
        
        # Build URL with parameters
        url = base_url + "?" + "&".join([f"{k}={v}" for k, v in params.items()])

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                print(f"  → API Request: {base_url}?offset={offset}")
                print(f"  → Headers: x-rapidapi-host={self.api_host}, x-rapidapi-key={'*' * 10 + self.api_key[-10:]}")
                
                response = await client.get(url, headers=headers)
                
                # Log response status
                print(f"  → Response Status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"  → Response Body: {response.text[:200]}")
                
                response.raise_for_status()

                data = response.json()
                
                # Handle different response formats
                if isinstance(data, dict):
                    # Some APIs return data wrapped in a dict
                    if 'data' in data:
                        data = data['data']
                    elif 'results' in data:
                        data = data['results']
                    elif 'jobs' in data:
                        data = data['jobs']
                    else:
                        print(f"  ⚠ Unexpected response format: {list(data.keys())[:5]}")
                        data = []
                
                if isinstance(data, list):
                    print(f"  → Received {len(data)} raw job listings")
                    # Transform API response to our Internship model
                    internships = self._transform_api_response(data)
                    print(f"  → After filtering: {len(internships)} CS internships")
                    return internships
                else:
                    print(f"  ⚠ Unexpected response type: {type(data)}")
                    print(f"  ⚠ Response sample: {str(data)[:200]}")
                    return []

        except httpx.HTTPStatusError as e:
            print(f"  ❌ HTTP Status Error (offset {offset}): {e.response.status_code}")
            print(f"  → Response: {e.response.text[:200] if hasattr(e.response, 'text') else 'No response body'}")
            return []
        except httpx.HTTPError as e:
            print(f"  ❌ HTTP Error (offset {offset}): {e}")
            return []
        except Exception as e:
            print(f"  ❌ Error fetching from Fantastic Jobs API (offset {offset}): {e}")
            import traceback
            traceback.print_exc()
            return []

    async def _fetch_from_fantastic_jobs_api(self) -> List[Internship]:
        """Fetch internships from Fantastic Jobs API (legacy method)"""
        return await self._fetch_from_fantastic_jobs_api_with_offset(0)
    
    def _transform_api_response(self, api_data: Any) -> List[Internship]:
        """Transform Fantastic Jobs API response to our Internship model"""
        internships = []
        
        # The API returns a list of job objects directly
        jobs = api_data if isinstance(api_data, list) else []
        
        print(f"Processing {len(jobs)} jobs from API response")
        
        for i, job in enumerate(jobs):
            try:
                # Debug: print job structure
                if i == 0:  # Only print first job structure
                    print(f"First job structure: {json.dumps(job, indent=2)[:300]}...")
                
                # Extract fields from the actual API response format
                title = job.get('title', f"Internship Position {i+1}")
                company = job.get('organization', "Unknown Company")
                
                # Handle location - the API has complex location data
                locations_derived = job.get('locations_derived', [])
                location = locations_derived[0] if locations_derived else "Location TBD"
                
                # Get organization description as job description
                description = job.get('linkedin_org_description', "No description available")
                if len(description) > 500:
                    description = description[:500] + "..."

                # Define keywords for exclusions (non-CS fields and senior positions)
                exclude_keywords = [
                    'accountant', 'accounting', 'finance', 'marketing', 'sales', 'hr',
                    'human resources', 'business analyst', 'management consultant',
                    'mechanical engineer', 'civil engineer', 'electrical engineer', 
                    'chemical engineer', 'biomedical engineer', 'nurse', 'teacher',
                    'legal', 'lawyer', 'paralegal', 'medical', 'healthcare', 'pharmacy',
                    'senior manager', 'lead', 'principal', 'staff', 'director', 'vp',
                    'vice president', 'head of', 'chief', 'executive', 'sr.',
                    # Add non-CS risk/analytics roles
                    'model risk', 'risk management', 'credit risk', 'market risk',
                    'financial risk', 'operational risk', 'compliance', 'audit',
                    'business analytics', 'financial analytics', 'business intelligence analyst',
                    'product manager', 'project manager', 'scrum master', 'product owner'
                ]
                
                # Keywords that indicate internship/entry-level positions
                internship_keywords = [
                    'intern', 'internship', 'co-op', 'coop', 'entry level', 'entry-level',
                    'new grad', 'recent grad', 'junior', 'jr.', 'associate', 'trainee',
                    'summer intern', 'winter intern', 'fall intern', 'spring intern'
                ]

                # CS-related keywords that must be present (positive inclusion)
                cs_include_keywords = [
                    'software', 'programming', 'developer', 'engineer', 'engineering',
                    'data science', 'machine learning', 'ai', 'artificial intelligence',
                    'computer science', 'cs', 'coding', 'algorithm', 'technical',
                    'technology', 'tech', 'full stack', 'full-stack', 'frontend', 'front-end',
                    'backend', 'back-end', 'devops', 'cloud', 'aws', 'azure', 'gcp',
                    'python', 'java', 'javascript', 'c++', 'c#', 'react', 'node',
                    'database', 'sql', 'nosql', 'api', 'microservices', 'kubernetes',
                    'docker', 'git', 'version control', 'agile', 'scrum', 'sdlc',
                    'data structure', 'computer vision', 'nlp', 'natural language processing',
                    'deep learning', 'neural network', 'blockchain', 'web3', 'cryptocurrency',
                    'cyber security', 'information security', 'security engineer',
                    'quantitative', 'quant', 'embedded', 'robotics', 'autonomy',
                    'ios', 'android', 'mobile development', 'ar', 'vr', 'xr'
                ]

                title_lower = title.lower()
                desc_lower = description.lower()
                full_text = f"{title_lower} {desc_lower}"

                # Check for exclusions first (most restrictive)
                is_excluded = any(keyword in title_lower or keyword in desc_lower for keyword in exclude_keywords)
                if is_excluded:
                    if i < 3:  # Debug for first 3 jobs
                        print(f"Job {i+1}: '{title}' - EXCLUDED (non-CS or senior position)")
                    continue

                # Check if it's actually an internship/entry-level position
                is_internship = any(keyword in title_lower for keyword in internship_keywords)
                if not is_internship:
                    if i < 3:  # Debug for first 3 jobs
                        print(f"Job {i+1}: '{title}' - EXCLUDED (not an internship)")
                    continue

                # POSITIVE CHECK: Must contain at least one CS-related keyword
                has_cs_keyword = any(keyword in full_text for keyword in cs_include_keywords)
                if not has_cs_keyword:
                    if i < 3:  # Debug for first 3 jobs
                        print(f"Job {i+1}: '{title}' - EXCLUDED (no CS-related keywords)")
                    continue

                # All checks passed - this is a CS internship
                if i < 3:  # Debug for first 3 jobs
                    print(f"Job {i+1}: '{title}' - ACCEPTED (CS internship)")
                
                # Handle salary data
                salary_raw = job.get('salary_raw', {})
                salary = "Competitive"
                if salary_raw and isinstance(salary_raw, dict):
                    value = salary_raw.get('value', {})
                    if isinstance(value, dict):
                        min_val = value.get('minValue')
                        max_val = value.get('maxValue')
                        unit = value.get('unitText', 'HOUR')
                        if min_val and max_val:
                            salary = f"${min_val}-{max_val}/{unit.lower()}"
                        elif min_val:
                            salary = f"${min_val}/{unit.lower()}"
                
                # Handle employment type
                employment_types = job.get('employment_type', [])
                job_type = "Internship"
                if employment_types and 'INTERN' in employment_types:
                    job_type = "Internship"
                elif employment_types:
                    job_type = employment_types[0].title()
                
                # Handle remote work
                remote = job.get('remote_derived', False)
                
                # Handle posted date
                posted_date = job.get('date_posted', datetime.now().strftime("%Y-%m-%d"))
                if posted_date and 'T' in posted_date:
                    posted_date = posted_date.split('T')[0]
                
                internship = Internship(
                    id=str(job.get('id', f"fantastic_jobs_{i}")),
                    title=title,
                    company=company,
                    location=location,
                    description=description,
                    requirements="See job description for requirements",
                    salary=salary,
                    duration="TBD",
                    posted_date=posted_date,
                    source_url=job.get('url', f"https://fantasticjobs.com/job/{i}"),
                    source="Fantastic Jobs",
                    remote=remote,
                    job_type=job_type
                )
                
                internships.append(internship)
                
            except Exception as e:
                print(f"Error processing job {i}: {e}")
                continue
        
        return internships
    
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