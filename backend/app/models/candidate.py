from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class Education(BaseModel):
    school: str
    degree: str
    dates: str

class Candidate(BaseModel):
    id: Optional[str] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    education_history: List[Education]
    work_experience_summary: str
    skills: List[str]
    current_position: str
    years_of_experience: float
    created_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "+1-123-456-7890",
                "education_history": [
                    {
                        "school": "Stanford University",
                        "degree": "MS Computer Science",
                        "dates": "2018-2020"
                    }
                ],
                "work_experience_summary": "5 years of software development experience...",
                "skills": ["Python", "Machine Learning", "FastAPI"],
                "current_position": "Senior Software Engineer",
                "years_of_experience": 5.0
            }
        } 