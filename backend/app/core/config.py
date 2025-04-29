from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "TalentScan"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # LLM Configuration
    EXTRACTION_PROMPT: str = """
    Extract the following information from the resume text in a structured format:
    - First Name
    - Last Name
    - Email
    - Phone
    - Education History (list of schools, degrees, and dates)
    - Work Experience Summary
    - Skills (as a list)
    - Current Position
    - Years of Experience
    
    Format the output as a JSON object.
    """
    
    CHAT_SYSTEM_PROMPT: str = """
    You are an AI HR assistant that helps analyze candidate data and answer questions about candidates.
    Base your responses only on the provided candidate data.
    Be concise and professional in your responses.
    """

settings = Settings() 