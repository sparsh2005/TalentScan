from fastapi import APIRouter, HTTPException
from app.services.chatbot import ChatbotService
from app.services.database import DatabaseService, InMemoryDatabase
from pydantic import BaseModel
import os

router = APIRouter()
chatbot = ChatbotService()

# Use Supabase if credentials are available, otherwise use in-memory storage
if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"):
    db_service = DatabaseService()
else:
    db_service = InMemoryDatabase()

class ChatQuery(BaseModel):
    query: str
    role: str = None  # Optional field for role-specific ranking

@router.post("/chat")
async def chat_with_hr(chat_query: ChatQuery):
    """
    Chat with HR assistant about candidates
    """
    try:
        # Get all candidates from database
        candidates = await db_service.get_all_candidates()
        
        if not candidates:
            return {
                "response": "No candidates found in the database. Please upload some resumes first."
            }

        # If role is specified, use ranking functionality
        if chat_query.role:
            response = await chatbot.rank_candidates(candidates, chat_query.role)
        else:
            response = await chatbot.get_response(chat_query.query, candidates)

        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rank")
async def rank_candidates(chat_query: ChatQuery):
    """
    Rank candidates for a specific role
    """
    if not chat_query.role:
        raise HTTPException(status_code=400, detail="Role must be specified for ranking")

    try:
        candidates = await db_service.get_all_candidates()
        
        if not candidates:
            return {
                "response": "No candidates found in the database. Please upload some resumes first."
            }

        response = await chatbot.rank_candidates(candidates, chat_query.role)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 