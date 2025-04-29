from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.resume_parser import ResumeParser
from app.services.database import DatabaseService, InMemoryDatabase
import os
import tempfile
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
resume_parser = ResumeParser()

# Use Supabase if credentials are available, otherwise use in-memory storage
if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"):
    db_service = DatabaseService()
else:
    db_service = InMemoryDatabase()
    logger.warning("Using in-memory storage as Supabase credentials are not configured")

@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload and process a resume file (PDF or DOCX)
    """
    try:
        # Log file details
        logger.info(f"Received file: {file.filename}, Content-Type: {file.content_type}")

        # Validate file type
        if file.content_type not in [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]:
            logger.error(f"Invalid file type: {file.content_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Only PDF and DOCX files are supported."
            )

        # Create temp directory if it doesn't exist
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Save uploaded file temporarily
        temp_file_path = os.path.join(temp_dir, file.filename)
        try:
            content = await file.read()
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(content)
            
            logger.info(f"File saved temporarily at: {temp_file_path}")

            # Parse resume and extract information
            logger.info("Starting resume parsing...")
            candidate_info = await resume_parser.parse_resume(
                temp_file_path,
                file.content_type
            )
            logger.info("Resume parsing completed successfully")

            # Store candidate information
            logger.info("Storing candidate information...")
            stored_candidate = await db_service.store_candidate(candidate_info)
            logger.info("Candidate information stored successfully")

            return {
                "message": "Resume processed successfully",
                "candidate": stored_candidate
            }

        except Exception as e:
            logger.error(f"Error processing resume: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                logger.info(f"Temporary file removed: {temp_file_path}")

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/candidates")
async def get_candidates():
    """
    Retrieve all candidates
    """
    try:
        candidates = await db_service.get_all_candidates()
        return {"candidates": candidates}
    except Exception as e:
        logger.error(f"Error retrieving candidates: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 