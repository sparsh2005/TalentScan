from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.resume_parser import ResumeParser
from app.services.database import DatabaseService, InMemoryDatabase
import os
import tempfile
from typing import Dict, Any

router = APIRouter()
resume_parser = ResumeParser()

# Use Supabase if credentials are available, otherwise use in-memory storage
if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"):
    db_service = DatabaseService()
else:
    db_service = InMemoryDatabase()

@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload and process a resume file (PDF or DOCX)
    """
    try:
        # Validate file type
        if file.content_type not in [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]:
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Parse resume and extract information
            candidate_info = await resume_parser.parse_resume(
                temp_file_path,
                file.content_type
            )

            # Store candidate information
            stored_candidate = await db_service.store_candidate(candidate_info)

            return {
                "message": "Resume processed successfully",
                "candidate": stored_candidate
            }

        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/candidates")
async def get_candidates():
    """
    Retrieve all candidates
    """
    try:
        candidates = await db_service.get_all_candidates()
        return {"candidates": candidates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 