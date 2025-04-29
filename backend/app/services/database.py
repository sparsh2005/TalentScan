from supabase import create_client
from typing import Dict, List, Any
from app.core.config import settings
from app.models.candidate import Candidate

class DatabaseService:
    def __init__(self):
        self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.table = "candidates"

    async def store_candidate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store candidate information in Supabase"""
        try:
            response = self.supabase.table(self.table).insert(candidate_data).execute()
            return response.data[0]
        except Exception as e:
            raise Exception(f"Error storing candidate: {str(e)}")

    async def get_all_candidates(self) -> List[Dict[str, Any]]:
        """Retrieve all candidates from the database"""
        try:
            response = self.supabase.table(self.table).select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error retrieving candidates: {str(e)}")

    async def search_candidates(self, query: str) -> List[Dict[str, Any]]:
        """Search candidates based on skills or experience"""
        try:
            # Basic search implementation - can be enhanced based on requirements
            response = self.supabase.table(self.table)\
                .select("*")\
                .or_(f"skills.cs.{query},work_experience_summary.ilike.%{query}%")\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error searching candidates: {str(e)}")

    async def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        """Retrieve a specific candidate by ID"""
        try:
            response = self.supabase.table(self.table)\
                .select("*")\
                .eq("id", candidate_id)\
                .single()\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error retrieving candidate: {str(e)}")

# Initialize in-memory storage as fallback
class InMemoryDatabase:
    def __init__(self):
        self.candidates: List[Dict[str, Any]] = []
        self.counter = 0

    async def store_candidate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        self.counter += 1
        candidate_data["id"] = str(self.counter)
        self.candidates.append(candidate_data)
        return candidate_data

    async def get_all_candidates(self) -> List[Dict[str, Any]]:
        return self.candidates

    async def search_candidates(self, query: str) -> List[Dict[str, Any]]:
        query = query.lower()
        return [
            c for c in self.candidates
            if query in str(c.get("skills", [])).lower() or
            query in c.get("work_experience_summary", "").lower()
        ]

    async def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        for candidate in self.candidates:
            if candidate["id"] == candidate_id:
                return candidate
        return None 