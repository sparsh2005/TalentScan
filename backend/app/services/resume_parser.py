from pdfminer.high_level import extract_text
from docx import Document
import json
from typing import Dict, Any
from app.core.config import settings
from openai import AsyncOpenAI

aclient = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
from app.core.config import settings

class ResumeParser:
    def __init__(self):

    def parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            return extract_text(file_path)
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")

    def parse_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")

    async def extract_information(self, text: str) -> Dict[str, Any]:
        """Extract structured information from resume text using OpenAI"""
        try:
            response = await aclient.chat.completions.create(model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts information from resumes."},
                {"role": "user", "content": settings.EXTRACTION_PROMPT + "\n\nResume text:\n" + text}
            ],
            temperature=0.0)

            # Parse the response into a dictionary
            extracted_info = json.loads(response.choices[0].message.content)
            return extracted_info

        except Exception as e:
            raise Exception(f"Error extracting information: {str(e)}")

    async def parse_resume(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Main method to parse resume and extract information"""
        try:
            # Extract text based on file type
            if file_type == "application/pdf":
                text = self.parse_pdf(file_path)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = self.parse_docx(file_path)
            else:
                raise ValueError("Unsupported file type")

            # Extract structured information
            return await self.extract_information(text)

        except Exception as e:
            raise Exception(f"Error processing resume: {str(e)}") 