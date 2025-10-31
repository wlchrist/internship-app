"""
Service for managing saved internships for users
"""
import sqlite3
from typing import List, Optional
from datetime import datetime
import secrets
from database import get_db_connection
from models import SavedJob, Internship
from services import InternshipService

class SavedJobsService:
    """Service for managing saved internships"""
    
    def __init__(self, internship_service: InternshipService):
        self.internship_service = internship_service
    
    def save_job(self, user_id: str, internship_id: str) -> Optional[SavedJob]:
        """Save an internship for a user"""
        try:
            # Check if already saved
            if self.is_job_saved(user_id, internship_id):
                return None
            
            # Create saved job
            saved_job_id = secrets.token_urlsafe(16)
            saved_at = datetime.now()
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO saved_jobs (id, user_id, internship_id, saved_at)
                VALUES (?, ?, ?, ?)
            """, (saved_job_id, user_id, internship_id, saved_at.isoformat()))
            conn.commit()
            conn.close()
            
            return SavedJob(
                id=saved_job_id,
                user_id=user_id,
                internship_id=internship_id,
                saved_at=saved_at
            )
        except sqlite3.IntegrityError:
            # Already saved (race condition)
            return None
    
    def unsave_job(self, user_id: str, internship_id: str) -> bool:
        """Remove a saved internship for a user"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM saved_jobs
                WHERE user_id = ? AND internship_id = ?
            """, (user_id, internship_id))
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return deleted_count > 0
        except Exception:
            return False
    
    def is_job_saved(self, user_id: str, internship_id: str) -> bool:
        """Check if an internship is saved by a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM saved_jobs
            WHERE user_id = ? AND internship_id = ?
        """, (user_id, internship_id))
        result = cursor.fetchone()
        conn.close()
        
        return result['count'] > 0 if result else False
    
    async def get_saved_jobs(self, user_id: str) -> List[Internship]:
        """Get all saved internships for a user with full internship data"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT internship_id, saved_at
            FROM saved_jobs
            WHERE user_id = ?
            ORDER BY saved_at DESC
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        # Get all internships
        all_internships = await self.internship_service.get_internships()
        
        # Create a map of internship IDs to internships
        internship_map = {internship.id: internship for internship in all_internships}
        
        # Get saved internships in order they were saved
        saved_internships = []
        for row in rows:
            internship_id = row['internship_id']
            if internship_id in internship_map:
                saved_internships.append(internship_map[internship_id])
        
        return saved_internships
    
    def get_saved_job_ids(self, user_id: str) -> List[str]:
        """Get list of internship IDs saved by a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT internship_id
            FROM saved_jobs
            WHERE user_id = ?
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [row['internship_id'] for row in rows]

